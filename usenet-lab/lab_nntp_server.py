#!/usr/bin/env python3
"""A small NNTP server for the Usenet for Mere Mortals lab.

This is a real NNTP server: it listens on a TCP socket and speaks
the reader protocol of RFC 3977 (plus the older XOVER spelling).
It is deliberately small -- one file, no dependencies beyond the
Python 3 standard library -- so a reader can read the whole of it
and see that there is no magic in a news server.

What it implements:

  CAPABILITIES, MODE READER, DATE, HELP, QUIT
  LIST ACTIVE / NEWSGROUPS / OVERVIEW.FMT / ACTIVE.TIMES
  GROUP, LISTGROUP
  ARTICLE, HEAD, BODY, STAT, NEXT, LAST   (by number or message-id)
  OVER, XOVER
  POST  (with cross-posting, and read-only groups refused)

Articles are stored as plain text files in a spool directory:

  SPOOL/<group>/<number>.txt

so you can open the spool with ordinary tools and see exactly what
the server is holding. Groups are the fixed, invented set below --
a real server learns new groups from control messages and feeds;
this lab keeps its handful still so the transcripts stay readable.

Run it:

  python3 lab_nntp_server.py --spool ./spool --port 11119

Then talk to it with any NNTP client, or with the raw_session.py
script in this folder.
"""

import argparse
import email.utils
import json
import os
import re
import socketserver
import sys
import threading
import time

# The lab's invented groups: name -> (description, posting status).
# Status letters are the ones LIST ACTIVE uses everywhere:
#   y = posting allowed, n = posting not allowed (read-only).
GROUPS = {
    "lab.announce": ("Announcements from the keeper of this lab server", "y"),
    "lab.general": ("General discussion on the lab network", "y"),
    "lab.knitting": ("Knitting: patterns, yarn and works in progress", "y"),
    "lab.recipes": ("Recipes and kitchen notes", "y"),
    "lab.binaries": ("Small binary postings for the lab (see the NZB chapter)", "y"),
    "lab.test": ("Test posts live here. Post as much as you like", "y"),
    "lab.archive": ("Read-only archive of finished threads", "n"),
}

# The overview database fields, exactly as LIST OVERVIEW.FMT reports.
# The two entries starting with ':' are metadata the server counts
# itself rather than headers it copies.
OVERVIEW_FMT = [
    "Subject:",
    "From:",
    "Date:",
    "Message-ID:",
    "References:",
    ":bytes",
    ":lines",
]

SERVER_HOSTNAME = "lab.invalid"
KEEPER = "sam@lab.invalid"


def now_rfc2822():
    return email.utils.formatdate(time.time(), localtime=False)


def parse_headers(raw):
    """Split a raw article into (header dict, header block, body).

    Handles folded headers (continuation lines start with space/tab)
    the simple way RFC 5322 specifies: unfold by joining lines.
    Header names in the returned dict are lower-cased.
    """
    text = raw.decode("utf-8", "replace")
    head, _, body = text.partition("\n\n")
    headers = {}
    current = None
    for line in head.split("\n"):
        if line[:1] in (" ", "\t") and current is not None:
            headers[current] += " " + line.strip()
        elif ":" in line:
            name, _, value = line.partition(":")
            current = name.strip().lower()
            headers[current] = value.strip()
        else:
            current = None
    return headers, head, body


class Spool:
    """The article store: files on disk plus in-memory indexes."""

    def __init__(self, root):
        self.root = root
        self.lock = threading.Lock()
        self.by_msgid = {}          # msgid -> (group, number)
        self.numbers = {}           # group -> sorted list of numbers
        self.counter = 0            # for minting message-ids
        for group in GROUPS:
            os.makedirs(os.path.join(root, group), exist_ok=True)
            nums = []
            for name in os.listdir(os.path.join(root, group)):
                if name.endswith(".txt") and name[:-4].isdigit():
                    num = int(name[:-4])
                    raw = self._read(group, num)
                    headers, _, _ = parse_headers(raw)
                    msgid = headers.get("message-id", "")
                    if msgid:
                        self.by_msgid[msgid] = (group, num)
                    nums.append(num)
            self.numbers[group] = sorted(nums)

    def _path(self, group, num):
        return os.path.join(self.root, group, "%d.txt" % num)

    def _read(self, group, num):
        with open(self._path(group, num), "rb") as fh:
            return fh.read()

    def read(self, group, num):
        if num in self.numbers.get(group, []):
            return self._read(group, num)
        return None

    def find(self, msgid):
        return self.by_msgid.get(msgid)

    def read_by_msgid(self, msgid):
        found = self.find(msgid)
        if not found:
            return None
        group, num = found
        return group, num, self._read(group, num)

    def counts(self, group):
        nums = self.numbers.get(group, [])
        if not nums:
            return 0, 0, 0
        return len(nums), nums[0], nums[-1]

    def post(self, raw, groups):
        """Store one article in each of `groups` (a cross-post).

        Returns the message-id used. The same message-id is filed
        under one article number per group, as real servers do.
        """
        headers, head, body = parse_headers(raw)
        with self.lock:
            msgid = headers.get("message-id")
            if not msgid or msgid in self.by_msgid:
                self.counter += 1
                msgid = "<lab-%d-%d@%s>" % (
                    int(time.time()), self.counter, SERVER_HOSTNAME)
                if "message-id" in headers:
                    head = re.sub(r"(?im)^Message-ID:.*$",
                                  "Message-ID: " + msgid, head, count=1)
                else:
                    head += "\nMessage-ID: " + msgid
            if "date" not in headers:
                head += "\nDate: " + now_rfc2822()
            stored = (head + "\n\n" + body).encode("utf-8")
            for group in groups:
                nums = self.numbers[group]
                num = (nums[-1] + 1) if nums else 1
                with open(self._path(group, num), "wb") as fh:
                    fh.write(stored)
                nums.append(num)
                self.by_msgid[msgid] = (group, num)
            return msgid


class NNTPHandler(socketserver.StreamRequestHandler):
    timeout = 300

    # -- plumbing -----------------------------------------------------

    def send(self, line):
        self.wfile.write(line.encode("utf-8") + b"\r\n")

    def send_block(self, text):
        """Send a multi-line response body, dot-stuffed, dot-ended."""
        for line in text.replace("\r\n", "\n").split("\n"):
            if line.startswith("."):
                line = "." + line
            self.send(line)
        self.send(".")

    def setup(self):
        super().setup()
        self.close_connection = False
        self.group = None        # currently selected group name
        self.current = None      # currently selected article number

    # -- helpers ------------------------------------------------------

    def resolve_article(self, arg):
        """Resolve an ARTICLE/HEAD/BODY/STAT argument.

        Returns (group, number, raw) or sends an error and returns
        None. An empty argument means 'the current article'.
        """
        spool = self.server.spool
        if arg.startswith("<"):
            found = spool.read_by_msgid(arg)
            if not found:
                self.send("430 No such article found")
                return None
            return found
        if arg == "":
            if self.group is None:
                self.send("412 No newsgroup selected")
                return None
            if self.current is None:
                self.send("420 No current article has been selected")
                return None
            num = self.current
        else:
            if self.group is None:
                self.send("412 No newsgroup selected")
                return None
            if not arg.isdigit():
                self.send("501 Syntax error in article number")
                return None
            num = int(arg)
        raw = spool.read(self.group, num)
        if raw is None:
            self.send("423 No such article number in this group")
            return None
        return self.group, num, raw

    def overview_line(self, group, num, raw):
        headers, _, body = parse_headers(raw)
        fields = [str(num)]
        for fmt in OVERVIEW_FMT:
            if fmt == ":bytes":
                fields.append(str(len(raw)))
            elif fmt == ":lines":
                fields.append(str(len(body.split("\n")) if body else 0))
            else:
                fields.append(headers.get(fmt[:-1].lower(), ""))
        return "\t".join(fields)

    # -- command handlers ----------------------------------------------

    def cmd_capabilities(self, arg):
        self.send("101 Capability list:")
        lines = [
            "VERSION 2",
            "READER",
            "POST",
            "OVER",
            "LIST ACTIVE ACTIVE.TIMES NEWSGROUPS OVERVIEW.FMT",
        ]
        for line in lines:
            self.send(line)
        self.send(".")

    def cmd_mode(self, arg):
        if arg.upper() == "READER":
            self.send("200 Reader mode, posting ok")
        else:
            self.send("501 Unknown MODE")

    def cmd_date(self, arg):
        self.send("111 " + time.strftime("%Y%m%d%H%M%S", time.gmtime()))

    def cmd_help(self, arg):
        self.send("100 Help text follows")
        self.send_block(
            "Commands understood:\n"
            "  CAPABILITIES            MODE READER          DATE\n"
            "  LIST [ACTIVE|NEWSGROUPS|OVERVIEW.FMT|ACTIVE.TIMES]\n"
            "  GROUP <name>            LISTGROUP [<name>]\n"
            "  ARTICLE|HEAD|BODY|STAT [<number>|<message-id>]\n"
            "  NEXT  LAST              OVER <range>         XOVER <range>\n"
            "  POST                    QUIT                 HELP")

    def cmd_list(self, arg):
        spool = self.server.spool
        parts = arg.split()
        kind = parts[0].upper() if parts else "ACTIVE"
        pattern = parts[1] if len(parts) > 1 else None

        def wanted(name):
            if pattern is None:
                return True
            regex = "^" + re.escape(pattern).replace(r"\*", ".*") + "$"
            return re.match(regex, name) is not None

        if kind == "ACTIVE":
            self.send("215 List of newsgroups follows")
            for name in sorted(GROUPS):
                if wanted(name):
                    _, first, last = spool.counts(name)
                    self.send("%s %d %d %s" % (name, last, first,
                                               GROUPS[name][1]))
            self.send(".")
        elif kind == "NEWSGROUPS":
            self.send("215 Descriptions of newsgroups follow")
            for name in sorted(GROUPS):
                if wanted(name):
                    self.send("%s\t%s" % (name, GROUPS[name][0]))
            self.send(".")
        elif kind == "OVERVIEW.FMT":
            self.send("215 Overview format follows")
            for fmt in OVERVIEW_FMT:
                self.send(fmt)
            self.send(".")
        elif kind == "ACTIVE.TIMES":
            self.send("215 Active times follow")
            for name in sorted(GROUPS):
                if wanted(name):
                    self.send("%s 1759000000 %s" % (name, KEEPER))
            self.send(".")
        else:
            self.send("501 Unknown LIST type")

    def cmd_group(self, arg):
        name = arg.strip()
        if name not in GROUPS:
            self.send("411 No such newsgroup")
            return
        count, first, last = self.server.spool.counts(name)
        self.group = name
        self.current = first if count else None
        self.send("211 %d %d %d %s" % (count, first, last, name))

    def cmd_listgroup(self, arg):
        name = arg.strip() or self.group
        if name is None:
            self.send("412 No newsgroup selected")
            return
        if name not in GROUPS:
            self.send("411 No such newsgroup")
            return
        self.group = name
        nums = self.server.spool.numbers[name]
        if nums:
            self.current = nums[0]
        count, first, last = self.server.spool.counts(name)
        self.send("211 %d %d %d %s" % (count, first, last, name))
        for num in nums:
            self.send(str(num))
        self.send(".")

    def _article_command(self, arg, want):
        resolved = self.resolve_article(arg.strip())
        if resolved is None:
            return
        group, num, raw = resolved
        if not arg.strip().startswith("<"):
            self.current = num
        headers, head, body = parse_headers(raw)
        msgid = headers.get("message-id", "<unknown@%s>" % SERVER_HOSTNAME)
        if want == "ARTICLE":
            self.send("220 %d %s Article follows" % (num, msgid))
            self.send_block(raw.decode("utf-8", "replace"))
        elif want == "HEAD":
            self.send("221 %d %s Headers follow" % (num, msgid))
            self.send_block(head)
        elif want == "BODY":
            self.send("222 %d %s Body follows" % (num, msgid))
            self.send_block(body)
        elif want == "STAT":
            self.send("223 %d %s" % (num, msgid))

    def cmd_article(self, arg):
        self._article_command(arg, "ARTICLE")

    def cmd_head(self, arg):
        self._article_command(arg, "HEAD")

    def cmd_body(self, arg):
        self._article_command(arg, "BODY")

    def cmd_stat(self, arg):
        self._article_command(arg, "STAT")

    def cmd_next(self, arg):
        self._step(1)

    def cmd_last(self, arg):
        self._step(-1)

    def _step(self, direction):
        if self.group is None:
            self.send("412 No newsgroup selected")
            return
        if self.current is None:
            self.send("420 No current article has been selected")
            return
        nums = self.server.spool.numbers[self.group]
        idx = nums.index(self.current) + direction
        if idx < 0:
            self.send("422 No previous article in this group")
            return
        if idx >= len(nums):
            self.send("421 No next article in this group")
            return
        self.current = nums[idx]
        raw = self.server.spool.read(self.group, self.current)
        headers, _, _ = parse_headers(raw)
        self.send("223 %d %s" % (self.current,
                                 headers.get("message-id", "")))

    def cmd_over(self, arg):
        if self.group is None:
            self.send("412 No newsgroup selected")
            return
        nums = self.server.spool.numbers[self.group]
        arg = arg.strip()
        if arg.startswith("<"):
            self.send("502 OVER by message-id is not implemented here")
            return
        if arg == "":
            if self.current is None:
                self.send("420 No current article has been selected")
                return
            wanted = [self.current]
        elif "-" in arg:
            lo, _, hi = arg.partition("-")
            lo = int(lo) if lo.isdigit() else 0
            hi = int(hi) if hi.isdigit() else (nums[-1] if nums else 0)
            wanted = [n for n in nums if lo <= n <= hi]
        elif arg.isdigit():
            wanted = [n for n in nums if n == int(arg)]
        else:
            self.send("501 Syntax error in range")
            return
        if not wanted:
            self.send("423 No articles in that range")
            return
        self.send("224 Overview information follows")
        for num in wanted:
            raw = self.server.spool.read(self.group, num)
            self.send(self.overview_line(self.group, num, raw))
        self.send(".")

    def cmd_post(self, arg):
        self.send("340 Send article, end with a line holding one dot")
        lines = []
        while True:
            line = self.rfile.readline()
            if not line:
                return
            line = line.decode("utf-8", "replace").rstrip("\r\n")
            if line == ".":
                break
            if line.startswith(".."):
                line = line[1:]
            lines.append(line)
        raw = "\n".join(lines).encode("utf-8")
        headers, _, _ = parse_headers(raw)
        for required in ("from", "subject", "newsgroups"):
            if required not in headers:
                self.send("441 Posting failed: no %s: header"
                          % required.capitalize())
                return
        groups = [g.strip() for g in headers["newsgroups"].split(",")]
        for group in groups:
            if group not in GROUPS:
                self.send("441 Posting failed: unknown group %s" % group)
                return
            if GROUPS[group][1] == "n":
                self.send("440 Posting not allowed in %s" % group)
                return
        msgid = self.server.spool.post(raw, groups)
        self.send("240 Article received " + msgid)

    def cmd_quit(self, arg):
        self.send("205 Closing connection. Goodbye.")
        self.close_connection = True

    COMMANDS = {
        "CAPABILITIES": cmd_capabilities,
        "MODE": cmd_mode,
        "DATE": cmd_date,
        "HELP": cmd_help,
        "LIST": cmd_list,
        "GROUP": cmd_group,
        "LISTGROUP": cmd_listgroup,
        "ARTICLE": cmd_article,
        "HEAD": cmd_head,
        "BODY": cmd_body,
        "STAT": cmd_stat,
        "NEXT": cmd_next,
        "LAST": cmd_last,
        "OVER": cmd_over,
        "XOVER": cmd_over,
        "POST": cmd_post,
        "QUIT": cmd_quit,
    }

    def handle(self):
        self.send("200 %s lab NNTP server ready (posting ok)"
                  % SERVER_HOSTNAME)
        while not self.close_connection:
            line = self.rfile.readline()
            if not line:
                break
            line = line.decode("utf-8", "replace").strip()
            if not line:
                continue
            verb, _, arg = line.partition(" ")
            handler = self.COMMANDS.get(verb.upper())
            if handler is None:
                self.send("500 Command not recognised")
            else:
                handler(self, arg.strip())


class Server(socketserver.ThreadingTCPServer):
    daemon_threads = True
    allow_reuse_address = True

    def __init__(self, address, spool):
        self.spool = spool
        super().__init__(address, NNTPHandler)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--spool", default="./spool",
                        help="directory holding the article files")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=11119)
    args = parser.parse_args()

    spool = Spool(args.spool)
    server = Server((args.host, args.port), spool)
    print("lab NNTP server listening on %s:%d, spool %s"
          % (args.host, args.port, os.path.abspath(args.spool)),
          flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""nzb_round_trip.py -- a file, posted as articles, fetched back by NZB.

The whole binary side of Usenet in one small run:

  1. Make a small file and note its SHA-256.
  2. Split it into segments. yEnc-encode each segment and post it
     to lab.binaries as its own article, the way binary posters do.
  3. Write an NZB file: XML that names, for each segment, the
     message-id of the article holding it (angle brackets off --
     that is the NZB convention).
  4. Forget the original. Read only the NZB, fetch each segment by
     message-id from the server, yEnc-decode, join in segment
     order, and compare SHA-256 with step 1.

That fetch-by-message-id step is the entire job of a Usenet
downloader such as SABnzbd, minus the repair work (PAR2) and the
unpacking. Run it in a scratch folder: it writes the file, the
.nzb and the rebuilt copy there.
"""

import binascii
import hashlib
import io
import os
import re
import sys
import warnings
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape, quoteattr

warnings.filterwarnings("ignore", category=DeprecationWarning)

import nntplib

HOST, PORT = "127.0.0.1", 11119
GROUP = "lab.binaries"
POSTER = "Sam Keeper <sam@lab.invalid>"
FILENAME = "harbour-chart.bin"
FILE_SIZE = 900
SEGMENT_SIZE = 300
NS = "{http://www.newzbin.com/DTD/2003/nzb}"


# -- yEnc ----------------------------------------------------------------
# yEnc in brief: add 42 to each byte (mod 256). If the result is a
# character that would confuse the transport (NUL, TAB, LF, CR,
# space, '.', '=') write '=' followed by the character + 64.
# Lines are wrapped at 128 characters.

CRITICAL = {0, 9, 10, 13, 32, 46, 61}


def yenc_encode(data):
    out = []
    col = 0
    for byte in data:
        c = (byte + 42) % 256
        chunk = ""
        if c in CRITICAL:
            chunk = "=" + chr((c + 64) % 256)
        else:
            chunk = chr(c)
        if col + len(chunk) > 128:
            out.append("\n")
            col = 0
        out.append(chunk)
        col += len(chunk)
    return "".join(out)


def yenc_decode(text):
    out = bytearray()
    i = 0
    while i < len(text):
        ch = text[i]
        if ch == "=":
            i += 1
            out.append((ord(text[i]) - 64 - 42) % 256)
        elif ch in ("\n", "\r"):
            pass
        else:
            out.append((ord(ch) - 42) % 256)
        i += 1
    return bytes(out)


# -- the posting half ------------------------------------------------------

def make_file(path):
    """A small deterministic binary: every byte value, patterned."""
    data = bytes(((i * 37) + 11) % 256 for i in range(FILE_SIZE))
    with open(path, "wb") as fh:
        fh.write(data)
    return data


def post_segments(server, data):
    """Post each yEnc segment as an article. Returns segment records."""
    segments = []
    total_parts = (len(data) + SEGMENT_SIZE - 1) // SEGMENT_SIZE
    for index in range(total_parts):
        part = data[index * SEGMENT_SIZE:(index + 1) * SEGMENT_SIZE]
        begin = index * SEGMENT_SIZE + 1
        end = begin + len(part) - 1
        crc = "%08x" % (binascii.crc32(part) & 0xFFFFFFFF)
        body = (
            "=ybegin part=%d line=128 size=%d name=%s\n"
            "=ypart begin=%d end=%d\n"
            "%s\n"
            "=yend size=%d part=%d pcrc32=%s"
            % (index + 1, len(data), FILENAME, begin, end,
               yenc_encode(part), len(part), index + 1, crc))
        article = (
            "From: %s\n"
            "Subject: %s [%d/%d]\n"
            "Newsgroups: %s\n"
            "\n"
            "%s\n" % (POSTER, FILENAME, index + 1, total_parts,
                      GROUP, body))
        reply = server.post(io.BytesIO(article.encode("utf-8")))
        msgid = reply[reply.index("<"):reply.index(">") + 1]
        segments.append({"number": index + 1, "bytes": len(body),
                         "id": msgid})
        print("posted segment %d/%d as %s" % (index + 1, total_parts,
                                              msgid))
    return segments


def write_nzb(path, segments):
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<!DOCTYPE nzb PUBLIC "-//newzBin//DTD NZB 2.0//EN" '
        '"http://www.newzbin.com/DTD/nzb/nzb-2.0.dtd">',
        '<nzb xmlns="http://www.newzbin.com/DTD/2003/nzb">',
        # Attribute values go through quoteattr: a poster's
        # address contains < and >, which XML forbids raw.
        '  <file poster=%s date="1759000000" '
        'subject=%s>' % (quoteattr(POSTER),
                         quoteattr("%s [%d/%d]" % (FILENAME,
                                                    len(segments),
                                                    len(segments)))),
        "    <groups>",
        "      <group>%s</group>" % GROUP,
        "    </groups>",
        "    <segments>",
    ]
    for seg in segments:
        # NZB stores message-ids WITHOUT their angle brackets.
        lines.append('      <segment bytes="%d" number="%d">%s</segment>'
                     % (seg["bytes"], seg["number"],
                        escape(seg["id"].strip("<>"))))
    lines += ["    </segments>", "  </file>", "</nzb>"]
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")


# -- the fetching half -----------------------------------------------------

def fetch_by_nzb(server, nzb_path):
    """Read only the NZB; fetch, decode and join the segments."""
    tree = ET.parse(nzb_path)
    file_el = tree.getroot().find(NS + "file")
    segments = []
    for seg in file_el.find(NS + "segments").findall(NS + "segment"):
        segments.append((int(seg.get("number")), "<" + seg.text + ">"))
    segments.sort()
    pieces = {}
    for number, msgid in segments:
        _, info = server.article(msgid)
        body = b"\n".join(info.lines).decode("utf-8", "replace")
        ypart = re.search(r"=ypart begin=(\d+) end=(\d+)", body)
        yend = re.search(r"=yend size=\d+ part=\d+ pcrc32=([0-9a-f]+)",
                         body)
        payload = body[ypart.end():yend.start()].strip("\n")
        data = yenc_decode(payload)
        crc = "%08x" % (binascii.crc32(data) & 0xFFFFFFFF)
        status = "ok" if crc == yend.group(1) else "CRC MISMATCH"
        print("fetched segment %d (%s): %d bytes, part CRC %s"
              % (number, msgid, len(data), status))
        pieces[int(ypart.group(1))] = data
    return b"".join(pieces[k] for k in sorted(pieces))


def main():
    original = make_file(FILENAME)
    digest = hashlib.sha256(original).hexdigest()
    print("made %s: %d bytes" % (FILENAME, len(original)))
    print("sha256 of the original: %s" % digest)

    server = nntplib.NNTP(HOST, port=PORT)
    segments = post_segments(server, original)
    nzb_name = FILENAME + ".nzb"
    write_nzb(nzb_name, segments)
    print("\nwrote %s:" % nzb_name)
    with open(nzb_name, "r", encoding="utf-8") as fh:
        print(fh.read())

    print("forgetting the original; fetching from the NZB alone")
    rebuilt = fetch_by_nzb(server, nzb_name)
    server.quit()
    with open("rebuilt-" + FILENAME, "wb") as fh:
        fh.write(rebuilt)
    rebuilt_digest = hashlib.sha256(rebuilt).hexdigest()
    print("\nsha256 of the rebuilt file: %s" % rebuilt_digest)
    print("MATCH" if rebuilt_digest == digest else "MISMATCH")
    return 0 if rebuilt_digest == digest else 1


if __name__ == "__main__":
    sys.exit(main())

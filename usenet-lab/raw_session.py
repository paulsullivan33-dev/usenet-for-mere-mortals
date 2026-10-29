#!/usr/bin/env python3
"""raw_session.py -- talk to an NNTP server with nothing in between.

Connects to the lab server, then sends each command given on the
command line (or in a script file of one command per line) and
prints the conversation exactly as it crosses the wire:

  C: the line the client sent
  S: the line the server answered

For POST, the pseudo-command  POST <file>  sends the article held
in <file> after the server's 340 invitation, ending it with the
single dot the protocol requires; a body line that begins with a
dot is dot-stuffed on the way out, as a real client must do.

Examples:

  python3 raw_session.py CAPABILITIES DATE QUIT
  python3 raw_session.py --script session.txt
"""

import socket
import sys

HOST, PORT = "127.0.0.1", 11119


def read_reply(rfile):
    """Read one reply; returns the list of its lines.

    A reply is either a single status line, or a status line whose
    code ends a multi-line block (101, 100, 211 with list, 215,
    220, 221, 222, 224) followed by lines and a lone dot.
    """
    first = rfile.readline().decode("utf-8", "replace").rstrip("\r\n")
    lines = [first]
    code = first[:3]
    if code in ("100", "101", "211", "215", "220", "221", "222", "224"):
        # 211 is multi-line only for LISTGROUP; a GROUP reply is one
        # line. The caller tells us which by the command, handled by
        # checking whether more data belongs: for a bare GROUP the
        # next line would be the *next* reply, so only LISTGROUP
        # passes through here -- see send_command.
        pass
    return lines


def read_block(rfile, first):
    lines = [first]
    while True:
        line = rfile.readline().decode("utf-8", "replace").rstrip("\r\n")
        lines.append(line)
        if line == ".":
            return lines


MULTILINE = {"100", "101", "215", "220", "221", "222", "224"}


def exchange(sock, rfile, command):
    """Send one command, print both sides, return the reply lines."""
    print("C: " + command)
    sock.sendall(command.encode("utf-8") + b"\r\n")
    first = rfile.readline().decode("utf-8", "replace").rstrip("\r\n")
    lines = [first]
    code = first[:3]
    verb = command.split(" ")[0].upper()
    if code in MULTILINE or (code == "211" and verb == "LISTGROUP"):
        lines += read_block(rfile, first)[1:]
    for line in lines:
        if line.startswith(".."):
            line = line[1:]  # undo dot-stuffing for display
        print("S: " + line)
    return lines


def do_post(sock, rfile, filename):
    print("C: POST")
    sock.sendall(b"POST\r\n")
    first = rfile.readline().decode("utf-8", "replace").rstrip("\r\n")
    print("S: " + first)
    if not first.startswith("340"):
        return
    with open(filename, "r", encoding="utf-8") as fh:
        article = fh.read().replace("\r\n", "\n").strip("\n")
    for line in article.split("\n"):
        shown = line
        if line.startswith("."):
            line = "." + line  # dot-stuffing
            shown = line + "   (dot-stuffed)"
        print("C: " + shown)
        sock.sendall(line.encode("utf-8") + b"\r\n")
    print("C: .")
    sock.sendall(b".\r\n")
    reply = rfile.readline().decode("utf-8", "replace").rstrip("\r\n")
    print("S: " + reply)


def main():
    args = sys.argv[1:]
    commands = []
    if args[:1] == ["--script"]:
        with open(args[1], "r", encoding="utf-8") as fh:
            commands = [ln.strip() for ln in fh if ln.strip()]
    else:
        commands = args
    with socket.create_connection((HOST, PORT)) as sock:
        rfile = sock.makefile("rb")
        greeting = rfile.readline().decode("utf-8", "replace").rstrip("\r\n")
        print("S: " + greeting)
        for command in commands:
            if command.upper().startswith("POST "):
                do_post(sock, rfile, command.split(None, 1)[1])
            else:
                exchange(sock, rfile, command)
        if not any(c.upper() == "QUIT" for c in commands):
            exchange(sock, rfile, "QUIT")


if __name__ == "__main__":
    main()

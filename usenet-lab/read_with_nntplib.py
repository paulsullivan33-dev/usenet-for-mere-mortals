#!/usr/bin/env python3
"""read_with_nntplib.py -- read the lab server the way a program does.

Walks the ordinary reading path with Python's nntplib: list the
groups, enter lab.knitting, scan the overview (subjects without
bodies), then fetch one article whole, and the same article's
head and body separately so the difference is visible.
"""

import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)

import nntplib

HOST, PORT = "127.0.0.1", 11119


def show(label, value):
    print("%s: %s" % (label, value))


def main():
    server = nntplib.NNTP(HOST, port=PORT)
    show("greeting", server.getwelcome())

    _, groups = server.list()
    print("\ngroups on this server:")
    for g in groups:
        print("  %-14s last=%s first=%s posting=%s"
              % (g.group, g.last, g.first, g.flag))

    resp, count, first, last, name = server.group("lab.knitting")
    print("\nentered %s: %s articles, numbers %s to %s"
          % (name, count, first, last))

    _, overview = server.over((int(first), int(last)))
    print("\noverview (one line per article, no bodies):")
    for num, fields in overview:
        print("  %s | %s | %s" % (num, fields["subject"], fields["from"]))

    _, info = server.article(int(first))
    print("\narticle %s in full:" % first)
    for line in info.lines:
        print("  " + line.decode("utf-8", "replace"))

    _, head = server.head(int(first))
    print("\nhead of article %s (headers only):" % first)
    for line in head.lines:
        print("  " + line.decode("utf-8", "replace"))

    _, body = server.body(int(first))
    print("\nbody of article %s (body only):" % first)
    for line in body.lines:
        print("  " + line.decode("utf-8", "replace"))

    server.quit()


if __name__ == "__main__":
    main()

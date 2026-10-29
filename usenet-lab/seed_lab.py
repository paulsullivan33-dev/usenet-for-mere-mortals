#!/usr/bin/env python3
"""seed_lab.py -- stock the lab server with its first articles.

Posts four invented articles through the ordinary NNTP POST path,
using Python's nntplib (a real NNTP client library) so the server
is exercised exactly as any newsreader would exercise it. Run once
against a fresh server; the articles it plants are the ones the
reading transcripts then browse. It finishes by trying to post
to the read-only archive group and being refused -- the keeper
files that one directly, with file_to_archive.py.

Every person, address and group here is invented for the lab.
Addresses use lab.invalid and example.org, domains reserved for
made-up examples.
"""

import io
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)

import nntplib

HOST, PORT = "127.0.0.1", 11119

ARTICLES = [
    ("""From: Sam Keeper <sam@lab.invalid>
Subject: Welcome to the lab news server
Newsgroups: lab.announce

Welcome. This server exists so the Usenet guide's readers can
watch the NNTP protocol work at close range.

Everything here is invented and local: the groups, the people
and the posts. Read anything, post test articles to lab.test,
and do not worry about breaking it -- the spool is a folder of
plain text files and can be emptied to start again.

Sam, server keeper
"""),
    ("""From: Alex Rivers <alex@example.org>
Subject: Choosing needles for a first jumper
Newsgroups: lab.knitting

I am about to start my first jumper and the pattern just says
"4 mm needles". The shop has straight pairs, circulars, and
double-pointed sets, all in 4 mm. Does the shape matter, or
only the size?

The wool is an ordinary double-knitting yarn, if that helps.
"""),
    ("""From: Jo Field <jo@example.net>
Subject: Re: Choosing needles for a first jumper
References: {REFERENCES}
Newsgroups: lab.knitting

Alex Rivers wrote:
> only the size?

The size sets your tension, so that part matters most. The
shape is about comfort: a jumper body is a wide piece, and a
circular needle used flat holds the weight in your lap
instead of on your wrists. Start there.
"""),
    ("""From: Priya Nair <priya@example.org>
Subject: A plain loaf that always works
Newsgroups: lab.recipes

500 g strong white flour, 7 g dried yeast, 10 g salt,
325 ml warm water. Mix, knead ten minutes, rise one hour,
shape, rise thirty minutes more, bake 30 minutes at 220 C.

It has never failed me. The crust is better if you put a
small tray of water in the bottom of the oven.
"""),
]


def main():
    server = nntplib.NNTP(HOST, port=PORT)
    print("server greeting:", server.getwelcome())
    references = ""
    for text in ARTICLES:
        # The knitting reply quotes the question's message-id in
        # its References header -- that header is the thread.
        text = text.replace("{REFERENCES}", references)
        reply = server.post(io.BytesIO(text.encode("utf-8")))
        subject = [ln for ln in text.splitlines()
                   if ln.startswith("Subject:")][0]
        print("posted:", subject, "->", reply)
        if "<" in reply:  # the 240 reply carries the message-id
            references = reply[reply.index("<"):reply.index(">") + 1]

    # One more article belongs in lab.archive -- but that group
    # is read-only, so POST must refuse it. Watch:
    archive_post = (
        "From: Sam Keeper <sam@lab.invalid>\n"
        "Subject: Thread: the spring swap meet (closed)\n"
        "Newsgroups: lab.archive\n\n"
        "This thread discussed the spring swap meet.\n")
    try:
        server.post(io.BytesIO(archive_post.encode("utf-8")))
        print("posted to lab.archive -- unexpected!")
    except nntplib.NNTPTemporaryError as exc:
        print("posting to lab.archive refused, as designed:", exc)
        print("the keeper files archive material directly instead")
        print("(see file_to_archive.py)")
    server.quit()
    print("done")


if __name__ == "__main__":
    main()

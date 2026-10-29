# Your First Groups

The outcome: you have run a real NNTP
server, read a thread through it, and
posted an article with your own hands —
and you can name the protocol command
behind each thing a newsreader does.

Everything here happens against the
lab server in `usenet-lab/`. Transcripts
are quoted from `usenet-lab/transcripts/`;
lines beginning `C:` are what the client
sent, `S:` what the server answered. The
server is small, but nothing about the
conversation is simulated: the clients
are a raw socket script and Python's
`nntplib`, and any real newsreader would
have the same conversation.

## Start the server, hear it greet you

```console
$ python3 lab_nntp_server.py --spool ./spool --port 11119 &
lab NNTP server listening on 127.0.0.1:11119, spool ...
```

Connect, and before you type anything
the server speaks first (t00):

```text
S: 200 lab.invalid lab NNTP server ready (posting ok)
C: CAPABILITIES
S: 101 Capability list:
S: VERSION 2
S: READER
S: POST
S: OVER
S: LIST ACTIVE ACTIVE.TIMES NEWSGROUPS OVERVIEW.FMT
S: .
```

Two habits to build now. A reply's
number is its meaning: `200` is a
greeting that permits posting (a
read-only server would say `201`). And
a multi-line answer — the capability
list here — ends with a line holding a
single dot. Every list in this protocol
ends that way, including articles
themselves, which is why a body line
that is only a dot needs care (below).

`CAPABILITIES` is the server's honest
self-description: protocol version, that
it serves readers, that posting is
allowed, and which commands it knows.
A newsreader asks this first and greys
out buttons accordingly.

## Stock the shelves

A fresh server carries groups but no
articles. The lab stocks its seven
invented groups by *posting* to them,
with `seed_lab.py` driving `nntplib`
(t01): a welcome in `lab.announce`, a
knitting question and its reply in
`lab.knitting`, a recipe in
`lab.recipes`. Each post is answered

```text
240 Article received <lab-…-2@lab.invalid>
```

— accepted, and christened with a
message-id. The reply in `lab.knitting`
carries a `References:` header naming
the question's id; that header, and
nothing else, makes them a thread.

The seeder's last act is a refusal: it
tries to post into `lab.archive`, the
read-only group, and gets
`440 Posting not allowed`. Archives are
filed by the server's keeper, not by
posters — `file_to_archive.py` does it
directly into the spool, with the server
stopped, because the spool is only
re-read at startup.

## See what the server carries

t02 walks the four lists. `LIST ACTIVE`
is the master list — name, last and
first article numbers, posting flag:

```text
S: lab.archive 1 1 n
S: lab.knitting 2 1 y
```

`LIST NEWSGROUPS` gives the one-line
descriptions a reader shows while you
browse. `LIST OVERVIEW.FMT` declares the
overview's fields (chapter 2). And one
command enters a group:

```text
C: GROUP lab.knitting
S: 211 2 1 2 lab.knitting
```

`211`, then count, first number, last
number, name. Entering a group also
sets your **current article** pointer
to the first article — the pointer the
next section walks.

## Read, three ways

The same article can be fetched whole,
in halves, or not at all (t03, t06):

- `ARTICLE 1` — headers and body (`220`)
- `HEAD 1` — headers only (`221`); a
  reader uses this to show an article's
  shape before spending bandwidth
- `BODY 1` — body only (`222`)
- `STAT 1` — no text at all (`223`); it
  answers "does this number exist, and
  what is its message-id?" and moves
  your pointer to it
- `NEXT` / `LAST` — move the pointer one
  article and answer like `STAT`; at the
  end of the group, `NEXT` answers
  `421 No next article in this group`

And the overview: `OVER 1-2` returns one
tab-separated line per article (t06) —
subject, author, date, message-id,
references, size — the thread list your
newsreader draws, obtained without a
single body changing hands. (Many
servers also answer the older spelling,
`XOVER`; the lab implements both and
their output is identical.)

Fetching **by message-id** is the other
addressing mode, and t06 proves its
quirk: with the pointer sitting on
article 2, `ARTICLE <…-2@lab.invalid>`
fetches article 1 — and `STAT` afterwards
still says 2. Asking by id never moves
your place. Downloaders live on this
mode: an NZB is nothing but ids.

## Post by hand

t04 is the full ceremony, raw:

```text
C: POST
S: 340 Send article, end with a line holding one dot
C: From: Alex Rivers <alex@example.org>
C: Subject: A first post sent by hand
C: Newsgroups: lab.test
C:
C: This article was posted by hand …
C: ..This line starts with a dot in the body.   (dot-stuffed)
C: .
S: 240 Article received <lab-…-1@lab.invalid>
```

Three things to notice. The server
cannot refuse until it has your headers,
so a bad post is answered only *after*
the dot — t05 collects the refusals:
`441` for an unknown group or a missing
`Subject:`, `440` for a read-only one.
A body line beginning with a dot travels
**doubled** — dot-stuffing — because a
lone dot means "finished"; the reader
undoes it, and the article reads back
whole in the same transcript. And a
`Newsgroups:` header naming *two*
groups posts to both at once — one
article, one message-id, a different
number in each group. That is
**cross-posting**, and t04 reads the
same message-id back from both groups.

**Check yourself.** Start the lab
server, post any test article to
`lab.test` by hand, and fetch it twice:
once by its number, once by the
message-id in the `240` reply. When both
fetches return the same text, you have
done — personally, at the wire — the
two things every Usenet program exists
to do.

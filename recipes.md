# Recipes

Each recipe is a small job done whole,
against the lab server, from parts the
earlier chapters verified. Commands are
the lab's; on a real server the same
commands run inside your newsreader,
which is chapter 4's point.

## 1. Stand up the lab and look around

Start the server, stock it, and take
the tour a new reader takes:

```console
$ python3 lab_nntp_server.py --spool ./spool --port 11119 &
$ python3 seed_lab.py
$ python3 raw_session.py "LIST ACTIVE" "LIST NEWSGROUPS" QUIT
```

The list tells you the groups, their
sizes and their flags. You now hold
chapter 2's map with live numbers in
it — transcripts t00–t02 are this
recipe, recorded.

## 2. Follow one thread by its References

A thread is a chain of `References:`
headers. To walk the lab's knitting
thread: enter the group, take the
overview, and read the `References`
field of each line (t06):

```text
C: GROUP lab.knitting
C: OVER 1-2
```

Article 2's overview line ends its
header fields with article 1's
message-id — that is the reply pointing
at its parent. Fetch parents the same
way as long as the chain continues;
your newsreader simply draws the tree
this describes.

## 3. Post a follow-up that threads properly

A reply is an ordinary post with three
habits: the subject gains `Re: `, the
body quotes a line or two of the parent
(chapter 7), and the headers carry the
line the whole thread hangs from:

```text
From: Jo Field <jo@example.net>
Subject: Re: Choosing needles for a first jumper
References: <the parent's message-id>
Newsgroups: lab.knitting
```

Get the parent's id from its overview
line or its `220` reply, put it in
`References:`, and post with the raw
client or `nntplib`. The seeder did
exactly this (t01) — which is why the
overview in recipe 2 has a chain to
walk. A follow-up without `References:`
is a new thread wearing a familiar
subject, and readers' threading will
strand it.

## 4. Share a small file with a friend, by NZB

The binary round trip of chapter 6, as
a procedure (t07 is the recording):

```console
$ mkdir nzb-run && cd nzb-run
$ python3 ../nzb_round_trip.py
```

The script splits a file, yEnc-encodes
and posts the segments to
`lab.binaries`, and writes the NZB.
Send the `.nzb` file — tiny, a few
hundred bytes — to your friend by any
channel you like. On a shared server,
their run of the fetching half rebuilds
the file, and the two SHA-256 hashes
are how both of you know it arrived
whole. The map travels by email; the
file never does.

## 5. Ask a group what is new since you last looked

Remember a group's last article number
from your last visit — say `GROUP`
answered `211 2 1 2`. Next visit, the
same command might answer `211 5 1 5`.
The new articles are the range between:

```text
C: GROUP lab.knitting
C: OVER 3-5
```

Three overview lines, no bodies until
one earns a click. This is precisely
what a newsreader does with its
per-group read markers; the numbers
differ, the arithmetic does not.

## 6. Search a group's subjects without reading it

The overview is plain text — pipe a
wide `OVER` range through a text search
to find the threads about one thing:

```console
$ python3 raw_session.py "GROUP lab.recipes" "OVER 1-99" QUIT | grep -i loaf
```

Crude, and honest: subject lines are
the index Usenet gives you for free.
(Real readers index locally and search
faster; the data they search is the
same overview.)

## 7. Prove a post is not yours to delete

A sobering one, from chapter 7. Post a
test article to `lab.test`. Now try to
remove it from the network: your
reader's "retract" or "cancel", where
offered, sends another article asking
servers to delete yours. On the lab —
one server, yours — you can delete the
spool file by hand and restart. On the
real network there is no spool you
own, and every other copy answers to
someone else. The recipe's lesson is
its outcome: there is no step 3.

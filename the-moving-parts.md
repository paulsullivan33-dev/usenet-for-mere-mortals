# The Moving Parts

By the end of this chapter you can point
at each piece of the Usenet machine and
say what it holds. Every part named here
appears in the lab, and most can be
touched: the lab server's storage is a
folder of plain text files, shown in
transcript t08.

## The article

The atom. Headers, a blank line, a body.
The headers a reader relies on most:

- **From:** who posted it (a name and an
  address; chapter 7 explains why to
  think before using your real one)
- **Subject:** the thread's title
- **Newsgroups:** the group — or groups —
  it was posted to
- **Date:** when it was posted
- **Message-ID:** its unique name,
  assigned when the server accepts it
- **References:** the message-ids of the
  articles it replies to, oldest first —
  this header *is* the thread

Chapter 4 posts one by hand and reads
the server's additions back: the lab
server adds the `Message-ID:` and
`Date:` itself, as real servers do.

## The newsgroup

A named stream of articles. A group has
a name built from a dotted **hierarchy**
(chapter 5), a short description, and a
posting flag — open, moderated, or
read-only. In the lab, the flag is the
last letter of each `LIST ACTIVE` line
in transcript t02, and the read-only
group refuses a real post in t05.

## The server and its spool

A **news server** is the program that
stores articles, answers readers, and
(optionally) exchanges articles with
other servers. Its store is the
**spool**. On the lab server the spool
is deliberately ordinary — transcript
t08 lists it:

```text
spool/lab.knitting/1.txt
spool/lab.knitting/2.txt
```

One folder per group, one file per
article, numbered in arrival order.
That numbering explains a protocol
subtlety chapter 4 leans on: an article
has *two* addresses — its number, which
means something only inside one group
on one server, and its message-id, which
names it everywhere.

## The protocol: NNTP

**NNTP** (Network News Transfer
Protocol) is the conversation between a
reader and a server — and, in a fuller
dialect, between server and server.
It is plain text: a command word from
the client, a numbered reply from the
server. Three digits, and the first one
tells you the shape of what follows:
`2xx` success, `3xx` "send me more",
`4xx` a refusal you can understand,
`5xx` an error. Chapter 4 speaks it by
hand; every reply code the lab provoked
is catalogued in chapter 11.

## The overview

Servers keep a one-line summary per
article — subject, author, date,
message-id, references, size — called
the **overview**. It exists so a reader
can list a group's threads without
downloading every body. `LIST OVERVIEW.FMT`
(asking, in transcript t02) says which
fields the summaries hold, and `OVER`
fetches them (t06). When your newsreader
shows a thread list instantly, this is
what it just read.

## The newsreader

Your program: it connects, lists groups,
fetches overviews, displays the articles
you open, and sends your posts. Behind
every button is one of the commands in
chapter 4. **Thunderbird**, **Pan** and
**slrn** are long-lived examples,
described from their documentation in
this guide; the lab drives the same
protocol with scripts instead.

## The provider

The organisation that runs a server you
may use — usually for money, at scale,
with years of articles kept. You are
buying disk, bandwidth and upkeep, not
content; the content is the network's.
Chapter 3 unpacks the offer.

## The indexer and the NZB

For binaries, two extra parts. An
**indexer** is a catalogue that watches
binary groups and records which
articles make up which file. Its output
is an **NZB**: an XML file listing, for
each segment of a file, the message-id
of the article that holds it. Hand an
NZB to a **downloader** — SABnzbd is the
series' worked example — and it fetches
exactly those articles, decodes them,
and joins them. Chapter 6 builds one by
hand and spends it.

**Check yourself.** Given a group name,
a message-id and an NZB, you should now
be able to say which part a newsreader
asks, which part a server stores, and
which part a downloader reads. If any of
the three is fuzzy, the lab in chapter 4
will make it concrete.

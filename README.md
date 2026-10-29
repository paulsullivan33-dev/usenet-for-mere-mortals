# Usenet for Mere Mortals

Before the web, there was **Usenet**: a
worldwide discussion network, older than
the browser, built from a simple idea.
Nobody owns it. Thousands of **news
servers** each keep a copy of everything
posted, pass new **articles** to their
neighbours, and let their own readers
read and reply. There is no centre, no
front page, and no company in charge —
just servers exchanging articles, and
**newsgroups**, one for each topic, to
keep the conversation sorted.

An article looks like an email — headers
at the top, plain text below — and it is
read with a **newsreader** program over
a protocol called **NNTP**. The same
network also carries files, chopped into
encoded pieces and posted article by
article, and a small XML map called an
**NZB** file is what lets a downloader
gather the pieces and rebuild the file.
This guide explains all of it, and then
does the part most explanations skip: it
runs a real server and speaks the
protocol by hand, so you can watch every
claim happen.

The lab behind this guide ran a small
but genuine NNTP server — written for
the lab, speaking the standard protocol
(RFC 3977) — and two independent clients
against it: a raw script that prints the
conversation wire by wire, and Python's
`nntplib`, the client library real
programs use. Against that server the
lab listed groups, read and walked
threads, posted articles by hand
(including a cross-post to two groups at
once), provoked every ordinary error the
protocol has, and closed the loop on
binaries: it split a file into segments,
yEnc-encoded and posted them, wrote an
NZB naming them, and rebuilt the file
from the NZB alone. The rebuilt file's
SHA-256 matched the original exactly.

What the lab could not do, it did not
fake. It has no account with a
commercial **provider**, so signing up,
paying, and today's prices are described
from documentation, never quoted. It
never posted to the live network, so
propagation between real servers is
explained, not demonstrated. Repair of
damaged downloads with PAR2 data is
likewise pointed at, not run — the
[SABnzbd guide](https://paulsullivan33-dev.github.io/sabnzbd-for-mere-mortals/)
in this series does that work live.
`criteria.md` keeps the full ledger of
what was run and what was only read.

One warning belongs up front, because
everything else follows from it: a post
to Usenet is copied from server to
server and kept by strangers. There is
no reliable way to take one back.
Chapter 7 is about living with that
fact; the short version is to post
nothing you would not pin to a public
noticeboard, because in every way that
matters, you just did.

## What this guide covers

- [**What Usenet is**](what-usenet-is.md) —
  the mental model: a network of servers
  holding copies, articles like emails,
  groups for topics, and no centre at all
- [**The moving parts**](the-moving-parts.md) —
  articles, message-ids, groups, spools,
  the protocol, newsreaders, providers,
  indexers and NZB files — which part
  holds what
- [**Getting access**](getting-access.md) —
  what a provider actually sells:
  retention, completion, connections and
  encrypted access, and the questions to
  ask before paying anyone
- [**Your first groups**](your-first-groups.md) —
  the lab server end to end: listing
  groups, reading a thread, posting by
  hand, and what a newsreader does
  behind its buttons
- [**Newsgroups and hierarchies**](newsgroups-and-hierarchies.md) —
  how group names are built, the big
  hierarchies, moderated and read-only
  groups, and how new groups appear
- [**Binaries and NZB**](binaries-and-nzb.md) —
  why files travel as encoded text,
  yEnc, segments, PAR2 in outline, and
  an NZB file read line by line
- [**Etiquette and safety**](etiquette-and-safety.md) —
  quoting, cross-posting, test groups —
  and the hard facts: posts are
  permanent, your address is public, and
  files from strangers are untrusted
- [**Recipes**](recipes.md) — follow a
  thread by its References, post a proper
  follow-up, share a small file by NZB,
  and check a group for what is new
- [**The neighbours**](the-neighbours.md) —
  mailing lists, web forums, Reddit,
  RSS and chat: what each does that
  Usenet doesn't, and vice versa
- [**Limits**](limits.md) — no centre
  means no edits and no deletes, the
  lab server's own edges, and where
  discussion mostly lives now
- [**Troubleshooting**](troubleshooting.md) —
  every error number the lab provoked,
  the dot that ends a post early, and
  the NZB that would not parse
- [**Glossary**](glossary.md) — the
  terms, collected in one place

## What it doesn't cover

Running a public news server of your
own — feeding it from other servers,
tuning retention, and keeping it within
the law and your provider's terms is a
project of its own; the lab server here
is a teaching tool on a private network.
Getting the most from any one
newsreader's buttons is likewise out —
this guide teaches the protocol every
newsreader shares, so the skills move
with you. And nothing here will help you
find anything in particular to download:
indexers are explained as a piece of the
machine, not reviewed as a directory.

## How to use this guide

Read chapter 1 for the model and
chapter 2 before touching anything —
knowing which part holds what turns
later confusion into a named problem.
Chapter 3 explains what access costs and
why, but you need no account to learn:
chapter 4's lab server is free, local,
and already stocked with test groups.
The lab's transcripts live in
`usenet-lab/transcripts/`; its server is
`usenet-lab/lab_nntp_server.py`, its
clients are `raw_session.py`,
`seed_lab.py`, `read_with_nntplib.py`
and `nzb_round_trip.py`, and its posting
fixtures are the `post-*.txt` files
beside them.

---

## Part of the series

This guide is one of the [For Mere Mortals](https://paulsullivan33-dev.github.io/mere-mortals/) guides: plain-language guides to the tools programmers and makers use.

Related guides:

- [SABnzbd for Mere Mortals](https://paulsullivan33-dev.github.io/sabnzbd-for-mere-mortals/)
- [Sonarr and Radarr for Mere Mortals](https://paulsullivan33-dev.github.io/arr-stack-for-mere-mortals/)
- [Matrix (Synapse) for Mere Mortals](https://paulsullivan33-dev.github.io/matrix-synapse-for-mere-mortals/)

## License

The writing in this guide is licensed under [CC BY 4.0](https://github.com/paulsullivan33-dev/usenet-for-mere-mortals/blob/main/LICENSE). Code examples and lab scripts are licensed under the [MIT License](https://github.com/paulsullivan33-dev/usenet-for-mere-mortals/blob/main/LICENSE-CODE).

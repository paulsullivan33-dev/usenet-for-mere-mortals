# Newsgroups and Hierarchies

The outcome: you can read a group name
the way a regular does — hierarchy
first, topic after — and you know how
groups come to exist, and what the
letters in a group list are telling you.

## Names are addresses

A newsgroup name is a dotted path, read
left to right from the general to the
specific:

```text
rec.crafts.knitting
│   │      └─ the topic itself
│   └─ a branch of the tree
└─ the hierarchy: recreation
```

The lab's groups follow the same rule
in miniature. `lab.knitting` and
`lab.recipes` are topic groups under an
invented local hierarchy, `lab` — the
name a private server might use for
groups that exist only there. Real
servers carry a mixture: the worldwide
hierarchies below, regional ones, and
often local ones of their own.

## The big hierarchies

Eight hierarchies form the historic
core — the "Big 8" — created and pruned
by a public, documented process:

- **comp.** — computers and computing
- **humanities.** — literature, fine
  arts, philosophy
- **misc.** — what fits nowhere else
- **news.** — about Usenet itself:
  announcements, administration, and
  groups for new readers
- **rec.** — recreation: hobbies, games,
  arts, sport
- **sci.** — science and research
- **soc.** — society, cultures, religion
- **talk.** — discussion and debate,
  much of it argumentative by design

Outside the Big 8, the **alt.**
hierarchy is the famous one: anyone may
propose an alt group, creation is
informal, and servers carry whichever
alt groups they please. The result is
broader, stranger, and less curated —
most binary groups live under alt, in
names beginning `alt.binaries.`. Beyond
both sit regional hierarchies named for
places (`de.` for German-language
groups, `uk.` for the United Kingdom,
and hundreds more), company and
university hierarchies, and private ones
like the lab's.

Nothing forces a server to carry a
group. Your provider's list *is* your
Usenet: two readers on different servers
can honestly disagree about whether a
group exists.

## How a group is born

In the Big 8 the documented path is
deliberate: a written proposal, a public
discussion period, a vote or a board
decision, then a **control message** —
a special article that instructs servers
to create the group. Server keepers
choose whether to honour control
messages automatically or review them,
which is why a newborn group appears on
different servers on different days.
Alt groups skip the vote: a control
message and a post in the group-creation
discussion group, and the group lives
wherever keepers accept it.

The lab shows the static end of this
story. Its seven groups are fixed in
the server's configuration — a keeper's
decision, made once — and `LIST ACTIVE`
(t02) is how a reader discovers the
result. Creation on the live network is
described here from documentation; the
lab issued no control messages.

## Moderated and read-only groups

A group's posting flag, the last field
of its `LIST ACTIVE` line, has three
values worth knowing:

- **y** — open: your post goes straight
  in, as every lab post in chapter 4 did
- **m** — moderated: your post is mailed
  to a moderator and appears only if
  approved. Your reader cannot tell the
  difference while posting; the article
  simply arrives later, or never. (The
  lab has no moderated group — the flow
  is described, not run.)
- **n** — no posting: announcements and
  archives, like `lab.archive`, whose
  `440` refusal chapter 4 met.

A moderated group's keepers also carry
its housekeeping: the charter (what is
on-topic), and often a periodic posting
of rules and frequently asked questions.
Reading a group's charter before posting
— usually findable among its pinned or
periodic articles — is the cheapest
etiquette there is, and chapter 7 says
more.

## Finding your groups

You cannot browse the whole network —
a full-service server carries tens of
thousands of groups. In practice:
search the list your reader downloads
(`LIST ACTIVE` plus the descriptions
from `LIST NEWSGROUPS`) for words from
your topic; try the obvious hierarchy
first (a hobby is probably under
`rec.`); and read a group for a while
before posting to it. Lurking — reading
without posting — is not rude. It is
how every regular started.

**Check yourself.** Take three group
names from this chapter and, for each,
name its hierarchy, guess its topic
from the path alone, and say which
posting flag you would want it to have.
Then look at the lab's list in t02 and
find the two flags the lab actually
uses.

# Glossary

**Article** — the unit of Usenet: a
block of headers over a plain-text body,
posted to one or more newsgroups.

**Binary (binaries)** — a file carried
as encoded text inside articles; also
the groups (`alt.binaries.*` and kin)
where such postings live.

**Block account** — a provider plan
selling a fixed quantity of data that
does not expire, instead of a monthly
subscription.

**Cancel message** — a control article
asking servers to delete an earlier
article. Voluntary for servers to
honour, and widely ignored.

**Completion** — the fraction of the
network's articles a given server
actually holds; matters most for
multi-segment files.

**Control message** — a special article
that instructs servers, for example to
create or remove a newsgroup.

**Cross-post** — one article sent to
several groups at once by naming them
all in its `Newsgroups:` header. One
message-id, one conversation.

**Feed** — the stream of articles one
server passes to another; also the
partner servers themselves.

**Header** — one line of an article's
top block (`From:`, `Subject:`, …)
naming a fact about the article.

**Hierarchy** — the first part of a
group name (`rec.`, `alt.`, `lab.`),
the top branch of the naming tree.

**Indexer** — a service that watches
binary groups and catalogues which
articles make up which files; its
records are published as NZB files.

**Message-ID** — an article's unique
name, in angle brackets, assigned when
a server accepts it; valid everywhere,
unlike article numbers.

**Moderated group** — a group whose
posts are reviewed by a moderator
before appearing; posting flag `m`.

**Multipost** — posting the same text
separately to several groups; starts a
separate thread in each. Frowned on —
cross-post instead.

**Newsreader** — the program a person
uses to read and post: Thunderbird,
Pan, slrn, or the lab's scripts.

**NNTP** — Network News Transfer
Protocol, the plain-text conversation
between readers and servers (and,
server to server) defined by RFC 3977.

**NZB** — an XML file listing, per
segment of a file, the message-id of
the article holding it (brackets
removed). A downloader's shopping list.

**Overview** — a server's one-line
summary per article (subject, author,
date, message-id, references, size),
fetched with `OVER` so readers can list
threads cheaply.

**PAR2** — repair data posted alongside
a file, from which a downloader can
reconstruct a limited number of missing
or damaged segments.

**Posting flag** — the last field of a
group's `LIST ACTIVE` line: `y` open,
`m` moderated, `n` no posting.

**Provider** — an organisation running
news servers that the public may read
and post through, usually for a fee.

**References** — the header listing the
message-ids of an article's ancestors;
the chain that makes a thread.

**Retention** — how many days back a
server's copy of a group reaches.

**Segment** — one article-sized piece
of a split file, yEnc-encoded and
labelled in its subject (`[2/3]`).

**Server (news server)** — the program
that stores articles in its spool,
answers readers, and may exchange
articles with peers.

**Spool** — a server's article store;
on the lab server, one folder per
group and one file per article.

**Thread** — an article and all its
descendants by `References:`, drawn by
readers as a tree.

**yEnc** — the encoding that spells
binary bytes as printable characters
for transport inside articles.

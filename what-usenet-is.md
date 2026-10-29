# What Usenet Is

You want to discuss something — a hobby,
a question, a recipe — with strangers
who care about the same thing, without
asking any company for an account or a
page. **Usenet is the oldest working
answer to that want.** It is a network
for exchanging written **articles**,
started in 1980 between two universities
in North Carolina, and still running
today on the same basic design.

The design is the thing to grasp,
because everything else in this guide
is a consequence of it:

**There is no centre.** A website lives
on one company's computers; when they
switch it off, it is gone. Usenet lives
on thousands of independent **news
servers**. Each server keeps its own
copy of the articles it has received.
When you post, you hand your article to
*your* server. Your server passes it to
the servers it exchanges with — its
**feed** partners — and they pass it
onward, copy by copy, until it has
flooded the network. Reading is the
mirror image: you never fetch an article
from "Usenet" itself. You ask your own
server for the copy it already holds.

**The unit is the article.** An article
looks like an email: a block of
**headers** (`From:`, `Subject:`, the
date, and more) over a plain-text body.
Unlike an email it is addressed to a
topic, not a person. Every article
carries a name of its own, the
**message-id**, which is how servers —
and later, downloaders — refer to that
exact article anywhere on the network.
Chapter 4 shows one being minted, and
chapter 6 shows a whole file rebuilt
from nothing but message-ids.

**Topics are newsgroups.** A
**newsgroup** is a named stream of
articles about one subject —
`rec.crafts.knitting`, in the real
network's naming style. Your server
carries the groups it chooses to carry.
You pick a group, your reader shows you
its recent articles and their replies
strung into **threads**, and you read or
answer as you like. Chapter 5 takes the
names apart.

**One network, two lives.** Usenet was
built for discussion, and its text
groups work exactly as described above.
But an article's body is just text, so
with an encoding trick a body can carry
a *file* — a picture, a program, a film —
split across many articles. That second
life, the **binaries**, is why most
people meet Usenet today, and it needs
extra machinery: encoders, repair data,
and NZB files. Chapter 6 covers it
whole, and this guide's lab runs it end
to end.

Two properties follow from the design,
and a new reader should hear both
before posting anything.

First, **a post cannot be taken back.**
Your article is copied to servers you
will never know about, and strangers
keep private archives. A *cancel message*
exists in the protocol, but servers are
free to ignore it and many do. Treat
every post as permanent and public —
chapter 7 returns to this.

Second, **your server is your window.**
Groups your server does not carry do
not exist for you; articles that aged
off its disks are gone from your copy.
Access to a good server is therefore
the one thing Usenet asks of you, and
chapter 3 is about what "good" means.

**Check yourself.** If you can say, in
one sentence each, what a newsgroup is,
what a message-id names, and why there
is no Usenet head office to complain
to, you have the model. The next chapter
names the parts one by one.

# Limits

The outcome of this chapter: you know
where both edges are — what the lab
server leaves out, and what Usenet
itself cannot do no matter whose server
you use.

## The lab server's limits

The lab server is a teaching model, and
its simplifications are deliberate:

- **Fixed groups.** Its seven groups
  are written into its source. It
  understands no control messages and
  creates no groups on request.
- **No feeds.** It exchanges articles
  with nobody. Propagation — the flood
  of chapter 1 — is described, not
  demonstrated: the lab is one window
  with nothing behind it.
- **No accounts, no encryption.** It
  does not ask who you are (`AUTHINFO`
  is not implemented) and speaks plain
  text on port 11119, not NNTP-over-TLS.
  On your own machine that is fine; on
  a network it would not be.
- **No expiry, no moderation queue, no
  killfiles.** Articles live forever in
  its spool; moderated groups and
  reader-side filtering are described in
  chapters 5 and 7 but not implemented.
- **A small command set.** It implements
  the reader commands the chapters use.
  `HDR`, `NEWGROUPS` and `NEWNEWS` get a
  `500`, honestly, instead of a guess.

None of these make the protocol it
speaks any less real — the clients
cannot tell the difference — but a
reader who runs it as a public server
would be running a toy in a storm.

## Usenet's own limits

- **No centre means no undo.** No edit,
  no delete, no recall, no global
  search, no one to appeal to. Chapters
  1 and 7 rest on this; it is the price
  of the design's durability, and it is
  not negotiable after the fact.
- **Abuse rides the same flood.** Spam,
  floods of junk articles, and forged
  posts propagate by exactly the
  machinery that carries the good
  articles. Defences — moderation,
  filters, provider-side cleaning — are
  local and partial, forever.
- **Your window is your server.**
  Groups not carried do not exist for
  you; articles older than retention are
  gone; a segment your provider missed
  is missing. Two readers can hold
  honestly different copies of "the"
  network, and both be right.
- **Binaries are heavy and rented.**
  The binary side works because
  providers spend real money on disks
  and bandwidth, and charge for it. The
  free, centreless feeling of text
  Usenet does not extend there.
- **The conversation moved.** Most text
  discussion that would once have filled
  the Big 8 now happens in forums,
  subreddits, chat rooms and group
  chats. Many groups are quiet, some
  are spam-haunted, and the liveliest
  ones are the well-moderated few. This
  guide teaches Usenet as it is: a
  working, smaller, older network — not
  the world capital of discussion it
  was in 1995.
- **Nothing here vouches for content.**
  The protocol authenticates almost
  nothing. Names in `From:` lines are
  claims, not proofs, and completeness
  checks on files prove integrity of
  the copy, never the honesty of the
  original.

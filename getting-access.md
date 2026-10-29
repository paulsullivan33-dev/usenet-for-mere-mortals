# Getting Access

The outcome of this chapter: you know
what a **provider** sells, which of its
numbers matter, and which questions to
ask before paying — so an advertisement
cannot sell you the wrong one.

You do not need any of this to finish
the guide. Chapter 4's lab server is a
complete, free NNTP server on your own
machine, and everything the protocol
does happens there. Real access matters
when you want the real network: its
groups, its history, and its binaries.

## What a provider is selling

A provider runs big news servers and
lets you read and post through them.
You are buying four things, and adverts
mix them together on purpose. Separate
them:

- **Retention** — how far back the
  server's copy reaches, in days. A file
  posted three years ago is fetchable
  only if your server's retention covers
  three years *and* the article survived
  the whole way. Text groups need far
  less retention than binaries; old
  discussions are small, old binaries are
  enormous.
- **Completion** — what fraction of the
  network's articles actually arrive and
  survive on this server. For a text
  thread, one missing article is an
  annoyance. For a file split into five
  hundred segments, a few missing
  articles can be fatal — repair data
  (chapter 6) covers small losses, not
  large ones.
- **Connections and speed** — how many
  articles you may fetch at once.
  Downloaders open many connections in
  parallel; a cheap plan with two
  connections will feel slow on binaries
  and perfectly fine for reading text.
- **Encryption** — NNTP over TLS,
  usually on port **563** instead of the
  plain-text port **119**. Without it,
  whatever network sits between you and
  the server can see which articles you
  fetch. With it, it cannot. Any provider
  you consider should offer it as
  standard; treat its absence as a
  disqualification.

Two shapes of plan cover most offers. A
**monthly** plan gives unlimited (or
very large) downloads for a flat fee. A
**block account** sells a fixed amount
of data — say a few hundred gigabytes —
that never expires, for readers whose
use is occasional. Neither shape is
better; they fit different habits. This
guide states no prices: it did not sign
up anywhere, and prices change. What
does not change is the arithmetic —
compare plans on retention, completion
and connections first, price last.

## Text-only and free servers

Discussion-only access is far cheaper
to run than binaries, and it shows:
some universities, companies and
hobbyists run **free text servers**,
and a few providers sell text-only
plans for very little. They carry the
discussion groups, keep them for a long
time, and skip the binary groups
entirely. If your interest is reading
and posting in groups like the lab's —
words, not files — a text server is not
a lesser Usenet. It is the original one.

Two cautions apply to free servers in
particular. The keeper's rules are the
law there: posting may be limited, and
abuse gets an account closed, fairly
enough. And a free server can vanish
when its keeper retires — keep your own
copies of anything you write that
matters to you, which chapter 7 argues
is good practice everywhere.

## What happens when you sign up

The documented shape, the same at most
providers: you choose a plan, pay, and
receive a server hostname, a username
and a password. You type those three
into your newsreader (or your
downloader), choose the encrypted port
if offered, and connect. There is no
content to browse on the provider's own
website, because the provider does not
make the content — a point chapter 2
made and marketing works hard to blur.

Before paying, ask the advert:

1. What is the retention, in days, for
   text and for binaries — separately?
2. Is encrypted access (port 563)
   included at this tier?
3. How many simultaneous connections,
   and is there a monthly data cap?
4. Block or monthly — and if monthly,
   what happens to unused months?

**Check yourself.** You are ready for
chapter 4 if you can explain, without
notes, why a five-hundred-segment file
cares about completion while a text
thread mostly does not. Then go and
meet a server that asks nothing of you
at all.

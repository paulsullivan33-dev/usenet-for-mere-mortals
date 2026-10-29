# Writing criteria for this guide

Every "for Mere Mortals" guide is written to the same nine-point
standard, so a reader who trusts one can trust the rest. Here it
is, with the verification notes for this particular guide below.

1. **Fix it first.** Reader outcomes lead, not action items: each
   chapter opens by naming the outcome it delivers, shows a check
   the reader can run to confirm they got it, and a reasonable
   reader finishes able to state what was done, what it means,
   and what to try next.
2. **Plain language.** Short sentences, everyday vocabulary,
   technical terms defined on first use. No slang, and no
   idioms that only make sense in one country — the reader may
   be translating as they go.
3. **No dead ends.** A guide never tells the reader to do
   something it cannot show them how to verify. Every claim a
   reader relies on — an install, a command, an output — is
   something this guide demonstrates or clearly labels
   documented-only below.
4. **Live-verified where it matters.** Procedures are run for
   real in the guide's lab wherever the build machine allows it,
   and the transcripts kept in the repository are the evidence.
   What could not be run is listed honestly below, never
   presented as if it had been.
5. **General audiences.** Nothing in this guide — examples,
   fixtures, names, addresses — is modelled on any particular
   reader or author's real life, network, or organisations.
   The lab's groups are an invented `lab.` hierarchy, its
   people are invented, and their addresses sit in reserved
   example domains (`lab.invalid`, `example.org`, `example.net`).
6. **Standalone.** A reader needs this guide, its lab, and
   nothing else. Where another guide would genuinely help, it
   is pointed to once, by name, and the chapter still completes
   without it.
7. **Honest about limits.** Chapter 10 names what the lab
   server leaves out (fixed groups, no feeds, no accounts or
   TLS, no expiry or moderation, a small command set) and what
   Usenet itself cannot do (no edits or deletes, abuse riding
   the same flood, server-dependent windows, binaries as a
   rented service, and a discussion world that has largely
   moved elsewhere).
8. **The ethics rule is in the text, early.** Chapter 1 states
   the permanence rule before any procedure depends on it —
   a post is copied everywhere and cannot reliably be taken
   back — and chapter 7 gives it a full treatment: sign
   nothing you would not publish, your `From:` address is
   public, other people's addresses are not costumes, and
   files from strangers are untrusted and their legality is
   the reader's own question.
9. **Builds clean.** The site builds with MkDocs in strict mode
   with no warnings, and a fresh reader following the chapters
   in order reaches the stated outcome of each.

## Verification notes for this guide

The build machine is a 2-CPU, 7.7 GB Ubuntu 24.04 sandbox,
shared with other work while the lab ran. The NNTP server at
the centre of the lab was **written for this guide** —
`usenet-lab/lab_nntp_server.py`, a single-file implementation
of the RFC 3977 reader protocol in pure Python 3.12, storing
articles as plain files in a spool folder. Writing the server
was a deliberate choice with a practical push: the sandbox's
package lock was held by another tenant's `apt-get` for the
whole build window, so installing a distribution server
(leafnode or INN) was not available; rather than wait or fake
the transcripts, the lab implemented the protocol itself and
then treated that server as a black box, driving it with two
independent clients — a raw socket script that prints the wire
conversation, and Python's own `nntplib`, the client library
shipped with the language (deprecated in 3.12, removed in
3.13; chapter 11 covers what that means for readers). Every
wire claim in the guide comes from those transcripts, kept in
`usenet-lab/transcripts/`.

Run for real, with transcripts as evidence:

- Server start, the `200` greeting, `CAPABILITIES` (VERSION 2,
  READER, POST, OVER, the LIST family), `DATE`, `HELP`, `QUIT`
  (t00).
- Stocking the server by posting through `nntplib`: four
  articles accepted with `240` replies and server-minted
  message-ids, the knitting reply carrying a `References:`
  header taken from its parent's `240` reply; a post to the
  read-only `lab.archive` refused with `440`; the keeper then
  filing the archive article straight into the spool with the
  server stopped, and the group showing the article after
  restart (t01).
- `LIST ACTIVE` (including the `y`/`n` posting flags),
  `LIST NEWSGROUPS`, `LIST OVERVIEW.FMT`, `LIST ACTIVE.TIMES`,
  `GROUP` (`211` with counts), and `LISTGROUP` (t02).
- Reading with `nntplib`: group list, group entry, overview of
  a two-article thread, and one article fetched whole, as
  `HEAD` only, and as `BODY` only (t03).
- Posting by hand over the raw protocol: the `340` invitation,
  headers, a body line starting with a dot sent dot-stuffed
  and read back whole, the lone-dot terminator, `240` with the
  minted message-id; a cross-post to two groups read back from
  both with the same message-id under different article
  numbers; the same article fetched by message-id with no
  group selected (t04).
- The refusal catalogue, each provoked deliberately: `411`
  unknown group, `423` unknown article number, `430` unknown
  message-id, `440` read-only group, `441` unknown group in a
  post, `441` missing `Subject:` header, `500` unknown
  command, `412` article-by-number with no group selected
  (t05).
- Pointer walking: `STAT`, `NEXT`, `LAST`, and `421` at the
  group's end; fetching by message-id while the pointer sat on
  another article, with `STAT` afterwards proving the pointer
  did not move; `OVER` for a range and `XOVER` returning
  identical lines for the same article, the overview's
  References field populated for the reply and empty for its
  parent (t06).
- The binary circuit, end to end: a 900-byte file split into
  three 300-byte segments, each yEnc-encoded by the lab's own
  codec and posted to `lab.binaries`; an NZB written naming
  the three message-ids (brackets off, poster address
  XML-escaped); a fetcher that read only the NZB, retrieved
  each segment by message-id, verified each part's CRC32 from
  its `=yend` line, decoded and joined them — SHA-256 of the
  rebuilt file identical to the original (t07). A segment
  article as stored and served, `=ybegin`/`=ypart`/`=yend`
  framing visible (t08), and the spool's folder layout behind
  all of it (t08).
- Two genuine failures along the way, kept and used rather
  than hidden: the lab's first NZB was rejected by the XML
  parser for an unescaped `<` in the poster attribute (fixed
  by escaping; chapter 6 shows the escaped form and chapter 11
  the diagnosis), and starting the server twice produced
  `Address already in use` from the forgotten first copy
  (chapter 11).

Documented only — described from documentation and the
protocol standards, not run, and the text does not claim
otherwise:

- Commercial providers end to end: signing up, paying, plan
  shapes as currently sold, and all prices. No account was
  opened; no price is stated anywhere in this guide.
- The live network: posting to real groups, propagation
  between real servers by feed, control messages creating a
  group, and honouring (or ignoring) of cancel messages. The
  lab is one server with no peers, so the flood is explained,
  not shown.
- Graphical and terminal newsreaders on screen (Thunderbird,
  Pan, slrn) and their per-program settings; the guide teaches
  the protocol they all speak.
- NNTP over TLS (port 563), `AUTHINFO` sign-in, and
  moderated-group approval flow (`m` flag) — none implemented
  by the lab server; the flags and ports are taught from the
  standards.
- PAR2 repair performed on a damaged download (the mechanism
  is explained; the series' SABnzbd guide performs a real
  repair), real indexer services and their accounts, and
  retention or completion measured on production servers.
- Leafnode and INN as installable servers, for the reason
  given above; the lab server stands in for them at the
  protocol level only.

Fixtures are this guide's own and deliberately generic: an
invented `lab.` hierarchy (announce, general, knitting,
recipes, binaries, test, archive), three invented people —
a server keeper, a knitter, a cook — at reserved example
addresses, a knitting question, a bread recipe, and a small
patterned binary file generated byte by byte. No real group,
person, organisation or event appears anywhere in the lab.

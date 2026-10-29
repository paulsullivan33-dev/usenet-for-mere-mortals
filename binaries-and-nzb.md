# Binaries and NZB

The outcome: you can follow a file's
whole journey — sliced, encoded, posted,
catalogued, fetched, rebuilt — and you
can read an NZB file and say exactly
what a downloader will do with it. The
lab ran this journey end to end; its
receipt is a checksum that matched.

## Why a file cannot travel as itself

Usenet articles were designed for text.
The early network moved 7-bit
characters, and some links still mangle
long lines or control characters. A
program or a picture is **binary** data
— all 256 byte values, including ones
that mean "end of line" and "end of
article" to the machinery. Posted raw,
it would arrive corrupted or truncated.
So binary posting begins with an
**encoding**: a scheme that spells
binary bytes using only safe, printable
characters, at some cost in size.

The encoding Usenet settled on is
**yEnc**. In brief: add 42 to each byte,
and when the result lands on a character
that would confuse the transport, write
it as an escape — an `=` followed by a
second character. Lines are kept short.
An encoded segment travels wrapped in
markers, and transcript t08 shows one
as it actually sits on a server:

```text
From: Sam Keeper <sam@lab.invalid>
Subject: harbour-chart.bin [1/3]
…
=ybegin part=1 line=128 size=900 name=harbour-chart.bin
=ypart begin=1 end=300
<128-character lines of encoded bytes>
=yend size=300 part=1 pcrc32=…
```

`=ybegin` names the file and its total
size; `=ypart` says which bytes of the
file this segment holds; `=yend` closes
with the segment's size and a **CRC**
checksum, so a downloader can verify
this piece before assembling anything.

## Segments, subjects and missing pieces

One article is a poor container for a
large file, so posters split files into
**segments** — the lab used 300-byte
pieces of a 900-byte file; real postings
use pieces of a few hundred kilobytes
and files of many gigabytes. Each
segment is its own article, and the
subject line carries the bookkeeping:
`harbour-chart.bin [1/3]` is segment 1
of 3. A downloader that finds all the
segments can rebuild the file. One that
finds two of three cannot — which is
why posters also post **PAR2** files:
repair data, computed from the file,
from which a downloader can reconstruct
a limited number of missing or damaged
segments. PAR2 is described here, not
run; the series' SABnzbd guide performs
a real repair against a real download.

## The NZB: a map made of message-ids

Hunting segments group by group is
slow, and retention makes it unreliable.
The **indexer** solves it (chapter 2):
it watches binary groups and records,
for each file, the message-id of every
segment. Its record is published as an
**NZB** — an XML shopping list. Here is
the lab's, complete (t07):

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE nzb PUBLIC "-//newzBin//DTD NZB 2.0//EN" "http://www.newzbin.com/DTD/nzb/nzb-2.0.dtd">
<nzb xmlns="http://www.newzbin.com/DTD/2003/nzb">
  <file poster="Sam Keeper &lt;sam@lab.invalid&gt;" date="1759000000" subject="harbour-chart.bin [3/3]">
    <groups>
      <group>lab.binaries</group>
    </groups>
    <segments>
      <segment bytes="426" number="1">lab-1793303697-6@lab.invalid</segment>
      <segment bytes="431" number="2">lab-1793303697-7@lab.invalid</segment>
      <segment bytes="429" number="3">lab-1793303697-8@lab.invalid</segment>
    </segments>
  </file>
</nzb>
```

Read it as a downloader does:

- `<file>` names the prize: who posted
  it, the subject the segments share.
  The poster's address appears with its
  angle brackets escaped (`&lt;`) —
  because this is XML, a raw `<` inside
  an attribute is illegal. The lab's
  first NZB draft forgot this, the file
  would not parse at all, and the fix is
  the escaped text you see. Real NZBs
  carry the same escaping.
- `<groups>` says where the segments
  were posted — a downloader may need it
  for some servers, though the ids alone
  are enough on most.
- Each `<segment>` gives a byte count,
  the segment's order, and — the entire
  point — a **message-id with its angle
  brackets removed**. That is the NZB
  convention, and the mirror image of
  the wire, where ids always wear their
  brackets. A fetcher wraps each one
  back up and asks the server for
  `ARTICLE <that-id>` — the by-id fetch
  chapter 4 proved never moves your
  place in a group, because a downloader
  has no place to keep.

## The round trip

The lab's fetcher (t07) read only the
NZB — the original file was set aside —
fetched the three articles by id,
checked each segment's CRC as it
decoded, joined them in segment order,
and compared hashes:

```text
sha256 of the original: 4544d9aaef92b51c…
sha256 of the rebuilt file: 4544d9aaef92b51c…
MATCH
```

That is the whole binary economy in
miniature, and it is exactly a real
downloader's job description — fetch by
id, verify, decode, join — plus the two
things the lab's perfect little network
did not need: PAR2 repair when a
segment is missing, and unpacking when
the joined file is itself an archive.
Both are SABnzbd's daily work, covered
live in its guide.

**Check yourself.** Look at the NZB
above and answer without scrolling: how
many articles will a downloader fetch,
from which group, in what order will it
join them, and how will it know the
join is right? If the four answers come
easily, this chapter did its work.

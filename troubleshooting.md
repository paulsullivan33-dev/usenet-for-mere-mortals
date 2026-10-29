# Troubleshooting

Every problem here was met in the lab
or follows directly from behaviour the
transcripts show. Server replies are
quoted exactly; where servers differ in
wording, the number is the stable part.

## The reply codes, in one place

From transcript t05 (and friends), the
refusals an ordinary reader can earn:

| Reply | Meaning | Usual cause |
|---|---|---|
| `411` | No such newsgroup | The name is misspelled, or your server does not carry it |
| `412` | No newsgroup selected | `ARTICLE`/`OVER`/`STAT` by number before any `GROUP` |
| `420` | No current article | `NEXT`/`OVER` with no pointer set — enter a group first |
| `421` | No next article | You are on the group's last article; not an error in your reader |
| `423` | No such article number | The number is beyond the group's end, or the article expired |
| `430` | No such article found | A message-id the server has never seen, or has expired |
| `440` | Posting not allowed | The group is read-only (`n` flag), or the server forbids posting |
| `441` | Posting failed | Headers missing (`From:`, `Subject:`, `Newsgroups:`), or a named group is unknown |
| `500` | Command not recognised | A typo, or a command this server does not implement |

Chapter 4's happy path is the same
table's other side: `200` greeting,
`211` group entered, `220`–`224` the
fetches, `240` post accepted, `340`
"send it", `205` goodbye.

## "Address already in use" when the server starts

The port is still held — almost always
by your own earlier copy of the server,
still running in a forgotten terminal.
The lab met this while restarting
between transcripts. Find the listener
(`ss -tlnp | grep 11119`), stop that
process, then start yours. Starting a
second server "to be sure" only deepens
the confusion about which spool is
being served.

## A post ends early, or a line vanishes

The single dot ends a post — and a
multi-line reply. If a body line of
your article is exactly `.`, everything
after it is never sent, and the server
may then answer your remaining lines as
if they were commands (expect a baffled
`500` or two). The cure is the one t04
shows: clients **dot-stuff**, doubling
any leading dot; if you post by hand and
your client does not, double the dots
yourself. The mirror-image symptom — a
body line arriving with one dot too
many — is a client or server somewhere
failing to *undo* the stuffing.

## The NZB will not parse

The lab's first NZB failed exactly
here: an XML parser rejected it, "not
well-formed", pointing at the `poster=`
attribute — the address inside it held
raw `<` and `>` characters, which XML
forbids in attribute values. Poster
addresses must be escaped (`&lt;`,
`&gt;`) or the brackets left out. When
a downloader calls a real NZB corrupt,
open it in a text editor and look at
the `<file>` line first: unescaped
addresses there are the classic cause,
and the error is the *file's*, not your
downloader's.

## A segment's CRC does not match

The `=yend` line of each segment
carries a CRC of that piece (chapter
6). A mismatch means the bytes that
arrived are not the bytes that were
posted — transport damage, or a mangled
fetch. Refetch that one article by its
message-id before blaming the whole
file; if the same segment keeps
failing, check whether a second copy
exists (some files are posted more than
once), and let PAR2 cover it if repair
data came with the posting. If every
segment fails its CRC, suspect the
decoder, not the network — your yEnc
handling is disagreeing with the
poster's, and a different tool is the
quickest test.

## Articles a friend can see and you cannot

Same group, same subject, missing on
your server: that is chapter 3's
**completion** and retention, not a
bug. Your server never received the
article, or aged it out. There is no
command that summons an article a
server does not hold — `430` is the
honest answer (t05). The practical
moves are a second provider on a
different feed, or waiting for a repost;
complaining to your own server's keeper
is the third, and sometimes works.

## The DeprecationWarning from the client scripts

Python 3.12 warns that its `nntplib`
module is deprecated; the module is
removed in Python 3.13. The lab's
scripts silence the warning where they
import it, and the guide says plainly:
on a newer Python, run the reading
chapters through `raw_session.py`
instead — the protocol it speaks is not
deprecated at all, and everything it
shows is the same conversation the
library was having on your behalf.

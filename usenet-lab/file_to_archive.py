#!/usr/bin/env python3
"""file_to_archive.py -- the keeper files an article into lab.archive.

lab.archive is read-only: the server refuses POSTs to it with a
440 reply (seed_lab.py demonstrates). Archives are not written
by posters; they are written by whoever keeps the server. This
tool does the keeper's version of the job -- it hands the
article straight to the spool, the server's own store, using
the same code the server uses, while the server is stopped.

Usage:

  python3 file_to_archive.py ARTICLE_FILE SPOOL_DIR

The article must carry From:, Subject: and Newsgroups: headers
naming lab.archive; the spool adds Date: and Message-ID: if
they are missing, exactly as it does for a posted article.
Restart the server afterwards so it re-reads its spool.
"""

import sys

from lab_nntp_server import Spool


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    article_file, spool_dir = sys.argv[1], sys.argv[2]
    with open(article_file, "rb") as fh:
        raw = fh.read()
    spool = Spool(spool_dir)
    msgid = spool.post(raw, ["lab.archive"])
    print("filed into lab.archive as", msgid)
    return 0


if __name__ == "__main__":
    sys.exit(main())

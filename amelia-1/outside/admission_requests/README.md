# OUTSIDE-2 admission requests (batch casts)

From W020, a request commit in this folder starts the **OUTSIDE-2 queue runner**
(`.github/workflows/outside2-queue.yml`). The request commit may be made directly by the
querent or by a connected assistant acting on the querent's explicit instruction. In either
case, the physical 32-toss cast remains the querent's act; Git history records the repository
commit separately from the physical act.

When a connected assistant submits the file, include a comment such as:

    # submission: assistant-initiated repository commit on querent instruction

The queue records the request file, line and source Git commit in the admission receipt.

## Format

A plain-text file, for example `batch-2026-10-07.txt`, one working per line:

    # OUTSIDE-2 casts, 7 October 2026
    # submission: assistant-initiated repository commit on querent instruction
    W020 T H T T H H T H T T T H H T H T H H T T H T T H H H T T H T H T
    W021 HTTTHHTHTHHTTTHHHTHTHTTHHTHTHTTH

- Each line is a working id and exactly 32 tosses, H or T. Spaces between tosses are fine.
- `#` starts a comment.
- Hold the registered question for each cast as you make it: *what is the scene that will be
  shown at the close of this working?*
- Number workings consecutively from the next one in the ledger.

## Rules

- Each physical cast is made once and admitted once. Never replace a committed cast. An identical
  duplicate request is harmless; a conflicting request for the same working halts before admission.
- Every valid cast committed here is binding when its turn arrives; none may be discarded because
  of its later target or reading.
- A run handles at most 20 workings. Additional queued requests remain committed for a later run.
- Do not submit another batch while a queue run is actively changing the ledger unless you intend
  it to wait for the next serialized run.
- If a run halts, its `INCIDENT_<run>.json` records the reason. A later request-folder commit
  resumes the queue. An already admitted unresolved working is always handled before any new cast.
- Do not admit or resolve workings by hand while the queue runner is active.

For W020 onward the queue creates and verifies its own RFC 3161 evidence. Its internal pushes use
GitHub's workflow token, so GitHub intentionally suppresses recursive triggering of the older
push-capture workflow. This is expected; the queue's own timestamp and receipt files are the timing
evidence for queued workings.

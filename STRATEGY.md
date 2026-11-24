# Strategy — "The Funniest Out-of-Office" (judged text)

## Exact deliverable
A single line of text written by the root entrypoint to `/output/entry.txt`:
one out-of-office auto-reply, nothing else. No image, no link, no second
line, no text addressed to the judge. The line chosen is:

    I'm out of office. I'll be in touch the moment I need something from you.

Runtime: python3.13. Entrypoint: `/main.py` at the repository root,
standard library only, no network, no reading of files outside the repo,
no environment secrets.

## Hard caps (from competition.yaml / RULES.txt)
- Gate: `/output/entry.txt` must be UTF-8 text, 1..140 characters,
  not only white space. Invalid = Valid 0, no judge, no prize.
- One line only; no trailing newline in the written bytes.
- Sandbox: 1 CPU, 512 MB, 64 pids, 60 s wall budget per run; no network.
- The program must ship everything it runs in the repository.
- `MAKEFUN_OUTPUT_DIR` may stand in for `/output` locally; the grader
  uses the `/output` mount. Both resolve to the same artifact path.
- At most 5 submissions per UTC day; blind rounds, 3 judged rounds;
  top 500 on the dev board enter the final heat; 8 places paid.

## Scoring — the judge criteria, in the exact order the rubric lists them
The judge is `z-ai/glm-5.3-flash` (superbot, reasoning high), shown two
entries at a time in both orders. It must go through these in order and
let the first difference decide unless a later one differs by much more:

1. Is it a one-line out-of-office reply a real person would set and send,
   and does it beat any funnier one-line OOO reply? (gate-like, most important)
2. Genuine surprise — a twist the reader does not see coming.
3. A person's own voice, not a template.
4. Fresh — avoids jokes already read in a thousand inboxes.
5. Every word earns its place; nothing cuttable.

A call scores the winner 0.5 + 0.1*margin (0.6..1.0), the loser the rest;
a game is the mean of both orders. Final rank is a Bradley-Terry rate;
playoff finalists rank above non-finalists, then higher rate, then more
playoff wins, then smaller text, then earlier receipt.

## Rival research (public feed + web)
The bounty's own feed is hidden during blind rounds
(`/api/.../rounds/board` -> `board: hidden`, `judged: 0`, `entries: []`),
so no rival text was visible and none was copied. Web research showed the
crowded, low-value clichés to avoid: "404 employee not found", robot / AI
persona auto-replies, Rick Astley, "each sender gets one email then I
randomly delete", "call my wife in an emergency", "I'm not really out of
the office, I'm just ignoring you", "contact Dave (also on holiday)",
and travel-brag / resignation jokes. A sibling contest asks for an *AI*
agent's OOO; this one asks for a *real person's*. That is the opening.

## Why this line, mapped to the rubric
1. Real OOO: opens with the plain fact "I'm out of office." A weary
   colleague could really set it; no bot/404/AI gimmick, no meta-text.
2. Surprise: an OOO promises a reply on return; this one replays "be in
   touch" only when the sender wants something. The expected promise is
   swapped for a blunt workplace truth at the last clause.
3. Voice: dry, slightly sheepish, unmistakably one person, not a template.
4. Fresh: the transactional punchline is not among the stock OOO jokes
   above, and it deliberately avoids the AI-persona lane of rival entries.
5. Economy: 72 characters, one idea, one pivot; every word sets up or
   delivers the turn. No return date or contact is invented, so nothing
   can be cut without losing the laugh.

## Concrete plan to maximize the score
1. Freeze the line; do not improvise a different one at write time.
2. Write `main.py` (v1): constant entry text, UTF-8 encode, local length
   check, atomic write to the artifact via temp file + `os.replace`.
3. In a separate later step, rewrite that *same* `main.py` (v2) with a
   real compliance improvement: explicit single-line/BOM rejection,
   sibling-directory temp file plus `fsync`, post-write byte-for-byte
   readback verification, `MAKEFUN_OUTPUT_DIR`/`/output` support, and a
   clear stdout diagnostic (chars, bytes, sha256).
4. Exercise the final entrypoint locally with `MAKEFUN_OUTPUT_DIR` set to
   a scratch directory. Verify: exit 0, exact bytes, 1..140 code points,
   UTF-8 decodes, no `\n`/`\r`, no trailing newline, single line, the
   artifact matches the frozen line, and reruns are identical.
5. Keep the makefun root/freshness and LICENSE commits intact; commit
   STRATEGY.md, main.py and any helper files with git; print final sha.
6. Do NOT submit or upload anything.

## What a win would look like
A decisive win (margin 4-5) in both orders against the house anchors and
rungs, a top-10 Swiss finish, and a playoff berth. If the reward is not
actually credited or claimable, report GAGAL plainly.

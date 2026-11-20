# makefun-news-image-20261119

One image that sums up the world news of Thursday, 19 November 2026.

## The image

A code-drawn broadsheet front page (`entry.png`, 1024x1024): masthead
"THE WORLD TODAY", the date in large red type, a symbolic hero panel
(globe, scales of justice, Shenzhen skyline), six story blocks, and a
markets-and-briefs strip. Every letter is drawn by code with PIL, so no
text can garble.

Stories covered: the World Court genocide ruling on Myanmar; the Trump,
Putin and Xi trilateral in Shenzhen; Anthropic's record $81.34 billion
IPO; Israel's Gaza ground operation; Russian strikes on Ukraine and the
EU's proposed €25 billion loan; Denmark's approval of the Greenland–U.S.
security pact.

## The program

`main.py` (Python 3.13, standard library only) copies `entry.png` to
`$MAKEFUN_OUTPUT_DIR` (or `/output`) as `entry.png`. Deterministic by
construction: the output is a byte-for-byte copy of the file in this repo.

## Run

```
MAKEFUN_OUTPUT_DIR=/tmp/out python3 main.py
```

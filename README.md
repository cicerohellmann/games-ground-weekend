# Games Ground Weekend Map

Unofficial, fan-made live map for the **Games Ground 2026 public days**:
Sat 7 and Sun 8 November 2026, Alte Münze, Berlin.

Live page: https://cicerohellmann.github.io/games-ground-weekend/

- Floor plan traced by hand from the venue sign; stages light up while an event runs.
- Time slots for both days, a timeline slider, picks, search and filters.
- Each event has a short "If you like: …" line (written for this map, not official).
- German-only events and age limits are marked.
- Lichthof and Loft Breakout are not on the traced plan: ask at the info point.

## Source

All program facts come from the official pages, read on 7 Nov 2026:

- https://www.gamesground.de/programme/saturday
- https://www.gamesground.de/programme/sunday

Always check the official program for changes.

## Update the program

```sh
curl -s https://www.gamesground.de/programme/saturday -o /tmp/sat.html
curl -s https://www.gamesground.de/programme/sunday   -o /tmp/sun.html
python3 tools/parse_programme.py /tmp/sat.html /tmp/sun.html /tmp/raw.json
python3 tools/build_data.py /tmp/raw.json data/programme.json
python3 tools/build.py        # writes index.html from src/template.html
```

The page is one self-contained `index.html`, copied from the
[devcon-map](https://github.com/cicerohellmann/devcon-map) app.

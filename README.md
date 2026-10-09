# Waffle math

Three brunch-planning calculators as a small static site - exact arithmetic,
every borrowed number labeled:

- **Batter for a crowd** - servings and style (buttermilk waffle / belgian /
  crepe / pancake) become eggs, flour, liquid and butter. Eggs round to whole
  eggs first and everything else scales with them; the drift is shown.
- **Iron shift** - servings, style and iron count become piece count, rounds
  and wall-clock minutes, with a session band.
- **Rest and hold** - style and minutes until serving become the verdict:
  under-rested, mix now, or mix later.

## Files

- `index.html` - landing page
- `app.html` - the three calculators
- `engine.js` - all arithmetic, shared by the page and the tests
- `oracle.py` - independent Python mirror of the engine; regenerates `expected.json`
- `expected.json` - 57 cases (per-card values plus error cases)
- `test.js` - runs the engine against `expected.json` (node test.js)

## Tests

```
python3 oracle.py   # regenerate expected cases
node test.js        # engine vs oracle
```

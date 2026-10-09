/* Waffle math - exact arithmetic, labeled kitchen norms.
   Labeled norms shown in the UI: per-serving batter ratios by style
   (buttermilk waffle 60g flour / 95g liquid / 0.5 egg / 15g butter;
    belgian 70/100/0.75/20; crepe 40/100/0.5/8 x3 pieces; pancake 60/90/0.5/10 x3 pieces),
   egg weight 50 g, iron minutes per piece (4/5/2/3), rest and hold windows
   (waffle 10/30, belgian 30/20, crepe 60/120, pancake 5/45 minutes). */
(function (root) {
  'use strict';

  var EGG_G = 50;
  var STYLES = {
    waffle:  { flour: 60, liquid: 95, egg: 0.5,  butter: 15, pieces: 1, min_per: 4, rest: 10, hold: 30 },
    belgian: { flour: 70, liquid: 100, egg: 0.75, butter: 20, pieces: 1, min_per: 5, rest: 30, hold: 20 },
    crepe:   { flour: 40, liquid: 100, egg: 0.5,  butter: 8,  pieces: 3, min_per: 2, rest: 60, hold: 120 },
    pancake: { flour: 60, liquid: 90, egg: 0.5,  butter: 10, pieces: 3, min_per: 3, rest: 5,  hold: 45 }
  };

  function styleOf(style) {
    var s = STYLES[String(style).toLowerCase()];
    if (!s) throw new Error('style is waffle, belgian, crepe or pancake (labeled)');
    return s;
  }
  function num(v, name) {
    if (typeof v !== 'number' || !isFinite(v)) throw new Error(name + ' must be a number');
    return v;
  }

  function batterPlan(servings, style) {
    servings = num(servings, 'servings');
    if (!Number.isInteger(servings)) throw new Error('count servings in whole people');
    if (servings <= 0) throw new Error('servings must be positive');
    if (servings > 48) throw new Error('keep it under 48 servings (labeled)');
    var s = styleOf(style);
    var eggsRaw = servings * s.egg;
    var eggs = Math.max(1, Math.round(eggsRaw));
    var k = eggs / eggsRaw;
    var flour = Math.round(s.flour * servings * k);
    var liquid = Math.round(s.liquid * servings * k);
    var butter = Math.round(s.butter * servings * k);
    var eggG = eggs * EGG_G;
    var verdict = servings < 4 ? 'a quiet breakfast' : servings < 10 ? 'a family brunch' : 'a full brunch shift';
    return {
      eggs: eggs, flour_g: flour, liquid_g: liquid, butter_g: butter,
      batter_g: flour + liquid + butter + eggG,
      drift_pct: Math.round((k - 1) * 1000) / 10,
      verdict: verdict
    };
  }

  function ironShift(servings, style, irons) {
    servings = num(servings, 'servings');
    irons = num(irons, 'irons');
    if (!Number.isInteger(servings)) throw new Error('count servings in whole people');
    if (servings <= 0) throw new Error('servings must be positive');
    if (servings > 48) throw new Error('keep it under 48 servings (labeled)');
    if (!Number.isInteger(irons)) throw new Error('count irons in whole irons');
    if (irons <= 0) throw new Error('irons must be positive');
    if (irons > 8) throw new Error('keep it under 8 irons (labeled)');
    var s = styleOf(style);
    var pieces = servings * s.pieces;
    var rounds = Math.ceil(pieces / irons);
    var wall = rounds * s.min_per;
    var verdict = wall < 20 ? 'a quick breakfast' : wall < 45 ? 'a brunch shift' : 'a marathon - borrow an iron';
    return { pieces: pieces, rounds: rounds, wall_min: wall, verdict: verdict };
  }

  function restWindow(style, waitMin) {
    waitMin = num(waitMin, 'minutes until serving');
    if (!Number.isInteger(waitMin)) throw new Error('count minutes in whole minutes');
    if (waitMin < 0) throw new Error('minutes until serving must be zero or more');
    if (waitMin > 720) throw new Error('keep it under 12 hours (labeled)');
    var s = styleOf(style);
    var verdict = waitMin < s.rest ? 'too soon - the batter is under-rested'
      : waitMin <= s.rest + s.hold ? 'mix now - the rest window fits'
      : 'too early - mix closer to serving';
    return { rest_min: s.rest, hold_min: s.hold, verdict: verdict };
  }

  var api = { batterPlan: batterPlan, ironShift: ironShift, restWindow: restWindow };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  root.WaffleMath = api;
})(typeof window !== 'undefined' ? window : globalThis);

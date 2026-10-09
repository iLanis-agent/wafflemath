#!/usr/bin/env python3
# Oracle for wafflemath. Mirrors engine.js float ops exactly (IEEE 754 doubles).
import math, json, os

EGG_G = 50
STYLES = {
  'waffle':  (60, 95, 0.5, 15, 1, 4, 10, 30),
  'belgian': (70, 100, 0.75, 20, 1, 5, 30, 20),
  'crepe':   (40, 100, 0.5, 8, 3, 2, 60, 120),
  'pancake': (60, 90, 0.5, 10, 3, 3, 5, 45),
}

def jround(x):  # JS Math.round for positive magnitudes
    return math.floor(x + 0.5)

def batterPlan(servings, style):
    f, l, e, b, _, _, _, _ = STYLES[style]
    eggsRaw = servings * e
    eggs = max(1, jround(eggsRaw))
    k = eggs / eggsRaw
    flour = jround(f * servings * k)
    liquid = jround(l * servings * k)
    butter = jround(b * servings * k)
    verdict = 'a quiet breakfast' if servings < 4 else 'a family brunch' if servings < 10 else 'a full brunch shift'
    return {'eggs': eggs, 'flour_g': flour, 'liquid_g': liquid, 'butter_g': butter,
            'batter_g': flour + liquid + butter + eggs * EGG_G,
            'drift_pct': jround((k - 1) * 1000) / 10, 'verdict': verdict}

def ironShift(servings, style, irons):
    _, _, _, _, p, m, _, _ = STYLES[style]
    pieces = servings * p
    rounds = math.ceil(pieces / irons)
    wall = rounds * m
    verdict = 'a quick breakfast' if wall < 20 else 'a brunch shift' if wall < 45 else 'a marathon - borrow an iron'
    return {'pieces': pieces, 'rounds': rounds, 'wall_min': wall, 'verdict': verdict}

def restWindow(style, waitMin):
    _, _, _, _, _, _, r, h = STYLES[style]
    verdict = 'too soon - the batter is under-rested' if waitMin < r else \
              'mix now - the rest window fits' if waitMin <= r + h else \
              'too early - mix closer to serving'
    return {'rest_min': r, 'hold_min': h, 'verdict': verdict}

FUN = {'batterPlan': batterPlan, 'ironShift': ironShift, 'restWindow': restWindow}

CASES = [
  {'card':'batterPlan','args':[2,'waffle']},  {'card':'batterPlan','args':[6,'waffle']},
  {'card':'batterPlan','args':[12,'waffle']}, {'card':'batterPlan','args':[48,'waffle']},
  {'card':'batterPlan','args':[3,'waffle']},  {'card':'batterPlan','args':[1,'belgian']},
  {'card':'batterPlan','args':[4,'belgian']}, {'card':'batterPlan','args':[9,'belgian']},
  {'card':'batterPlan','args':[24,'belgian']},{'card':'batterPlan','args':[3,'crepe']},
  {'card':'batterPlan','args':[8,'crepe']},   {'card':'batterPlan','args':[16,'crepe']},
  {'card':'batterPlan','args':[2,'crepe']},   {'card':'batterPlan','args':[5,'pancake']},
  {'card':'batterPlan','args':[10,'pancake']},{'card':'batterPlan','args':[7,'pancake']},
  {'card':'batterPlan','args':[1,'pancake']},
  {'card':'batterPlan','args':[0,'waffle'],'error':'positive'},
  {'card':'batterPlan','args':[-3,'waffle'],'error':'positive'},
  {'card':'batterPlan','args':[2.5,'waffle'],'error':'whole people'},
  {'card':'batterPlan','args':[60,'waffle'],'error':'under 48'},
  {'card':'batterPlan','args':[4,'galette'],'error':'style is'},
  {'card':'ironShift','args':[6,'waffle',1]},  {'card':'ironShift','args':[6,'waffle',2]},
  {'card':'ironShift','args':[12,'waffle',2]}, {'card':'ironShift','args':[48,'waffle',3]},
  {'card':'ironShift','args':[4,'belgian',1]}, {'card':'ironShift','args':[10,'belgian',2]},
  {'card':'ironShift','args':[8,'crepe',1]},   {'card':'ironShift','args':[8,'crepe',2]},
  {'card':'ironShift','args':[24,'crepe',3]},  {'card':'ironShift','args':[5,'pancake',1]},
  {'card':'ironShift','args':[10,'pancake',2]},{'card':'ironShift','args':[16,'pancake',1]},
  {'card':'ironShift','args':[3,'waffle',8]},  {'card':'ironShift','args':[20,'belgian',4]},
  {'card':'ironShift','args':[0,'waffle',1],'error':'positive'},
  {'card':'ironShift','args':[4,'waffle',0],'error':'positive'},
  {'card':'ironShift','args':[4,'waffle',2.5],'error':'whole irons'},
  {'card':'ironShift','args':[4,'waffle',9],'error':'under 8'},
  {'card':'ironShift','args':[4,'galette',1],'error':'style is'},
  {'card':'restWindow','args':['waffle',5]},   {'card':'restWindow','args':['waffle',10]},
  {'card':'restWindow','args':['waffle',40]},  {'card':'restWindow','args':['waffle',41]},
  {'card':'restWindow','args':['belgian',45]}, {'card':'restWindow','args':['belgian',50]},
  {'card':'restWindow','args':['belgian',51]}, {'card':'restWindow','args':['crepe',30]},
  {'card':'restWindow','args':['crepe',180]},  {'card':'restWindow','args':['crepe',181]},
  {'card':'restWindow','args':['pancake',0]},  {'card':'restWindow','args':['pancake',50]},
  {'card':'restWindow','args':['pancake',51]},
  {'card':'restWindow','args':['waffle',-5],'error':'zero or more'},
  {'card':'restWindow','args':['waffle',800],'error':'under 12 hours'},
  {'card':'restWindow','args':['galette',30],'error':'style is'},
]

out = []
for c in CASES:
    row = dict(c)
    if 'error' not in c:
        row['expect'] = FUN[c['card']](*c['args'])
    out.append(row)
path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'expected.json')
with open(path, 'w') as fh:
    json.dump(out, fh, indent=1)
    fh.write('\n')
print(len(out), 'cases written')

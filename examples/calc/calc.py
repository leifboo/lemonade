
from lemonade.main import main as lemonade

# generate our grammar
try:
    lemonade(("lemonade", "gram.y"))
except SystemExit:
    pass

# import it
from gram import *

import re, sys


tokenCode = {
    '+': PLUS,
    '-': MINUS,
    '/': DIVIDE,
    '*': TIMES,
    }


tokens = re.split(" ?([+-/*]) ?", sys.argv[1])
print tokens

p = Parser()
for t in tokens:
    yymajor = tokenCode.get(t)
    if yymajor is None:
        yymajor = NUM
        yyminor = float(t)
    else:
        yyminor = None
    p.parse(yymajor, yyminor)
p.parse(0, None)


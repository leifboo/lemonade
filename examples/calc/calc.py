
import sys

from lemonade.main import main as lemonade

# generate our grammar
try:
    lemonade(["lemonade", "-q", "gram.y"])
except SystemExit:
    pass

# import it
from gram import *


#
# the lexer
#

tokenType = {
    '+': PLUS,
    '-': MINUS,
    '/': DIVIDE,
    '*': TIMES,
    }

def tokenize(input):
    import re
    tokenText = re.split("([+-/*])|\s*", input)
    for text in tokenText:
        if text is None:
            continue
        type = tokenType.get(text)
        if type is None:
            type = NUM
            value = float(text)
        else:
            value = None
        yield (type, value)
    return


#
# the delegate
#

class Delegate(object):

    def accept(self):
        return

    def parse_failed(self):
        assert False, "Giving up.  Parser is hopelessly lost..."

    def syntax_error(self, token):
        print >>sys.stderr, "Syntax error!"
        return



p = Parser(Delegate())
#p.trace(sys.stdout, "# ")
p.parse(tokenize(sys.argv[1]))


'''
Main program file for the LEMON parser generator.
'''

from build import *
from parse import *
from report import *
from struct import *

from ccruft import printf
from sys import stderr, exit
from optparse import OptionParser


def main(argv):
    '''The main program.  Parse the command line and do it...'''

    parser = OptionParser(usage="%prog [options] FILE")
    parser.add_option("-b",
                      action="store_true", dest='basisflag', default=False,
                      help="print only the basis in report")
    parser.add_option("-c",
                      action="store_true", dest='compress', default=False,
                      help="don't compress the action table")
    parser.add_option("-g",
                      action="store_true", dest='rpflag', default=False,
                      help="print grammar without actions")
    parser.add_option("-q",
                      action="store_true", dest='quiet', default=False,
                      help="don't print the report file")
    parser.add_option("-s",
                      action="store_true", dest='statistics', default=False,
                      help="print parser stats to standard output")
    parser.add_option("-v",
                      action="store_true", dest='version', default=False,
                      help="print the version number")

    options, inputFiles = parser.parse_args(argv[1:])

    if options.version:
        printf("Lemonade 1.0\n")
        exit(0)

    if len(inputFiles) != 1:
        fprintf(stderr, "Exactly one filename argument is required.\n")
        exit(1)

    lem = lemon(
        None,
        None,
        0, 0, 0, 0,
        None,
        0, # errorcnt
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        0, 0, 0, 0,
        None,
        )

    # Initialize the machine
    Strsafe_init()
    Symbol_init()
    State_init()
    lem.argv0 = argv[0]
    lem.filename = inputFiles[0]
    lem.basisflag = options.basisflag
    Symbol_new("$")
    lem.errsym = Symbol_new("error")
    lem.errsym.useCnt = 0

    # Parse the input file
    Parse(lem)
    if lem.errorcnt:
        exit(lem.errorcnt)
    if lem.nrule == 0:
        fprintf(stderr, "Empty grammar.\n")
        exit(1)

    # Count and index the symbols of the grammar
    lem.nsymbol = Symbol_count()
    Symbol_new("{default}")
    lem.symbols = Symbol_arrayof()
    for i in range(lem.nsymbol + 1):
        lem.symbols[i].index = i
    lem.symbols.sort(cmp=Symbolcmpp)
    for i in range(lem.nsymbol + 1):
        lem.symbols[i].index = i
    i = 1
    while lem.symbols[i].name[0].isupper():
        i += 1
    lem.nterminal = i

    # Generate a reprint of the grammar, if requested on the command line
    if options.rpflag:
        Reprint(lem)
    else:
        # Initialize the size for all follow and first sets
        SetSize(lem.nterminal + 1)

        # Find the precedence for every production rule (that has one)
        FindRulePrecedences(lem)

        # Compute the lambda-nonterminals and the first-sets for every
        # nonterminal
        FindFirstSets(lem)

        # Compute all LR(0) states.  Also record follow-set
        # propagation links so that the follow-set can be computed
        # later
        lem.nstate = 0
        FindStates(lem)
        lem.sorted = State_arrayof()

        # Tie up loose ends on the propagation links
        FindLinks(lem)

        # Compute the follow set of every reducible configuration
        FindFollowSets(lem)

        # Compute the action tables
        FindActions(lem)

        # Compress the action tables
        if not options.compress:
            CompressTables(lem)

        # Reorder and renumber the states so that states with fewer
        # choices occur at the end.
        ResortStates(lem)

        # Generate a report of the parser generated.  (the "y.output" file)
        if not options.quiet:
            ReportOutput(lem)

        # Generate the source code for the parser
        ReportTable(lem)


    if options.statistics:
        printf("Parser statistics: %d terminals, %d nonterminals, %d rules\n",
               lem.nterminal, lem.nsymbol - lem.nterminal, lem.nrule)
        printf("                   %d states, %d parser table entries, %d conflicts\n",
               lem.nstate, lem.tablesize, lem.nconflict)

    if lem.nconflict:
        fprintf(stderr, "%d parsing conflicts.\n", lem.nconflict)

    exit(lem.errorcnt + lem.nconflict)
    return lem.errorcnt + lem.nconflict


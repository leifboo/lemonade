
def memory_error():
    fprintf(stderr, "Out of memory.  Aborting...\n")
    exit(1)

nDefine = 0
azDefine = 0
def handle_D_option(z):
    nDefine += 1
    azDefine = realloc(azDefine, (sizeof(azDefine[0])) * nDefine)
    if azDefine == 0:
        fprintf(stderr, "out of memory\n")
        exit(1)

    paz = &azDefine[nDefine - 1]
    paz[00] = malloc(strlen(z) + 1)
    if (paz[00]) == 0:
        fprintf(stderr, "out of memory\n")
        exit(1)

    strcpy(paz[00], z)
    for (z = paz[00]; (z[00]) and ((z[00]) != '='); z++):
        pass

    z[00] = 0

def main(argc, argv):
    version = 0
    rpflag = 0
    basisflag = 0
    compress = 0
    quiet = 0
    statistics = 0
    mhflag = 0
    options = XXXstructInitXXX([OPT_FLAG, "b", &basisflag, "Print only the basis in report."], [OPT_FLAG, "c", &compress, "Don't compress the action table."], [OPT_FSTR, "D", handle_D_option, "Define an %ifdef macro."], [OPT_FLAG, "g", &rpflag, "Print grammar without actions."], [OPT_FLAG, "m", &mhflag, "Output a makeheaders compatible file"], [OPT_FLAG, "q", &quiet, "(Quiet) Don't print the report file."], [OPT_FLAG, "s", &statistics, "Print parser stats to standard output."], [OPT_FLAG, "x", &version, "Print the version number."], [OPT_FLAG, 0, 0, 0])
    OptInit(argv, options, stderr)
    if version:
        printf("Lemon version 1.0\n")
        exit(0)

    if OptNArgs() != 1:
        fprintf(stderr, "Exactly one filename argument is required.\n")
        exit(1)

    memset(&lem, 0, sizeof(lem))
    lem.errorcnt = 0
    Strsafe_init()
    Symbol_init()
    State_init()
    lem.argv0 = argv[0]
    lem.filename = OptArg(0)
    lem.basisflag = basisflag
    Symbol_new("$")
    lem.errsym = Symbol_new("error")
    lem.errsym.useCnt = 0
    Parse(&lem)
    if lem.errorcnt:
        exit(lem.errorcnt)

    if lem.nrule == 0:
        fprintf(stderr, "Empty grammar.\n")
        exit(1)

    lem.nsymbol = Symbol_count()
    Symbol_new("{default}")
    lem.symbols = Symbol_arrayof()
    for (i = 0; i <= lem.nsymbol; i++):
        lem.symbols[i].index = i

    qsort(lem.symbols, lem.nsymbol + 1, sizeof(), Symbolcmpp)
    for (i = 0; i <= lem.nsymbol; i++):
        lem.symbols[i].index = i

    for (i = 1; (__ctype_b_loc()[00])[lem.symbols[i].name[0]] & (_ISupper); i++):
        pass

    lem.nterminal = i
    if rpflag:
        Reprint(&lem)
    else:
        SetSize(lem.nterminal + 1)
        FindRulePrecedences(&lem)
        FindFirstSets(&lem)
        lem.nstate = 0
        FindStates(&lem)
        lem.sorted = State_arrayof()
        FindLinks(&lem)
        FindFollowSets(&lem)
        FindActions(&lem)
        if compress == 0:
            CompressTables(&lem)

        ResortStates(&lem)
        if not quiet:
            ReportOutput(&lem)

        ReportTable(&lem, mhflag)
        if not mhflag:
            ReportHeader(&lem)


    if statistics:
        printf("Parser statistics: %d terminals, %d nonterminals, %d rules\n", lem.nterminal, lem.nsymbol - lem.nterminal, lem.nrule)
        printf("                   %d states, %d parser table entries, %d conflicts\n", lem.nstate, lem.tablesize, lem.nconflict)

    if lem.nconflict:
        fprintf(stderr, "%d parsing conflicts.\n", lem.nconflict)

    exit(lem.errorcnt + lem.nconflict)
    return lem.errorcnt + lem.nconflict


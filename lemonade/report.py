
def file_makename(lemp, suffix):
    name = malloc((strlen(lemp.filename) + strlen(suffix)) + 5)
    if name == 0:
        fprintf(stderr, "Can't allocate space for a filename.\n")
        exit(1)

    cp = strrchr(lemp.filename, '/')
    cp = cp + 1 if cp else lemp.filename
    strcpy(name, cp)
    cp = strrchr(name, '.')
    if cp:
        cp[00] = 0

    strcat(name, suffix)
    return name

def file_open(lemp, suffix, mode):
    if lemp.outname:
        free(lemp.outname)

    lemp.outname = file_makename(lemp, suffix)
    fp = fopen(lemp.outname, mode)
    if (fp == 0) and ((mode[00]) == 'w'):
        fprintf(stderr, "Can't open file \"%s\".\n", lemp.outname)
        lemp.errorcnt += 1
        return 0

    return fp

def Reprint(lemp):
    printf("// Reprint of input file \"%s\".\n// Symbols:\n", lemp.filename)
    maxlen = 10
    for (i = 0; i < lemp.nsymbol; i++):
        sp = lemp.symbols[i]
        len = strlen(sp.name)
        if len > maxlen:
            maxlen = len


    ncolumns = 76 / (maxlen + 5)
    if ncolumns < 1:
        ncolumns = 1

    skip = ((lemp.nsymbol + ncolumns) - 1) / ncolumns
    for (i = 0; i < skip; i++):
        printf("//")
        for (j = i; j < lemp.nsymbol; j += skip):
            sp = lemp.symbols[j]
            _assert(sp.index == j)
            printf(" %3d %-*.*s", j, maxlen, maxlen, sp.name)

        printf("\n")

    for (rp = lemp.rule; rp; rp = rp.next):
        printf("%s", rp.lhs.name)
        printf(" ::=")
        for (i = 0; i < rp.nrhs; i++):
            sp = rp.rhs[i]
            printf(" %s", sp.name)
            if sp.type == MULTITERMINAL:
                for (j = 1; j < sp.nsubsym; j++):
                    printf("|%s", sp.subsym[j].name)



        printf(".")
        if rp.precsym:
            printf(" [%s]", rp.precsym.name)

        printf("\n")


def ConfigPrint(fp, cfp):
    rp = cfp.rp
    fprintf(fp, "%s ::=", rp.lhs.name)
    for (i = 0; i <= rp.nrhs; i++):
        if i == cfp.dot:
            fprintf(fp, " *")

        if i == rp.nrhs:
            break

        sp = rp.rhs[i]
        fprintf(fp, " %s", sp.name)
        if sp.type == MULTITERMINAL:
            for (j = 1; j < sp.nsubsym; j++):
                fprintf(fp, "|%s", sp.subsym[j].name)




def PrintAction(ap, fp, indent):
    result = 1
    @switch ap.type:
    @case SHIFT:
        fprintf(fp, "%*s shift  %d", indent, ap.sp.name, ap.x.stp.statenum)
        break

    @case REDUCE:
        fprintf(fp, "%*s reduce %d", indent, ap.sp.name, ap.x.rp.index)
        break

    @case ACCEPT:
        fprintf(fp, "%*s accept", indent, ap.sp.name)
        break

    @case ERROR:
        fprintf(fp, "%*s error", indent, ap.sp.name)
        break

    @case SRCONFLICT:

    @case RRCONFLICT:
        fprintf(fp, "%*s reduce %-3d ** Parsing conflict **", indent, ap.sp.name, ap.x.rp.index)
        break

    @case SSCONFLICT:
        fprintf(fp, "%*s shift  %d ** Parsing conflict **", indent, ap.sp.name, ap.x.stp.statenum)
        break

    @case SH_RESOLVED:

    @case RD_RESOLVED:

    @case NOT_USED:
        result = 0
        break


    return result

def ReportOutput(lemp):
    fp = file_open(lemp, ".out", "wb")
    if fp == 0:
        return

    for (i = 0; i < lemp.nstate; i++):
        stp = lemp.sorted[i]
        fprintf(fp, "State %d:\n", stp.statenum)
        if lemp.basisflag:
            cfp = stp.bp
        else:
            cfp = stp.cfp

        while cfp:
            if cfp.dot == cfp.rp.nrhs:
                sprintf(buf, "(%d)", cfp.rp.index)
                fprintf(fp, "    %5s ", buf)
            else:
                fprintf(fp, "          ")

            ConfigPrint(fp, cfp)
            fprintf(fp, "\n")
            if lemp.basisflag:
                cfp = cfp.bp
            else:
                cfp = cfp.next


        fprintf(fp, "\n")
        for (ap = stp.ap; ap; ap = ap.next):
            if PrintAction(ap, fp, 30):
                fprintf(fp, "\n")


        fprintf(fp, "\n")

    fprintf(fp, "----------------------------------------------------\n")
    fprintf(fp, "Symbols:\n")
    for (i = 0; i < lemp.nsymbol; i++):
        sp = lemp.symbols[i]
        fprintf(fp, "  %3d: %s", i, sp.name)
        if sp.type == NONTERMINAL:
            fprintf(fp, ":")
            if sp._lambda:
                fprintf(fp, " <lambda>")

            for (j = 0; j < lemp.nterminal; j++):
                if sp.firstset and sp.firstset[j]:
                    fprintf(fp, " %s", lemp.symbols[j].name)



        fprintf(fp, "\n")

    fclose(fp)
    return

def pathsearch(argv0, name, modemask):
    cp = strrchr(argv0, '/')
    if cp:
        c = cp[00]
        cp[00] = 0
        path = malloc((strlen(argv0) + strlen(name)) + 2)
        if path:
            sprintf(path, "%s/%s", argv0, name)

        cp[00] = c
    else:
        pathlist = getenv("PATH")
        if pathlist == 0:
            pathlist = ".:/bin:/usr/bin"

        path = malloc((strlen(pathlist) + strlen(name)) + 2)
        if path != 0:
            while pathlist[00]:
                cp = strchr(pathlist, ':')
                if cp == 0:
                    cp = &pathlist[strlen(pathlist)]

                c = cp[00]
                cp[00] = 0
                sprintf(path, "%s/%s", pathlist, name)
                cp[00] = c
                if c == 0:
                    pathlist = ""
                else:
                    pathlist = &cp[1]

                if access(path, modemask) == 0:
                    break




    return path

def compute_action(lemp, ap):
    @switch ap.type:
    @case SHIFT:
        act = ap.x.stp.statenum
        break

    @case REDUCE:
        act = ap.x.rp.index + lemp.nstate
        break

    @case ERROR:
        act = lemp.nstate + lemp.nrule
        break

    @case ACCEPT:
        act = (lemp.nstate + lemp.nrule) + 1
        break

    @default:
        act = -1
        break


    return act

def tplt_xfer(name, _in, out, lineno):
    while fgets(line, 1000, _in) and ((line[0] != '%') or (line[1] != '%')):
        (lineno[00]) += 1
        iStart = 0
        if name:
            for (i = 0; line[i]; i++):
                if ((line[i] == 'P') and (strncmp(&line[i], "Parse", 5) == 0)) and ((i == 0) or (not ((__ctype_b_loc()[00])[line[i - 1]] & (_ISalpha)))):
                    if i > iStart:
                        fprintf(out, "%.*s", i - iStart, &line[iStart])

                    fprintf(out, "%s", name)
                    i += 4
                    iStart = i + 1



        fprintf(out, "%s", &line[iStart])


def tplt_open(lemp):
    templatename = "lempar.c"
    cp = strrchr(lemp.filename, '.')
    if cp:
        sprintf(buf, "%.*s.lt", cp - lemp.filename, lemp.filename)
    else:
        sprintf(buf, "%s.lt", lemp.filename)

    if access(buf, 004) == 0:
        tpltname = buf
    elif access(templatename, 004) == 0:
        tpltname = templatename
    else:
        tpltname = pathsearch(lemp.argv0, templatename, 0)
        if access(tpltname, 004) != 0:
            tpltname = 0


    if (not tpltname) and (cp = strrchr(lemp.filename, '/')):
        sprintf(buf, "%.*s/%s", cp - lemp.filename, lemp.filename, templatename)
        if access(buf, 004) == 0:
            tpltname = buf


    if tpltname == 0:
        fprintf(stderr, "Can't find the parser driver template file \"%s\".\n", templatename)
        lemp.errorcnt += 1
        return 0

    _in = fopen(tpltname, "rb")
    if _in == 0:
        fprintf(stderr, "Can't open the template file \"%s\".\n", templatename)
        lemp.errorcnt += 1
        return 0

    return _in

def tplt_linedir(out, lineno, filename):
    fprintf(out, "#line %d \"", lineno)
    while filename[00]:
        if (filename[00]) == '\\':
            _IO_putc('\\', out)

        _IO_putc(filename[00], out)
        filename += 1

    fprintf(out, "\"\n")

def tplt_print(out, lemp, str, lineno):
    if str == 0:
        return

    (lineno[00]) += 1
    while str[00]:
        if (str[00]) == '\n':
            (lineno[00]) += 1

        _IO_putc(str[00], out)
        str += 1

    if str[-1] != '\n':
        _IO_putc('\n', out)
        (lineno[00]) += 1

    tplt_linedir(out, (lineno[00]) + 2, lemp.outname)
    lineno[00] += 2
    return

def emit_destructor_code(out, sp, lemp, lineno):
    cp = 0
    linecnt = 0
    if sp.type == TERMINAL:
        cp = lemp.tokendest
        if cp == 0:
            return

        fprintf(out, "{\n")
        (lineno[00]) += 1
    elif sp.destructor:
        cp = sp.destructor
        fprintf(out, "{\n")
        (lineno[00]) += 1
    elif lemp.vardest:
        cp = lemp.vardest
        if cp == 0:
            return

        fprintf(out, "{\n")
        (lineno[00]) += 1
    else:
        _assert(0)

    for (; cp[00]; cp++):
        if ((cp[00]) == '$') and (cp[1] == '$'):
            fprintf(out, "(yypminor->yy%d)", sp.dtnum)
            cp += 1
            continue

        if (cp[00]) == '\n':
            linecnt += 1

        fputc(cp[00], out)

    lineno[00] += 3 + linecnt
    fprintf(out, "\n")
    tplt_linedir(out, lineno[00], lemp.outname)
    fprintf(out, "}\n")
    return

def has_destructor(sp, lemp):
    if sp.type == TERMINAL:
        ret = lemp.tokendest != 0
    else:
        ret = (lemp.vardest != 0) or (sp.destructor != 0)

    return ret

def append_str(zText, n, p1, p2):
    z = 0
    alloced = 0
    used = 0
    if zText == 0:
        used = 0
        return z

    if n <= 0:
        if n < 0:
            used += n
            _assert(used >= 0)

        n = strlen(zText)

    if ((n + ((sizeof(zInt)) * 2)) + used) >= alloced:
        alloced = ((n + ((sizeof(zInt)) * 2)) + used) + 200
        z = realloc(z, alloced)

    if z == 0:
        return ""

    while (n--) > 0:
        c = (zText++)[00]
        if ((c == '%') and (n > 0)) and (zText[0] == 'd'):
            sprintf(zInt, "%d", p1)
            p1 = p2
            strcpy(&z[used], zInt)
            used += strlen(&z[used])
            zText += 1
            n -= 1
        else:
            z[used++] = c


    z[used] = 0
    return z

def translate_code(lemp, rp):
    lhsused = 0
    for (i = 0; i < rp.nrhs; i++):
        used[i] = 0

    lhsused = 0
    if rp.code == 0:
        rp.code = "\n"
        rp.line = rp.ruleline

    append_str(0, 0, 0, 0)
    for (cp = rp.code; cp[00]; cp++):
        if ((__ctype_b_loc()[00])[cp[00]] & (_ISalpha)) and ((cp == rp.code) or ((not ((__ctype_b_loc()[00])[cp[-1]] & (_ISalnum))) and (cp[-1] != '_'))):
            for (xp = &cp[1]; ((__ctype_b_loc()[00])[xp[00]] & (_ISalnum)) or ((xp[00]) == '_'); xp++):
                pass

            saved = xp[00]
            xp[00] = 0
            if rp.lhsalias and (strcmp(cp, rp.lhsalias) == 0):
                append_str("yygotominor.yy%d", 0, rp.lhs.dtnum, 0)
                cp = xp
                lhsused = 1
            else:
                for (i = 0; i < rp.nrhs; i++):
                    if rp.rhsalias[i] and (strcmp(cp, rp.rhsalias[i]) == 0):
                        if (cp != rp.code) and (cp[-1] == '@'):
                            append_str("yymsp[%d].major", -1, (i - rp.nrhs) + 1, 0)
                        else:
                            sp = rp.rhs[i]
                            if sp.type == MULTITERMINAL:
                                dtnum = sp.subsym[0].dtnum
                            else:
                                dtnum = sp.dtnum

                            append_str("yymsp[%d].minor.yy%d", 0, (i - rp.nrhs) + 1, dtnum)

                        cp = xp
                        used[i] = 1
                        break



            xp[00] = saved

        append_str(cp, 1, 0, 0)

    if rp.lhsalias and (not lhsused):
        ErrorMsg(lemp.filename, rp.ruleline, "Label \"%s\" for \"%s(%s)\" is never used.", rp.lhsalias, rp.lhs.name, rp.lhsalias)
        lemp.errorcnt += 1

    for (i = 0; i < rp.nrhs; i++):
        if rp.rhsalias[i] and (not used[i]):
            ErrorMsg(lemp.filename, rp.ruleline, "Label %s for \"%s(%s)\" is never used.", rp.rhsalias[i], rp.rhs[i].name, rp.rhsalias[i])
            lemp.errorcnt += 1
        elif rp.rhsalias[i] == 0:
            if has_destructor(rp.rhs[i], lemp):
                append_str("  yy_destructor(%d,&yymsp[%d].minor);\n", 0, rp.rhs[i].index, (i - rp.nrhs) + 1)
            else:
                pass



    if rp.code:
        cp = append_str(0, 0, 0, 0)
        rp.code = Strsafe(cp if cp else "")


def emit_code(out, rp, lemp, lineno):
    linecnt = 0
    if rp.code:
        tplt_linedir(out, rp.line, lemp.filename)
        fprintf(out, "{%s", rp.code)
        for (cp = rp.code; cp[00]; cp++):
            if (cp[00]) == '\n':
                linecnt += 1


        lineno[00] += 3 + linecnt
        fprintf(out, "}\n")
        tplt_linedir(out, lineno[00], lemp.outname)

    return

def print_stack_union(out, lemp, plineno, mhflag):
    lineno = plineno[00]
    arraysize = lemp.nsymbol * 2
    types = calloc(arraysize, sizeof())
    for (i = 0; i < arraysize; i++):
        types[i] = 0

    maxdtlength = 0
    if lemp.vartype:
        maxdtlength = strlen(lemp.vartype)

    for (i = 0; i < lemp.nsymbol; i++):
        sp = lemp.symbols[i]
        if sp.datatype == 0:
            continue

        len = strlen(sp.datatype)
        if len > maxdtlength:
            maxdtlength = len


    stddt = malloc((maxdtlength * 2) + 1)
    if (types == 0) or (stddt == 0):
        fprintf(stderr, "Out of memory.\n")
        exit(1)

    for (i = 0; i < lemp.nsymbol; i++):
        sp = lemp.symbols[i]
        if sp == lemp.errsym:
            sp.dtnum = arraysize + 1
            continue

        if (sp.type != NONTERMINAL) or ((sp.datatype == 0) and (lemp.vartype == 0)):
            sp.dtnum = 0
            continue

        cp = sp.datatype
        if cp == 0:
            cp = lemp.vartype

        j = 0
        while (__ctype_b_loc()[00])[cp[00]] & (_ISspace):
            cp += 1

        while cp[00]:
            stddt[j++] = (cp++)[00]

        while (j > 0) and ((__ctype_b_loc()[00])[stddt[j - 1]] & (_ISspace)):
            j -= 1

        stddt[j] = 0
        hash = 0
        for (j = 0; stddt[j]; j++):
            hash = (hash * 53) + stddt[j]

        hash = (hash & 0x7fffffff) % arraysize
        while types[hash]:
            if strcmp(types[hash], stddt) == 0:
                sp.dtnum = hash + 1
                break

            hash += 1
            if hash >= arraysize:
                hash = 0


        if types[hash] == 0:
            sp.dtnum = hash + 1
            types[hash] = malloc(strlen(stddt) + 1)
            if types[hash] == 0:
                fprintf(stderr, "Out of memory.\n")
                exit(1)

            strcpy(types[hash], stddt)


    name = lemp.name if lemp.name else "Parse"
    lineno = plineno[00]
    if mhflag:
        fprintf(out, "#if INTERFACE\n")
        lineno += 1

    fprintf(out, "#define %sTOKENTYPE %s\n", name, lemp.tokentype if lemp.tokentype else "void*")
    lineno += 1
    if mhflag:
        fprintf(out, "#endif\n")
        lineno += 1

    fprintf(out, "typedef union {\n")
    lineno += 1
    fprintf(out, "  %sTOKENTYPE yy0;\n", name)
    lineno += 1
    for (i = 0; i < arraysize; i++):
        if types[i] == 0:
            continue

        fprintf(out, "  %s yy%d;\n", types[i], i + 1)
        lineno += 1
        free(types[i])

    if lemp.errsym.useCnt:
        fprintf(out, "  int yy%d;\n", lemp.errsym.dtnum)
        lineno += 1

    free(stddt)
    free(types)
    fprintf(out, "} YYMINORTYPE;\n")
    lineno += 1
    plineno[00] = lineno

def minimum_size_type(lwr, upr):
    if lwr >= 0:
        if upr <= 255:
            return "unsigned char"
        elif upr < 65535:
            return "unsigned short int"
        else:
            return "unsigned int"

    elif (lwr >= (-127)) and (upr <= 127):
        return "signed char"
    elif (lwr >= (-32767)) and (upr < 32767):
        return "short"
    else:
        return "int"



def axset_compare(a, b):
    p1 = a
    p2 = b
    return p2.nAction - p1.nAction

def writeRuleText(out, rp):
    fprintf(out, "%s ::=", rp.lhs.name)
    for (j = 0; j < rp.nrhs; j++):
        sp = rp.rhs[j]
        fprintf(out, " %s", sp.name)
        if sp.type == MULTITERMINAL:
            for (k = 1; k < sp.nsubsym; k++):
                fprintf(out, "|%s", sp.subsym[k].name)




def ReportTable(lemp, mhflag):
    _in = tplt_open(lemp)
    if _in == 0:
        return

    out = file_open(lemp, ".c", "wb")
    if out == 0:
        fclose(_in)
        return

    lineno = 1
    tplt_xfer(lemp.name, _in, out, &lineno)
    tplt_print(out, lemp, lemp.include, &lineno)
    if mhflag:
        name = file_makename(lemp, ".h")
        fprintf(out, "#include \"%s\"\n", name)
        lineno += 1
        free(name)

    tplt_xfer(lemp.name, _in, out, &lineno)
    if mhflag:
        fprintf(out, "#if INTERFACE\n")
        lineno += 1
        if lemp.tokenprefix:
            prefix = lemp.tokenprefix
        else:
            prefix = ""

        for (i = 1; i < lemp.nterminal; i++):
            fprintf(out, "#define %s%-30s %2d\n", prefix, lemp.symbols[i].name, i)
            lineno += 1

        fprintf(out, "#endif\n")
        lineno += 1

    tplt_xfer(lemp.name, _in, out, &lineno)
    fprintf(out, "#define YYCODETYPE %s\n", minimum_size_type(0, lemp.nsymbol + 5))
    lineno += 1
    fprintf(out, "#define YYNOCODE %d\n", lemp.nsymbol + 1)
    lineno += 1
    fprintf(out, "#define YYACTIONTYPE %s\n", minimum_size_type(0, (lemp.nstate + lemp.nrule) + 5))
    lineno += 1
    if lemp.wildcard:
        fprintf(out, "#define YYWILDCARD %d\n", lemp.wildcard.index)
        lineno += 1

    print_stack_union(out, lemp, &lineno, mhflag)
    fprintf(out, "#ifndef YYSTACKDEPTH\n")
    lineno += 1
    if lemp.stacksize:
        fprintf(out, "#define YYSTACKDEPTH %s\n", lemp.stacksize)
        lineno += 1
    else:
        fprintf(out, "#define YYSTACKDEPTH 100\n")
        lineno += 1

    fprintf(out, "#endif\n")
    lineno += 1
    if mhflag:
        fprintf(out, "#if INTERFACE\n")
        lineno += 1

    name = lemp.name if lemp.name else "Parse"
    if lemp.arg and lemp.arg[0]:
        i = strlen(lemp.arg)
        while (i >= 1) and ((__ctype_b_loc()[00])[lemp.arg[i - 1]] & (_ISspace)):
            i -= 1

        while (i >= 1) and (((__ctype_b_loc()[00])[lemp.arg[i - 1]] & (_ISalnum)) or (lemp.arg[i - 1] == '_')):
            i -= 1

        fprintf(out, "#define %sARG_SDECL %s;\n", name, lemp.arg)
        lineno += 1
        fprintf(out, "#define %sARG_PDECL ,%s\n", name, lemp.arg)
        lineno += 1
        fprintf(out, "#define %sARG_FETCH %s = yypParser->%s\n", name, lemp.arg, &lemp.arg[i])
        lineno += 1
        fprintf(out, "#define %sARG_STORE yypParser->%s = %s\n", name, &lemp.arg[i], &lemp.arg[i])
        lineno += 1
    else:
        fprintf(out, "#define %sARG_SDECL\n", name)
        lineno += 1
        fprintf(out, "#define %sARG_PDECL\n", name)
        lineno += 1
        fprintf(out, "#define %sARG_FETCH\n", name)
        lineno += 1
        fprintf(out, "#define %sARG_STORE\n", name)
        lineno += 1

    if mhflag:
        fprintf(out, "#endif\n")
        lineno += 1

    fprintf(out, "#define YYNSTATE %d\n", lemp.nstate)
    lineno += 1
    fprintf(out, "#define YYNRULE %d\n", lemp.nrule)
    lineno += 1
    if lemp.errsym.useCnt:
        fprintf(out, "#define YYERRORSYMBOL %d\n", lemp.errsym.index)
        lineno += 1
        fprintf(out, "#define YYERRSYMDT yy%d\n", lemp.errsym.dtnum)
        lineno += 1

    if lemp.has_fallback:
        fprintf(out, "#define YYFALLBACK 1\n")
        lineno += 1

    tplt_xfer(lemp.name, _in, out, &lineno)
    ax = calloc(lemp.nstate * 2, sizeof(ax[0]))
    if ax == 0:
        fprintf(stderr, "malloc failed\n")
        exit(1)

    for (i = 0; i < lemp.nstate; i++):
        stp = lemp.sorted[i]
        ax[i * 2].stp = stp
        ax[i * 2].isTkn = 1
        ax[i * 2].nAction = stp.nTknAct
        ax[(i * 2) + 1].stp = stp
        ax[(i * 2) + 1].isTkn = 0
        ax[(i * 2) + 1].nAction = stp.nNtAct

    mxTknOfst = (mnTknOfst = 0)
    mxNtOfst = (mnNtOfst = 0)
    qsort(ax, lemp.nstate * 2, sizeof(ax[0]), axset_compare)
    pActtab = acttab_alloc()
    for (i = 0; (i < (lemp.nstate * 2)) and (ax[i].nAction > 0); i++):
        stp = ax[i].stp
        if ax[i].isTkn:
            for (ap = stp.ap; ap; ap = ap.next):
                if ap.sp.index >= lemp.nterminal:
                    continue

                action = compute_action(lemp, ap)
                if action < 0:
                    continue

                acttab_action(pActtab, ap.sp.index, action)

            stp.iTknOfst = acttab_insert(pActtab)
            if stp.iTknOfst < mnTknOfst:
                mnTknOfst = stp.iTknOfst

            if stp.iTknOfst > mxTknOfst:
                mxTknOfst = stp.iTknOfst

        else:
            for (ap = stp.ap; ap; ap = ap.next):
                if ap.sp.index < lemp.nterminal:
                    continue

                if ap.sp.index == lemp.nsymbol:
                    continue

                action = compute_action(lemp, ap)
                if action < 0:
                    continue

                acttab_action(pActtab, ap.sp.index, action)

            stp.iNtOfst = acttab_insert(pActtab)
            if stp.iNtOfst < mnNtOfst:
                mnNtOfst = stp.iNtOfst

            if stp.iNtOfst > mxNtOfst:
                mxNtOfst = stp.iNtOfst



    free(ax)
    fprintf(out, "static const YYACTIONTYPE yy_action[] = {\n")
    lineno += 1
    n = pActtab.nAction
    for (i = (j = 0); i < n; i++):
        action = pActtab.aAction[i].action
        if action < 0:
            action = (lemp.nstate + lemp.nrule) + 2

        if j == 0:
            fprintf(out, " /* %5d */ ", i)

        fprintf(out, " %4d,", action)
        if (j == 9) or (i == (n - 1)):
            fprintf(out, "\n")
            lineno += 1
            j = 0
        else:
            j += 1


    fprintf(out, "};\n")
    lineno += 1
    fprintf(out, "static const YYCODETYPE yy_lookahead[] = {\n")
    lineno += 1
    for (i = (j = 0); i < n; i++):
        la = pActtab.aAction[i].lookahead
        if la < 0:
            la = lemp.nsymbol

        if j == 0:
            fprintf(out, " /* %5d */ ", i)

        fprintf(out, " %4d,", la)
        if (j == 9) or (i == (n - 1)):
            fprintf(out, "\n")
            lineno += 1
            j = 0
        else:
            j += 1


    fprintf(out, "};\n")
    lineno += 1
    fprintf(out, "#define YY_SHIFT_USE_DFLT (%d)\n", mnTknOfst - 1)
    lineno += 1
    n = lemp.nstate
    while (n > 0) and (lemp.sorted[n - 1].iTknOfst == (-2147483647)):
        n -= 1

    fprintf(out, "#define YY_SHIFT_MAX %d\n", n - 1)
    lineno += 1
    fprintf(out, "static const %s yy_shift_ofst[] = {\n", minimum_size_type(mnTknOfst - 1, mxTknOfst))
    lineno += 1
    for (i = (j = 0); i < n; i++):
        stp = lemp.sorted[i]
        ofst = stp.iTknOfst
        if ofst == (-2147483647):
            ofst = mnTknOfst - 1

        if j == 0:
            fprintf(out, " /* %5d */ ", i)

        fprintf(out, " %4d,", ofst)
        if (j == 9) or (i == (n - 1)):
            fprintf(out, "\n")
            lineno += 1
            j = 0
        else:
            j += 1


    fprintf(out, "};\n")
    lineno += 1
    fprintf(out, "#define YY_REDUCE_USE_DFLT (%d)\n", mnNtOfst - 1)
    lineno += 1
    n = lemp.nstate
    while (n > 0) and (lemp.sorted[n - 1].iNtOfst == (-2147483647)):
        n -= 1

    fprintf(out, "#define YY_REDUCE_MAX %d\n", n - 1)
    lineno += 1
    fprintf(out, "static const %s yy_reduce_ofst[] = {\n", minimum_size_type(mnNtOfst - 1, mxNtOfst))
    lineno += 1
    for (i = (j = 0); i < n; i++):
        stp = lemp.sorted[i]
        ofst = stp.iNtOfst
        if ofst == (-2147483647):
            ofst = mnNtOfst - 1

        if j == 0:
            fprintf(out, " /* %5d */ ", i)

        fprintf(out, " %4d,", ofst)
        if (j == 9) or (i == (n - 1)):
            fprintf(out, "\n")
            lineno += 1
            j = 0
        else:
            j += 1


    fprintf(out, "};\n")
    lineno += 1
    fprintf(out, "static const YYACTIONTYPE yy_default[] = {\n")
    lineno += 1
    n = lemp.nstate
    for (i = (j = 0); i < n; i++):
        stp = lemp.sorted[i]
        if j == 0:
            fprintf(out, " /* %5d */ ", i)

        fprintf(out, " %4d,", stp.iDflt)
        if (j == 9) or (i == (n - 1)):
            fprintf(out, "\n")
            lineno += 1
            j = 0
        else:
            j += 1


    fprintf(out, "};\n")
    lineno += 1
    tplt_xfer(lemp.name, _in, out, &lineno)
    if lemp.has_fallback:
        for (i = 0; i < lemp.nterminal; i++):
            p = lemp.symbols[i]
            if p.fallback == 0:
                fprintf(out, "    0,  /* %10s => nothing */\n", p.name)
            else:
                fprintf(out, "  %3d,  /* %10s => %s */\n", p.fallback.index, p.name, p.fallback.name)

            lineno += 1


    tplt_xfer(lemp.name, _in, out, &lineno)
    for (i = 0; i < lemp.nsymbol; i++):
        sprintf(line, "\"%s\",", lemp.symbols[i].name)
        fprintf(out, "  %-15s", line)
        if (i & 3) == 3:
            fprintf(out, "\n")
            lineno += 1


    if (i & 3) != 0:
        fprintf(out, "\n")
        lineno += 1

    tplt_xfer(lemp.name, _in, out, &lineno)
    for (i = 0, rp = lemp.rule; rp; rp = rp.next, i++):
        _assert(rp.index == i)
        fprintf(out, " /* %3d */ \"", i)
        writeRuleText(out, rp)
        fprintf(out, "\",\n")
        lineno += 1

    tplt_xfer(lemp.name, _in, out, &lineno)
    if lemp.tokendest:
        for (i = 0; i < lemp.nsymbol; i++):
            sp = lemp.symbols[i]
            if (sp == 0) or (sp.type != TERMINAL):
                continue

            fprintf(out, "    case %d: /* %s */\n", sp.index, sp.name)
            lineno += 1

        for (i = 0; (i < lemp.nsymbol) and (lemp.symbols[i].type != TERMINAL); i++):
            pass

        if i < lemp.nsymbol:
            emit_destructor_code(out, lemp.symbols[i], lemp, &lineno)
            fprintf(out, "      break;\n")
            lineno += 1


    if lemp.vardest:
        dflt_sp = 0
        for (i = 0; i < lemp.nsymbol; i++):
            sp = lemp.symbols[i]
            if (((sp == 0) or (sp.type == TERMINAL)) or (sp.index <= 0)) or (sp.destructor != 0):
                continue

            fprintf(out, "    case %d: /* %s */\n", sp.index, sp.name)
            lineno += 1
            dflt_sp = sp

        if dflt_sp != 0:
            emit_destructor_code(out, dflt_sp, lemp, &lineno)
            fprintf(out, "      break;\n")
            lineno += 1


    for (i = 0; i < lemp.nsymbol; i++):
        sp = lemp.symbols[i]
        if ((sp == 0) or (sp.type == TERMINAL)) or (sp.destructor == 0):
            continue

        fprintf(out, "    case %d: /* %s */\n", sp.index, sp.name)
        lineno += 1
        for (j = i + 1; j < lemp.nsymbol; j++):
            sp2 = lemp.symbols[j]
            if (((sp2 and (sp2.type != TERMINAL)) and sp2.destructor) and (sp2.dtnum == sp.dtnum)) and (strcmp(sp.destructor, sp2.destructor) == 0):
                fprintf(out, "    case %d: /* %s */\n", sp2.index, sp2.name)
                lineno += 1
                sp2.destructor = 0


        emit_destructor_code(out, lemp.symbols[i], lemp, &lineno)
        fprintf(out, "      break;\n")
        lineno += 1

    tplt_xfer(lemp.name, _in, out, &lineno)
    tplt_print(out, lemp, lemp.overflow, &lineno)
    tplt_xfer(lemp.name, _in, out, &lineno)
    for (rp = lemp.rule; rp; rp = rp.next):
        fprintf(out, "  { %d, %d },\n", rp.lhs.index, rp.nrhs)
        lineno += 1

    tplt_xfer(lemp.name, _in, out, &lineno)
    for (rp = lemp.rule; rp; rp = rp.next):
        translate_code(lemp, rp)

    for (rp = lemp.rule; rp; rp = rp.next):
        if rp.code == 0:
            continue

        fprintf(out, "      case %d: /* ", rp.index)
        writeRuleText(out, rp)
        fprintf(out, " */\n")
        lineno += 1
        for (rp2 = rp.next; rp2; rp2 = rp2.next):
            if rp2.code == rp.code:
                fprintf(out, "      case %d: /* ", rp2.index)
                writeRuleText(out, rp2)
                fprintf(out, " */\n")
                lineno += 1
                rp2.code = 0


        emit_code(out, rp, lemp, &lineno)
        fprintf(out, "        break;\n")
        lineno += 1

    tplt_xfer(lemp.name, _in, out, &lineno)
    tplt_print(out, lemp, lemp.failure, &lineno)
    tplt_xfer(lemp.name, _in, out, &lineno)
    tplt_print(out, lemp, lemp.error, &lineno)
    tplt_xfer(lemp.name, _in, out, &lineno)
    tplt_print(out, lemp, lemp.accept, &lineno)
    tplt_xfer(lemp.name, _in, out, &lineno)
    tplt_print(out, lemp, lemp.extracode, &lineno)
    fclose(_in)
    fclose(out)
    return

def ReportHeader(lemp):
    if lemp.tokenprefix:
        prefix = lemp.tokenprefix
    else:
        prefix = ""

    _in = file_open(lemp, ".h", "rb")
    if _in:
        for (i = 1; (i < lemp.nterminal) and fgets(line, 1000, _in); i++):
            sprintf(pattern, "#define %s%-30s %2d\n", prefix, lemp.symbols[i].name, i)
            if strcmp(line, pattern):
                break


        fclose(_in)
        if i == lemp.nterminal:
            return


    out = file_open(lemp, ".h", "wb")
    if out:
        for (i = 1; i < lemp.nterminal; i++):
            fprintf(out, "#define %s%-30s %2d\n", prefix, lemp.symbols[i].name, i)

        fclose(out)

    return

def CompressTables(lemp):
    for (i = 0; i < lemp.nstate; i++):
        stp = lemp.sorted[i]
        nbest = 0
        rbest = 0
        usesWildcard = 0
        for (ap = stp.ap; ap; ap = ap.next):
            if (ap.type == SHIFT) and (ap.sp == lemp.wildcard):
                usesWildcard = 1

            if ap.type != REDUCE:
                continue

            rp = ap.x.rp
            if rp.lhsStart:
                continue

            if rp == rbest:
                continue

            n = 1
            for (ap2 = ap.next; ap2; ap2 = ap2.next):
                if ap2.type != REDUCE:
                    continue

                rp2 = ap2.x.rp
                if rp2 == rbest:
                    continue

                if rp2 == rp:
                    n += 1


            if n > nbest:
                nbest = n
                rbest = rp


        if (nbest < 1) or usesWildcard:
            continue

        for (ap = stp.ap; ap; ap = ap.next):
            if (ap.type == REDUCE) and (ap.x.rp == rbest):
                break


        _assert(ap)
        ap.sp = Symbol_new("{default}")
        for (ap = ap.next; ap; ap = ap.next):
            if (ap.type == REDUCE) and (ap.x.rp == rbest):
                ap.type = NOT_USED


        stp.ap = Action_sort(stp.ap)


def stateResortCompare(a, b):
    pA = (a)[00]
    pB = (b)[00]
    n = pB.nNtAct - pA.nNtAct
    if n == 0:
        n = pB.nTknAct - pA.nTknAct

    return n

def ResortStates(lemp):
    for (i = 0; i < lemp.nstate; i++):
        stp = lemp.sorted[i]
        stp.nTknAct = (stp.nNtAct = 0)
        stp.iDflt = lemp.nstate + lemp.nrule
        stp.iTknOfst = -2147483647
        stp.iNtOfst = -2147483647
        for (ap = stp.ap; ap; ap = ap.next):
            if compute_action(lemp, ap) >= 0:
                if ap.sp.index < lemp.nterminal:
                    stp.nTknAct += 1
                elif ap.sp.index < lemp.nsymbol:
                    stp.nNtAct += 1
                else:
                    stp.iDflt = compute_action(lemp, ap)




    qsort(&lemp.sorted[1], lemp.nstate - 1, sizeof(lemp.sorted[0]), stateResortCompare)
    for (i = 0; i < lemp.nstate; i++):
        lemp.sorted[i].statenum = i



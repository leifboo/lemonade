

def parseonetoken(psp):
    x = Strsafe(psp.tokenstart)
    @switch psp.state:
    @case INITIALIZE:
        psp.prevrule = 0
        psp.preccounter = 0
        psp.firstrule = (psp.lastrule = 0)
        psp.gp.nrule = 0

    @case WAITING_FOR_DECL_OR_RULE:
        if x[0] == '%':
            psp.state = WAITING_FOR_DECL_KEYWORD
        elif (__ctype_b_loc()[00])[x[0]] & (_ISlower):
            psp.lhs = Symbol_new(x)
            psp.nrhs = 0
            psp.lhsalias = 0
            psp.state = WAITING_FOR_ARROW
        elif x[0] == '{':
            if psp.prevrule == 0:
                ErrorMsg(psp.filename, psp.tokenlineno, "There is not prior rule opon which to attach the code fragment which begins on this line.")
                psp.errorcnt += 1
            elif psp.prevrule.code != 0:
                ErrorMsg(psp.filename, psp.tokenlineno, "Code fragment beginning on this line is not the first to follow the previous rule.")
                psp.errorcnt += 1
            else:
                psp.prevrule.line = psp.tokenlineno
                psp.prevrule.code = &x[1]

        elif x[0] == '[':
            psp.state = PRECEDENCE_MARK_1
        else:
            ErrorMsg(psp.filename, psp.tokenlineno, "Token \"%s\" should be either \"%%\" or a nonterminal name.", x)
            psp.errorcnt += 1

        break

    @case PRECEDENCE_MARK_1:
        if not ((__ctype_b_loc()[00])[x[0]] & (_ISupper)):
            ErrorMsg(psp.filename, psp.tokenlineno, "The precedence symbol must be a terminal.")
            psp.errorcnt += 1
        elif psp.prevrule == 0:
            ErrorMsg(psp.filename, psp.tokenlineno, "There is no prior rule to assign precedence \"[%s]\".", x)
            psp.errorcnt += 1
        elif psp.prevrule.precsym != 0:
            ErrorMsg(psp.filename, psp.tokenlineno, "Precedence mark on this line is not the first to follow the previous rule.")
            psp.errorcnt += 1
        else:
            psp.prevrule.precsym = Symbol_new(x)

        psp.state = PRECEDENCE_MARK_2
        break

    @case PRECEDENCE_MARK_2:
        if x[0] != ']':
            ErrorMsg(psp.filename, psp.tokenlineno, "Missing \"]\" on precedence mark.")
            psp.errorcnt += 1

        psp.state = WAITING_FOR_DECL_OR_RULE
        break

    @case WAITING_FOR_ARROW:
        if ((x[0] == ':') and (x[1] == ':')) and (x[2] == '='):
            psp.state = IN_RHS
        elif x[0] == '(':
            psp.state = LHS_ALIAS_1
        else:
            ErrorMsg(psp.filename, psp.tokenlineno, "Expected to see a \":\" following the LHS symbol \"%s\".", psp.lhs.name)
            psp.errorcnt += 1
            psp.state = RESYNC_AFTER_RULE_ERROR

        break

    @case LHS_ALIAS_1:
        if (__ctype_b_loc()[00])[x[0]] & (_ISalpha):
            psp.lhsalias = x
            psp.state = LHS_ALIAS_2
        else:
            ErrorMsg(psp.filename, psp.tokenlineno, "\"%s\" is not a valid alias for the LHS \"%s\"\n", x, psp.lhs.name)
            psp.errorcnt += 1
            psp.state = RESYNC_AFTER_RULE_ERROR

        break

    @case LHS_ALIAS_2:
        if x[0] == ')':
            psp.state = LHS_ALIAS_3
        else:
            ErrorMsg(psp.filename, psp.tokenlineno, "Missing \")\" following LHS alias name \"%s\".", psp.lhsalias)
            psp.errorcnt += 1
            psp.state = RESYNC_AFTER_RULE_ERROR

        break

    @case LHS_ALIAS_3:
        if ((x[0] == ':') and (x[1] == ':')) and (x[2] == '='):
            psp.state = IN_RHS
        else:
            ErrorMsg(psp.filename, psp.tokenlineno, "Missing \"->\" following: \"%s(%s)\".", psp.lhs.name, psp.lhsalias)
            psp.errorcnt += 1
            psp.state = RESYNC_AFTER_RULE_ERROR

        break

    @case IN_RHS:
        if x[0] == '.':
            rp = calloc(((sizeof()) + ((sizeof()) * psp.nrhs)) + ((sizeof()) * psp.nrhs), 1)
            if rp == 0:
                ErrorMsg(psp.filename, psp.tokenlineno, "Can't allocate enough memory for this rule.")
                psp.errorcnt += 1
                psp.prevrule = 0
            else:
                rp.ruleline = psp.tokenlineno
                rp.rhs = &rp[1]
                rp.rhsalias = &rp.rhs[psp.nrhs]
                for (i = 0; i < psp.nrhs; i++):
                    rp.rhs[i] = psp.rhs[i]
                    rp.rhsalias[i] = psp.alias[i]

                rp.lhs = psp.lhs
                rp.lhsalias = psp.lhsalias
                rp.nrhs = psp.nrhs
                rp.code = 0
                rp.precsym = 0
                rp.index = psp.gp.nrule++
                rp.nextlhs = rp.lhs.rule
                rp.lhs.rule = rp
                rp.next = 0
                if psp.firstrule == 0:
                    psp.firstrule = (psp.lastrule = rp)
                else:
                    psp.lastrule.next = rp
                    psp.lastrule = rp

                psp.prevrule = rp

            psp.state = WAITING_FOR_DECL_OR_RULE
        elif (__ctype_b_loc()[00])[x[0]] & (_ISalpha):
            if psp.nrhs >= 1000:
                ErrorMsg(psp.filename, psp.tokenlineno, "Too many symbols on RHS of rule beginning at \"%s\".", x)
                psp.errorcnt += 1
                psp.state = RESYNC_AFTER_RULE_ERROR
            else:
                psp.rhs[psp.nrhs] = Symbol_new(x)
                psp.alias[psp.nrhs] = 0
                psp.nrhs += 1

        elif ((x[0] == '|') or (x[0] == '/')) and (psp.nrhs > 0):
            msp = psp.rhs[psp.nrhs - 1]
            if msp.type != MULTITERMINAL:
                origsp = msp
                msp = calloc(1, sizeof(msp[00]))
                memset(msp, 0, sizeof(msp[00]))
                msp.type = MULTITERMINAL
                msp.nsubsym = 1
                msp.subsym = calloc(1, sizeof())
                msp.subsym[0] = origsp
                msp.name = origsp.name
                psp.rhs[psp.nrhs - 1] = msp

            msp.nsubsym += 1
            msp.subsym = realloc(msp.subsym, (sizeof()) * msp.nsubsym)
            msp.subsym[msp.nsubsym - 1] = Symbol_new(&x[1])
            if ((__ctype_b_loc()[00])[x[1]] & (_ISlower)) or ((__ctype_b_loc()[00])[msp.subsym[0].name[0]] & (_ISlower)):
                ErrorMsg(psp.filename, psp.tokenlineno, "Cannot form a compound containing a non-terminal")
                psp.errorcnt += 1

        elif (x[0] == '(') and (psp.nrhs > 0):
            psp.state = RHS_ALIAS_1
        else:
            ErrorMsg(psp.filename, psp.tokenlineno, "Illegal character on RHS of rule: \"%s\".", x)
            psp.errorcnt += 1
            psp.state = RESYNC_AFTER_RULE_ERROR

        break

    @case RHS_ALIAS_1:
        if (__ctype_b_loc()[00])[x[0]] & (_ISalpha):
            psp.alias[psp.nrhs - 1] = x
            psp.state = RHS_ALIAS_2
        else:
            ErrorMsg(psp.filename, psp.tokenlineno, "\"%s\" is not a valid alias for the RHS symbol \"%s\"\n", x, psp.rhs[psp.nrhs - 1].name)
            psp.errorcnt += 1
            psp.state = RESYNC_AFTER_RULE_ERROR

        break

    @case RHS_ALIAS_2:
        if x[0] == ')':
            psp.state = IN_RHS
        else:
            ErrorMsg(psp.filename, psp.tokenlineno, "Missing \")\" following LHS alias name \"%s\".", psp.lhsalias)
            psp.errorcnt += 1
            psp.state = RESYNC_AFTER_RULE_ERROR

        break

    @case WAITING_FOR_DECL_KEYWORD:
        if (__ctype_b_loc()[00])[x[0]] & (_ISalpha):
            psp.declkeyword = x
            psp.declargslot = 0
            psp.insertLineMacro = 1
            psp.state = WAITING_FOR_DECL_ARG
            if strcmp(x, "name") == 0:
                psp.declargslot = &psp.gp.name
                psp.insertLineMacro = 0
            elif strcmp(x, "include") == 0:
                psp.declargslot = &psp.gp.include
            elif strcmp(x, "code") == 0:
                psp.declargslot = &psp.gp.extracode
            elif strcmp(x, "token_destructor") == 0:
                psp.declargslot = &psp.gp.tokendest
            elif strcmp(x, "default_destructor") == 0:
                psp.declargslot = &psp.gp.vardest
            elif strcmp(x, "token_prefix") == 0:
                psp.declargslot = &psp.gp.tokenprefix
                psp.insertLineMacro = 0
            elif strcmp(x, "syntax_error") == 0:
                psp.declargslot = &psp.gp.error
            elif strcmp(x, "parse_accept") == 0:
                psp.declargslot = &psp.gp.accept
            elif strcmp(x, "parse_failure") == 0:
                psp.declargslot = &psp.gp.failure
            elif strcmp(x, "stack_overflow") == 0:
                psp.declargslot = &psp.gp.overflow
            elif strcmp(x, "extra_argument") == 0:
                psp.declargslot = &psp.gp.arg
                psp.insertLineMacro = 0
            elif strcmp(x, "token_type") == 0:
                psp.declargslot = &psp.gp.tokentype
                psp.insertLineMacro = 0
            elif strcmp(x, "default_type") == 0:
                psp.declargslot = &psp.gp.vartype
                psp.insertLineMacro = 0
            elif strcmp(x, "stack_size") == 0:
                psp.declargslot = &psp.gp.stacksize
                psp.insertLineMacro = 0
            elif strcmp(x, "start_symbol") == 0:
                psp.declargslot = &psp.gp.start
                psp.insertLineMacro = 0
            elif strcmp(x, "left") == 0:
                psp.preccounter += 1
                psp.declassoc = LEFT
                psp.state = WAITING_FOR_PRECEDENCE_SYMBOL
            elif strcmp(x, "right") == 0:
                psp.preccounter += 1
                psp.declassoc = RIGHT
                psp.state = WAITING_FOR_PRECEDENCE_SYMBOL
            elif strcmp(x, "nonassoc") == 0:
                psp.preccounter += 1
                psp.declassoc = NONE
                psp.state = WAITING_FOR_PRECEDENCE_SYMBOL
            elif strcmp(x, "destructor") == 0:
                psp.state = WAITING_FOR_DESTRUCTOR_SYMBOL
            elif strcmp(x, "type") == 0:
                psp.state = WAITING_FOR_DATATYPE_SYMBOL
            elif strcmp(x, "fallback") == 0:
                psp.fallback = 0
                psp.state = WAITING_FOR_FALLBACK_ID
            elif strcmp(x, "wildcard") == 0:
                psp.state = WAITING_FOR_WILDCARD_ID
            else:
                ErrorMsg(psp.filename, psp.tokenlineno, "Unknown declaration keyword: \"%%%s\".", x)
                psp.errorcnt += 1
                psp.state = RESYNC_AFTER_DECL_ERROR

        else:
            ErrorMsg(psp.filename, psp.tokenlineno, "Illegal declaration keyword: \"%s\".", x)
            psp.errorcnt += 1
            psp.state = RESYNC_AFTER_DECL_ERROR

        break

    @case WAITING_FOR_DESTRUCTOR_SYMBOL:
        if not ((__ctype_b_loc()[00])[x[0]] & (_ISalpha)):
            ErrorMsg(psp.filename, psp.tokenlineno, "Symbol name missing after %destructor keyword")
            psp.errorcnt += 1
            psp.state = RESYNC_AFTER_DECL_ERROR
        else:
            sp = Symbol_new(x)
            psp.declargslot = &sp.destructor
            psp.insertLineMacro = 1
            psp.state = WAITING_FOR_DECL_ARG

        break

    @case WAITING_FOR_DATATYPE_SYMBOL:
        if not ((__ctype_b_loc()[00])[x[0]] & (_ISalpha)):
            ErrorMsg(psp.filename, psp.tokenlineno, "Symbol name missing after %destructor keyword")
            psp.errorcnt += 1
            psp.state = RESYNC_AFTER_DECL_ERROR
        else:
            sp = Symbol_new(x)
            psp.declargslot = &sp.datatype
            psp.insertLineMacro = 0
            psp.state = WAITING_FOR_DECL_ARG

        break

    @case WAITING_FOR_PRECEDENCE_SYMBOL:
        if x[0] == '.':
            psp.state = WAITING_FOR_DECL_OR_RULE
        elif (__ctype_b_loc()[00])[x[0]] & (_ISupper):
            sp = Symbol_new(x)
            if sp.prec >= 0:
                ErrorMsg(psp.filename, psp.tokenlineno, "Symbol \"%s\" has already be given a precedence.", x)
                psp.errorcnt += 1
            else:
                sp.prec = psp.preccounter
                sp.assoc = psp.declassoc

        else:
            ErrorMsg(psp.filename, psp.tokenlineno, "Can't assign a precedence to \"%s\".", x)
            psp.errorcnt += 1

        break

    @case WAITING_FOR_DECL_ARG:
        if ((x[0] == '{') or (x[0] == '\"')) or ((__ctype_b_loc()[00])[x[0]] & (_ISalnum)):
            zNew = x
            if (zNew[0] == '"') or (zNew[0] == '{'):
                zNew += 1

            nNew = strlen(zNew)
            if psp.declargslot[00]:
                zOld = psp.declargslot[00]
            else:
                zOld = ""

            nOld = strlen(zOld)
            n = (nOld + nNew) + 20
            if psp.insertLineMacro:
                for (z = psp.filename, nBack = 0; z[00]; z++):
                    if (z[00]) == '\\':
                        nBack += 1


                sprintf(zLine, "#line %d ", psp.tokenlineno)
                nLine = strlen(zLine)
                n += (nLine + strlen(psp.filename)) + nBack

            psp.declargslot[00] = (zBuf = realloc(psp.declargslot[00], n))
            zBuf += nOld
            if psp.insertLineMacro:
                if nOld and (zBuf[-1] != '\n'):
                    (zBuf++)[00] = '\n'

                memcpy(zBuf, zLine, nLine)
                zBuf += nLine
                (zBuf++)[00] = '"'
                for (z = psp.filename; z[00]; z++):
                    if (z[00]) == '\\':
                        (zBuf++)[00] = '\\'

                    (zBuf++)[00] = z[00]

                (zBuf++)[00] = '"'
                (zBuf++)[00] = '\n'

            memcpy(zBuf, zNew, nNew)
            zBuf += nNew
            zBuf[00] = 0
            psp.state = WAITING_FOR_DECL_OR_RULE
        else:
            ErrorMsg(psp.filename, psp.tokenlineno, "Illegal argument to %%%s: %s", psp.declkeyword, x)
            psp.errorcnt += 1
            psp.state = RESYNC_AFTER_DECL_ERROR

        break

    @case WAITING_FOR_FALLBACK_ID:
        if x[0] == '.':
            psp.state = WAITING_FOR_DECL_OR_RULE
        elif not ((__ctype_b_loc()[00])[x[0]] & (_ISupper)):
            ErrorMsg(psp.filename, psp.tokenlineno, "%%fallback argument \"%s\" should be a token", x)
            psp.errorcnt += 1
        else:
            sp = Symbol_new(x)
            if psp.fallback == 0:
                psp.fallback = sp
            elif sp.fallback:
                ErrorMsg(psp.filename, psp.tokenlineno, "More than one fallback assigned to token %s", x)
                psp.errorcnt += 1
            else:
                sp.fallback = psp.fallback
                psp.gp.has_fallback = 1


        break

    @case WAITING_FOR_WILDCARD_ID:
        if x[0] == '.':
            psp.state = WAITING_FOR_DECL_OR_RULE
        elif not ((__ctype_b_loc()[00])[x[0]] & (_ISupper)):
            ErrorMsg(psp.filename, psp.tokenlineno, "%%wildcard argument \"%s\" should be a token", x)
            psp.errorcnt += 1
        else:
            sp = Symbol_new(x)
            if psp.gp.wildcard == 0:
                psp.gp.wildcard = sp
            else:
                ErrorMsg(psp.filename, psp.tokenlineno, "Extra wildcard to token: %s", x)
                psp.errorcnt += 1


        break

    @case RESYNC_AFTER_RULE_ERROR:

    @case RESYNC_AFTER_DECL_ERROR:
        if x[0] == '.':
            psp.state = WAITING_FOR_DECL_OR_RULE

        if x[0] == '%':
            psp.state = WAITING_FOR_DECL_KEYWORD

        break



def preprocess_input(z):
    exclude = 0
    start = 0
    lineno = 1
    start_lineno = 1
    for (i = 0; z[i]; i++):
        if z[i] == '\n':
            lineno += 1

        if (z[i] != '%') or ((i > 0) and (z[i - 1] != '\n')):
            continue

        if (strncmp(&z[i], "%endif", 6) == 0) and ((__ctype_b_loc()[00])[z[i + 6]] & (_ISspace)):
            if exclude:
                exclude -= 1
                if exclude == 0:
                    for (j = start; j < i; j++):
                        if z[j] != '\n':
                        z[j] = ' '




            for (j = i; z[j] and (z[j] != '\n'); j++):
                z[j] = ' '

        elif ((strncmp(&z[i], "%ifdef", 6) == 0) and ((__ctype_b_loc()[00])[z[i + 6]] & (_ISspace))) or ((strncmp(&z[i], "%ifndef", 7) == 0) and ((__ctype_b_loc()[00])[z[i + 7]] & (_ISspace))):
            if exclude:
                exclude += 1
            else:
                for (j = i + 7; (__ctype_b_loc()[00])[z[j]] & (_ISspace); j++):
                    pass

                for (n = 0; z[j + n] and (not ((__ctype_b_loc()[00])[z[j + n]] & (_ISspace))); n++):
                    pass

                exclude = 1
                for (k = 0; k < nDefine; k++):
                    if (strncmp(azDefine[k], &z[j], n) == 0) and (strlen(azDefine[k]) == n):
                        exclude = 0
                        break


                if z[i + 3] == 'n':
                    exclude = not exclude

                if exclude:
                    start = i
                    start_lineno = lineno


            for (j = i; z[j] and (z[j] != '\n'); j++):
                z[j] = ' '



    if exclude:
        fprintf(stderr, "unterminated %%ifdef starting on line %d\n", start_lineno)
        exit(1)


def Parse(gp):
    startline = 0
    memset(&ps, '\0', sizeof(ps))
    ps.gp = gp
    ps.filename = gp.filename
    ps.errorcnt = 0
    ps.state = INITIALIZE
    fp = fopen(ps.filename, "rb")
    if fp == 0:
        ErrorMsg(ps.filename, 0, "Can't open this file for reading.")
        gp.errorcnt += 1
        return

    fseek(fp, 0, 2)
    filesize = ftell(fp)
    rewind(fp)
    filebuf = malloc(filesize + 1)
    if filebuf == 0:
        ErrorMsg(ps.filename, 0, "Can't allocate %d of memory to hold this file.", filesize + 1)
        gp.errorcnt += 1
        return

    if fread(filebuf, 1, filesize, fp) != filesize:
        ErrorMsg(ps.filename, 0, "Can't read in all %d bytes of this file.", filesize)
        free(filebuf)
        gp.errorcnt += 1
        return

    fclose(fp)
    filebuf[filesize] = 0
    preprocess_input(filebuf)
    lineno = 1
    for (cp = filebuf; (c = cp[00]) != 0;):
        if c == '\n':
            lineno += 1

        if (__ctype_b_loc()[00])[c] & (_ISspace):
            cp += 1
            continue

        if (c == '/') and (cp[1] == '/'):
            cp += 2
            while ((c = cp[00]) != 0) and (c != '\n'):
                cp += 1

            continue

        if (c == '/') and (cp[1] == '*'):
            cp += 2
            while ((c = cp[00]) != 0) and ((c != '/') or (cp[-1] != '*')):
                if c == '\n':
                    lineno += 1

                cp += 1

            if c:
                cp += 1

            continue

        ps.tokenstart = cp
        ps.tokenlineno = lineno
        if c == '\"':
            cp += 1
            while ((c = cp[00]) != 0) and (c != '\"'):
                if c == '\n':
                    lineno += 1

                cp += 1

            if c == 0:
                ErrorMsg(ps.filename, startline, "String starting on this line is not terminated before the end of the file.")
                ps.errorcnt += 1
                nextcp = cp
            else:
                nextcp = cp + 1

        elif c == '{':
            cp += 1
            for (level = 1; ((c = cp[00]) != 0) and ((level > 1) or (c != '}')); cp++):
                if c == '\n':
                    lineno += 1
                elif c == '{':
                    level += 1
                elif c == '}':
                    level -= 1
                elif (c == '/') and (cp[1] == '*'):
                    cp = &cp[2]
                    prevc = 0
                    while ((c = cp[00]) != 0) and ((c != '/') or (prevc != '*')):
                        if c == '\n':
                            lineno += 1

                        prevc = c
                        cp += 1

                elif (c == '/') and (cp[1] == '/'):
                    cp = &cp[2]
                    while ((c = cp[00]) != 0) and (c != '\n'):
                        cp += 1

                    if c:
                        lineno += 1

                elif (c == '\'') or (c == '\"'):
                    startchar = c
                    prevc = 0
                    for (cp++; ((c = cp[00]) != 0) and ((c != startchar) or (prevc == '\\')); cp++):
                        if c == '\n':
                            lineno += 1

                        if prevc == '\\':
                            prevc = 0
                        else:
                            prevc = c




            if c == 0:
                ErrorMsg(ps.filename, ps.tokenlineno, "C code starting on this line is not terminated before the end of the file.")
                ps.errorcnt += 1
                nextcp = cp
            else:
                nextcp = cp + 1

        elif (__ctype_b_loc()[00])[c] & (_ISalnum):
            while ((c = cp[00]) != 0) and (((__ctype_b_loc()[00])[c] & (_ISalnum)) or (c == '_')):
                cp += 1

            nextcp = cp
        elif ((c == ':') and (cp[1] == ':')) and (cp[2] == '='):
            cp += 3
            nextcp = cp
        elif ((c == '/') or (c == '|')) and ((__ctype_b_loc()[00])[cp[1]] & (_ISalpha)):
            cp += 2
            while ((c = cp[00]) != 0) and (((__ctype_b_loc()[00])[c] & (_ISalnum)) or (c == '_')):
                cp += 1

            nextcp = cp
        else:
            cp += 1
            nextcp = cp

        c = cp[00]
        cp[00] = 0
        parseonetoken(&ps)
        cp[00] = c
        cp = nextcp

    free(filebuf)
    gp.rule = ps.firstrule
    gp.errorcnt = ps.errorcnt


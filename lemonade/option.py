
argv = None
op = None
errstream = None
def errline(n, k, err):
    if argv[0]:
        fprintf(err, "%s", argv[0])

    spcnt = strlen(argv[0]) + 1
    for (i = 1; (i < n) and argv[i]; i++):
        fprintf(err, " %s", argv[i])
        spcnt += strlen(argv[i]) + 1

    spcnt += k
    for (; argv[i]; i++):
        fprintf(err, " %s", argv[i])

    if spcnt < 20:
        fprintf(err, "\n%*s^-- here\n", spcnt, "")
    else:
        fprintf(err, "\n%*shere --^\n", spcnt - 7, "")


def argindex(n):
    dashdash = 0
    if (argv != 0) and ((argv[00]) != 0):
        for (i = 1; argv[i]; i++):
            if dashdash or (not (((argv[i][0] == '-') or (argv[i][0] == '+')) or (strchr(argv[i], '=') != 0))):
                if n == 0:
                    return i

                n -= 1

            if strcmp(argv[i], "--") == 0:
                dashdash = 1



    return -1

emsg = "Command line syntax error: "
def handleflags(i, err):
    errcnt = 0
    for (j = 0; op[j].label; j++):
        if strncmp(&argv[i][1], op[j].label, strlen(op[j].label)) == 0:
            break


    v = 1 if argv[i][0] == '-' else 0
    if op[j].label == 0:
        if err:
            fprintf(err, "%sundefined option.\n", emsg)
            errline(i, 1, err)

        errcnt += 1
    elif op[j].type == OPT_FLAG:
        (op[j].arg)[00] = v
    elif op[j].type == OPT_FFLAG:
        ((op[j].arg)[00])(v)
    elif op[j].type == OPT_FSTR:
        ((op[j].arg)[00])(&argv[i][2])
    else:
        if err:
            fprintf(err, "%smissing argument on switch.\n", emsg)
            errline(i, 1, err)

        errcnt += 1

    return errcnt

def handleswitch(i, err):
    lv = 0
    dv = 0.0
    sv = 0
    errcnt = 0
    cp = strchr(argv[i], '=')
    _assert(cp != 0)
    cp[00] = 0
    for (j = 0; op[j].label; j++):
        if strcmp(argv[i], op[j].label) == 0:
            break


    cp[00] = '='
    if op[j].label == 0:
        if err:
            fprintf(err, "%sundefined option.\n", emsg)
            errline(i, 0, err)

        errcnt += 1
    else:
        cp += 1
        @switch op[j].type:
        @case OPT_FLAG:

        @case OPT_FFLAG:
            if err:
                fprintf(err, "%soption requires an argument.\n", emsg)
                errline(i, 0, err)

            errcnt += 1
            break

        @case OPT_DBL:

        @case OPT_FDBL:
            dv = strtod(cp, &end)
            if end[00]:
                if err:
                    fprintf(err, "%sillegal character in floating-point argument.\n", emsg)
                    errline(i, (end) - (argv[i]), err)

                errcnt += 1

            break

        @case OPT_INT:

        @case OPT_FINT:
            lv = strtol(cp, &end, 0)
            if end[00]:
                if err:
                    fprintf(err, "%sillegal character in integer argument.\n", emsg)
                    errline(i, (end) - (argv[i]), err)

                errcnt += 1

            break

        @case OPT_STR:

        @case OPT_FSTR:
            sv = cp
            break


        @switch op[j].type:
        @case OPT_FLAG:

        @case OPT_FFLAG:
            break

        @case OPT_DBL:
            (op[j].arg)[00] = dv
            break

        @case OPT_FDBL:
            ((op[j].arg)[00])(dv)
            break

        @case OPT_INT:
            (op[j].arg)[00] = lv
            break

        @case OPT_FINT:
            ((op[j].arg)[00])(lv)
            break

        @case OPT_STR:
            (op[j].arg)[00] = sv
            break

        @case OPT_FSTR:
            ((op[j].arg)[00])(sv)
            break



    return errcnt

def OptInit(a, o, err):
    errcnt = 0
    argv = a
    op = o
    errstream = err
    if (argv and (argv[00])) and op:
        for (i = 1; argv[i]; i++):
            if (argv[i][0] == '+') or (argv[i][0] == '-'):
                errcnt += handleflags(i, err)
            elif strchr(argv[i], '='):
                errcnt += handleswitch(i, err)



    if errcnt > 0:
        fprintf(err, "Valid command line options for \"%s\" are:\n", a[00])
        OptPrint()
        exit(1)

    return 0

def OptNArgs():
    cnt = 0
    dashdash = 0
    if (argv != 0) and (argv[0] != 0):
        for (i = 1; argv[i]; i++):
            if dashdash or (not (((argv[i][0] == '-') or (argv[i][0] == '+')) or (strchr(argv[i], '=') != 0))):
                cnt += 1

            if strcmp(argv[i], "--") == 0:
                dashdash = 1



    return cnt

def OptArg(n):
    i = argindex(n)
    return argv[i] if i >= 0 else 0

def OptErr(n):
    i = argindex(n)
    if i >= 0:
        errline(i, 0, errstream)


def OptPrint():
    max = 0
    for (i = 0; op[i].label; i++):
        len = strlen(op[i].label) + 1
        @switch op[i].type:
        @case OPT_FLAG:

        @case OPT_FFLAG:
            break

        @case OPT_INT:

        @case OPT_FINT:
            len += 9
            break

        @case OPT_DBL:

        @case OPT_FDBL:
            len += 6
            break

        @case OPT_STR:

        @case OPT_FSTR:
            len += 8
            break


        if len > max:
            max = len


    for (i = 0; op[i].label; i++):
        @switch op[i].type:
        @case OPT_FLAG:

        @case OPT_FFLAG:
            fprintf(errstream, "  -%-*s  %s\n", max, op[i].label, op[i].message)
            break

        @case OPT_INT:

        @case OPT_FINT:
            fprintf(errstream, "  %s=<integer>%*s  %s\n", op[i].label, (max - strlen(op[i].label)) - 9, "", op[i].message)
            break

        @case OPT_DBL:

        @case OPT_FDBL:
            fprintf(errstream, "  %s=<real>%*s  %s\n", op[i].label, (max - strlen(op[i].label)) - 6, "", op[i].message)
            break

        @case OPT_STR:

        @case OPT_FSTR:
            fprintf(errstream, "  %s=<string>%*s  %s\n", op[i].label, (max - strlen(op[i].label)) - 8, "", op[i].message)
            break





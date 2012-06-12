

def acttab_free(p):
    free(p.aAction)
    free(p.aLookahead)
    free(p)

def acttab_alloc():
    p = calloc(1, sizeof(p[00]))
    if p == 0:
        fprintf(stderr, "Unable to allocate memory for a new acttab.")
        exit(1)

    memset(p, 0, sizeof(p[00]))
    return p

def acttab_action(p, lookahead, action):
    if p.nLookahead >= p.nLookaheadAlloc:
        p.nLookaheadAlloc += 25
        p.aLookahead = realloc(p.aLookahead, (sizeof(p.aLookahead[0])) * p.nLookaheadAlloc)
        if p.aLookahead == 0:
            fprintf(stderr, "malloc failed\n")
            exit(1)


    if p.nLookahead == 0:
        p.mxLookahead = lookahead
        p.mnLookahead = lookahead
        p.mnAction = action
    else:
        if p.mxLookahead < lookahead:
            p.mxLookahead = lookahead

        if p.mnLookahead > lookahead:
            p.mnLookahead = lookahead
            p.mnAction = action


    p.aLookahead[p.nLookahead].lookahead = lookahead
    p.aLookahead[p.nLookahead].action = action
    p.nLookahead += 1

def acttab_insert(p):
    _assert(p.nLookahead > 0)
    n = p.mxLookahead + 1
    if (p.nAction + n) >= p.nActionAlloc:
        oldAlloc = p.nActionAlloc
        p.nActionAlloc = ((p.nAction + n) + p.nActionAlloc) + 20
        p.aAction = realloc(p.aAction, (sizeof(p.aAction[0])) * p.nActionAlloc)
        if p.aAction == 0:
            fprintf(stderr, "malloc failed\n")
            exit(1)

        for (i = oldAlloc; i < p.nActionAlloc; i++):
            p.aAction[i].lookahead = -1
            p.aAction[i].action = -1


    for (i = 0; i < (p.nAction + p.mnLookahead); i++):
        if p.aAction[i].lookahead < 0:
            for (j = 0; j < p.nLookahead; j++):
                k = (p.aLookahead[j].lookahead - p.mnLookahead) + i
                if k < 0:
                    break

                if p.aAction[k].lookahead >= 0:
                    break


            if j < p.nLookahead:
                continue

            for (j = 0; j < p.nAction; j++):
                if p.aAction[j].lookahead == ((j + p.mnLookahead) - i):
                    break


            if j == p.nAction:
                break

        elif p.aAction[i].lookahead == p.mnLookahead:
            if p.aAction[i].action != p.mnAction:
                continue

            for (j = 0; j < p.nLookahead; j++):
                k = (p.aLookahead[j].lookahead - p.mnLookahead) + i
                if (k < 0) or (k >= p.nAction):
                    break

                if p.aLookahead[j].lookahead != p.aAction[k].lookahead:
                    break

                if p.aLookahead[j].action != p.aAction[k].action:
                    break


            if j < p.nLookahead:
                continue

            n = 0
            for (j = 0; j < p.nAction; j++):
                if p.aAction[j].lookahead < 0:
                    continue

                if p.aAction[j].lookahead == ((j + p.mnLookahead) - i):
                    n += 1


            if n == p.nLookahead:
                break



    for (j = 0; j < p.nLookahead; j++):
        k = (p.aLookahead[j].lookahead - p.mnLookahead) + i
        p.aAction[k] = p.aLookahead[j]
        if k >= p.nAction:
            p.nAction = k + 1


    p.nLookahead = 0
    return i - p.mnLookahead



freelist = 0
current = 0
currentend = 0
basis = 0
basisend = 0
def newconfig():
    if freelist == 0:
        amt = 3
        freelist = calloc(amt, sizeof())
        if freelist == 0:
            fprintf(stderr, "Unable to allocate memory for a new configuration.")
            exit(1)

        for (i = 0; i < (amt - 1); i++):
            freelist[i].next = &freelist[i + 1]

        freelist[amt - 1].next = 0

    new = freelist
    freelist = freelist.next
    return new

def deleteconfig(old):
    old.next = freelist
    freelist = old

def Configlist_init():
    current = 0
    currentend = &current
    basis = 0
    basisend = &basis
    Configtable_init()
    return

def Configlist_reset():
    current = 0
    currentend = &current
    basis = 0
    basisend = &basis
    Configtable_clear(0)
    return

def Configlist_add(rp, dot):
    _assert(currentend != 0)
    model.rp = rp
    model.dot = dot
    cfp = Configtable_find(&model)
    if cfp == 0:
        cfp = newconfig()
        cfp.rp = rp
        cfp.dot = dot
        cfp.fws = SetNew()
        cfp.stp = 0
        cfp.fplp = (cfp.bplp = 0)
        cfp.next = 0
        cfp.bp = 0
        currentend[00] = cfp
        currentend = &cfp.next
        Configtable_insert(cfp)

    return cfp

def Configlist_addbasis(rp, dot):
    _assert(basisend != 0)
    _assert(currentend != 0)
    model.rp = rp
    model.dot = dot
    cfp = Configtable_find(&model)
    if cfp == 0:
        cfp = newconfig()
        cfp.rp = rp
        cfp.dot = dot
        cfp.fws = SetNew()
        cfp.stp = 0
        cfp.fplp = (cfp.bplp = 0)
        cfp.next = 0
        cfp.bp = 0
        currentend[00] = cfp
        currentend = &cfp.next
        basisend[00] = cfp
        basisend = &cfp.bp
        Configtable_insert(cfp)

    return cfp

def Configlist_closure(lemp):
    _assert(currentend != 0)
    for (cfp = current; cfp; cfp = cfp.next):
        rp = cfp.rp
        dot = cfp.dot
        if dot >= rp.nrhs:
            continue

        sp = rp.rhs[dot]
        if sp.type == NONTERMINAL:
            if (sp.rule == 0) and (sp != lemp.errsym):
                ErrorMsg(lemp.filename, rp.line, "Nonterminal \"%s\" has no rules.", sp.name)
                lemp.errorcnt += 1

            for (newrp = sp.rule; newrp; newrp = newrp.nextlhs):
                newcfp = Configlist_add(newrp, 0)
                for (i = dot + 1; i < rp.nrhs; i++):
                    xsp = rp.rhs[i]
                    if xsp.type == TERMINAL:
                        SetAdd(newcfp.fws, xsp.index)
                        break
                    elif xsp.type == MULTITERMINAL:
                        for (k = 0; k < xsp.nsubsym; k++):
                            SetAdd(newcfp.fws, xsp.subsym[k].index)

                        break
                    else:
                        SetUnion(newcfp.fws, xsp.firstset)
                        if xsp._lambda == False:
                            break



                if i == rp.nrhs:
                    Plink_add(&cfp.fplp, newcfp)




    return

def Configlist_sort():
    current = msort(current, &current.next, Configcmp)
    currentend = 0
    return

def Configlist_sortbasis():
    basis = msort(current, &current.bp, Configcmp)
    basisend = 0
    return

def Configlist_return():
    old = current
    current = 0
    currentend = 0
    return old

def Configlist_basis():
    old = basis
    basis = 0
    basisend = 0
    return old

def Configlist_eat(cfp):
    for (; cfp; cfp = nextcfp):
        nextcfp = cfp.next
        _assert(cfp.fplp == 0)
        _assert(cfp.bplp == 0)
        if cfp.fws:
            SetFree(cfp.fws)

        deleteconfig(cfp)

    return


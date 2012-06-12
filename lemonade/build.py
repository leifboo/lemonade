
def FindRulePrecedences(xp):
    for (rp = xp.rule; rp; rp = rp.next):
        if rp.precsym == 0:
            for (i = 0; (i < rp.nrhs) and (rp.precsym == 0); i++):
                sp = rp.rhs[i]
                if sp.type == MULTITERMINAL:
                    for (j = 0; j < sp.nsubsym; j++):
                        if sp.subsym[j].prec >= 0:
                            rp.precsym = sp.subsym[j]
                            break


                elif sp.prec >= 0:
                    rp.precsym = rp.rhs[i]




    return

def FindFirstSets(lemp):
    for (i = 0; i < lemp.nsymbol; i++):
        lemp.symbols[i]._lambda = False

    for (i = lemp.nterminal; i < lemp.nsymbol; i++):
        lemp.symbols[i].firstset = SetNew()


    _cond = 1
    while _cond:
        progress = 0
        for (rp = lemp.rule; rp; rp = rp.next):
            if rp.lhs._lambda:
                continue

            for (i = 0; i < rp.nrhs; i++):
                sp = rp.rhs[i]
                if (sp.type != TERMINAL) or (sp._lambda == False):
                    break


            if i == rp.nrhs:
                rp.lhs._lambda = True
                progress = 1


        _cond = progress
    _cond = 1
    while _cond:
        progress = 0
        for (rp = lemp.rule; rp; rp = rp.next):
            s1 = rp.lhs
            for (i = 0; i < rp.nrhs; i++):
                s2 = rp.rhs[i]
                if s2.type == TERMINAL:
                    progress += SetAdd(s1.firstset, s2.index)
                    break
                elif s2.type == MULTITERMINAL:
                    for (j = 0; j < s2.nsubsym; j++):
                        progress += SetAdd(s1.firstset, s2.subsym[j].index)

                    break
                elif s1 == s2:
                    if s1._lambda == False:
                        break

                else:
                    progress += SetUnion(s1.firstset, s2.firstset)
                    if s2._lambda == False:
                        break




        _cond = progress    return

def FindStates(lemp):
    Configlist_init()
    if lemp.start:
        sp = Symbol_find(lemp.start)
        if sp == 0:
            ErrorMsg(lemp.filename, 0, "The specified start symbol \"%s\" is not in a nonterminal of the grammar.  \"%s\" will be used as the start symbol instead.", lemp.start, lemp.rule.lhs.name)
            lemp.errorcnt += 1
            sp = lemp.rule.lhs

    else:
        sp = lemp.rule.lhs

    for (rp = lemp.rule; rp; rp = rp.next):
        for (i = 0; i < rp.nrhs; i++):
            if rp.rhs[i] == sp:
                ErrorMsg(lemp.filename, 0, "The start symbol \"%s\" occurs on the right-hand side of a rule. This will result in a parser which does not work properly.", sp.name)
                lemp.errorcnt += 1



    for (rp = sp.rule; rp; rp = rp.nextlhs):
        rp.lhsStart = 1
        newcfp = Configlist_addbasis(rp, 0)
        SetAdd(newcfp.fws, 0)

    getstate(lemp)
    return

def getstate(lemp):
    Configlist_sortbasis()
    bp = Configlist_basis()
    stp = State_find(bp)
    if stp:
        for (x = bp, y = stp.bp; x and y; x = x.bp, y = y.bp):
            Plink_copy(&y.bplp, x.bplp)
            Plink_delete(x.fplp)
            x.fplp = (x.bplp = 0)

        cfp = Configlist_return()
        Configlist_eat(cfp)
    else:
        Configlist_closure(lemp)
        Configlist_sort()
        cfp = Configlist_return()
        stp = State_new()
        if stp == 0:
            memory_error()

        pass
        stp.bp = bp
        stp.cfp = cfp
        stp.statenum = lemp.nstate++
        stp.ap = 0
        State_insert(stp, stp.bp)
        buildshifts(lemp, stp)

    return stp

def same_symbol(a, b):
    if a == b:
        return 1

    if a.type != MULTITERMINAL:
        return 0

    if b.type != MULTITERMINAL:
        return 0

    if a.nsubsym != b.nsubsym:
        return 0

    for (i = 0; i < a.nsubsym; i++):
        if a.subsym[i] != b.subsym[i]:
            return 0


    return 1

def buildshifts(lemp, stp):
    for (cfp = stp.cfp; cfp; cfp = cfp.next):
        cfp.status = INCOMPLETE

    for (cfp = stp.cfp; cfp; cfp = cfp.next):
        if cfp.status == COMPLETE:
            continue

        if cfp.dot >= cfp.rp.nrhs:
            continue

        Configlist_reset()
        sp = cfp.rp.rhs[cfp.dot]
        for (bcfp = cfp; bcfp; bcfp = bcfp.next):
            if bcfp.status == COMPLETE:
                continue

            if bcfp.dot >= bcfp.rp.nrhs:
                continue

            bsp = bcfp.rp.rhs[bcfp.dot]
            if not same_symbol(bsp, sp):
                continue

            bcfp.status = COMPLETE
            new = Configlist_addbasis(bcfp.rp, bcfp.dot + 1)
            Plink_add(&new.bplp, bcfp)

        newstp = getstate(lemp)
        if sp.type == MULTITERMINAL:
            for (i = 0; i < sp.nsubsym; i++):
                Action_add(&stp.ap, SHIFT, sp.subsym[i], newstp)

        else:
            Action_add(&stp.ap, SHIFT, sp, newstp)



def FindLinks(lemp):
    for (i = 0; i < lemp.nstate; i++):
        stp = lemp.sorted[i]
        for (cfp = stp.cfp; cfp; cfp = cfp.next):
            cfp.stp = stp


    for (i = 0; i < lemp.nstate; i++):
        stp = lemp.sorted[i]
        for (cfp = stp.cfp; cfp; cfp = cfp.next):
            for (plp = cfp.bplp; plp; plp = plp.next):
                other = plp.cfp
                Plink_add(&other.fplp, cfp)




def FindFollowSets(lemp):
    for (i = 0; i < lemp.nstate; i++):
        for (cfp = lemp.sorted[i].cfp; cfp; cfp = cfp.next):
            cfp.status = INCOMPLETE



    _cond = 1
    while _cond:
        progress = 0
        for (i = 0; i < lemp.nstate; i++):
            for (cfp = lemp.sorted[i].cfp; cfp; cfp = cfp.next):
                if cfp.status == COMPLETE:
                    continue

                for (plp = cfp.fplp; plp; plp = plp.next):
                    change = SetUnion(plp.cfp.fws, cfp.fws)
                    if change:
                        plp.cfp.status = INCOMPLETE
                        progress = 1


                cfp.status = COMPLETE


        _cond = progress
def FindActions(lemp):
    for (i = 0; i < lemp.nstate; i++):
        stp = lemp.sorted[i]
        for (cfp = stp.cfp; cfp; cfp = cfp.next):
            if cfp.rp.nrhs == cfp.dot:
                for (j = 0; j < lemp.nterminal; j++):
                    if cfp.fws[j]:
                        Action_add(&stp.ap, REDUCE, lemp.symbols[j], cfp.rp)





    if lemp.start:
        sp = Symbol_find(lemp.start)
        if sp == 0:
            sp = lemp.rule.lhs

    else:
        sp = lemp.rule.lhs

    Action_add(&lemp.sorted[0].ap, ACCEPT, sp, 0)
    for (i = 0; i < lemp.nstate; i++):
        stp = lemp.sorted[i]
        stp.ap = Action_sort(stp.ap)
        for (ap = stp.ap; ap and ap.next; ap = ap.next):
            for (nap = ap.next; nap and (nap.sp == ap.sp); nap = nap.next):
                lemp.nconflict += resolve_conflict(ap, nap, lemp.errsym)



    for (rp = lemp.rule; rp; rp = rp.next):
        rp.canReduce = False

    for (i = 0; i < lemp.nstate; i++):
        for (ap = lemp.sorted[i].ap; ap; ap = ap.next):
            if ap.type == REDUCE:
                ap.x.rp.canReduce = True



    for (rp = lemp.rule; rp; rp = rp.next):
        if rp.canReduce:
            continue

        ErrorMsg(lemp.filename, rp.ruleline, "This rule can not be reduced.\n")
        lemp.errorcnt += 1


def resolve_conflict(apx, apy, errsym):
    errcnt = 0
    _assert(apx.sp == apy.sp)
    if (apx.type == SHIFT) and (apy.type == SHIFT):
        apy.type = SSCONFLICT
        errcnt += 1

    if (apx.type == SHIFT) and (apy.type == REDUCE):
        spx = apx.sp
        spy = apy.x.rp.precsym
        if ((spy == 0) or (spx.prec < 0)) or (spy.prec < 0):
            apy.type = SRCONFLICT
            errcnt += 1
        elif spx.prec > spy.prec:
            apy.type = RD_RESOLVED
        elif spx.prec < spy.prec:
            apx.type = SH_RESOLVED
        elif (spx.prec == spy.prec) and (spx.assoc == RIGHT):
            apy.type = RD_RESOLVED
        elif (spx.prec == spy.prec) and (spx.assoc == LEFT):
            apx.type = SH_RESOLVED
        else:
            _assert((spx.prec == spy.prec) and (spx.assoc == NONE))
            apy.type = SRCONFLICT
            errcnt += 1

    elif (apx.type == REDUCE) and (apy.type == REDUCE):
        spx = apx.x.rp.precsym
        spy = apy.x.rp.precsym
        if ((((spx == 0) or (spy == 0)) or (spx.prec < 0)) or (spy.prec < 0)) or (spx.prec == spy.prec):
            apy.type = RRCONFLICT
            errcnt += 1
        elif spx.prec > spy.prec:
            apy.type = RD_RESOLVED
        elif spx.prec < spy.prec:
            apx.type = RD_RESOLVED

    else:
        _assert((((((((((apx.type == SH_RESOLVED) or (apx.type == RD_RESOLVED)) or (apx.type == SSCONFLICT)) or (apx.type == SRCONFLICT)) or (apx.type == RRCONFLICT)) or (apy.type == SH_RESOLVED)) or (apy.type == RD_RESOLVED)) or (apy.type == SSCONFLICT)) or (apy.type == SRCONFLICT)) or (apy.type == RRCONFLICT))

    return errcnt


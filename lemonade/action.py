
def Action_new():
    freelist = 0
    if freelist == 0:
        amt = 100
        freelist = calloc(amt, sizeof())
        if freelist == 0:
            fprintf(stderr, "Unable to allocate memory for a new parser action.")
            exit(1)

        for (i = 0; i < (amt - 1); i++):
            freelist[i].next = &freelist[i + 1]

        freelist[amt - 1].next = 0

    new = freelist
    freelist = freelist.next
    return new

def actioncmp(ap1, ap2):
    rc = ap1.sp.index - ap2.sp.index
    if rc == 0:
        rc = (ap1.type) - (ap2.type)

    if (rc == 0) and (ap1.type == REDUCE):
        rc = ap1.x.rp.index - ap2.x.rp.index

    return rc

def Action_sort(ap):
    ap = msort(ap, &ap.next, actioncmp)
    return ap

def Action_add(app, type, sp, arg):
    new = Action_new()
    new.next = app[00]
    app[00] = new
    new.type = type
    new.sp = sp
    if type == SHIFT:
        new.x.stp = arg
    else:
        new.x.rp = arg



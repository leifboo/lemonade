
plink_freelist = 0
def Plink_new():
    if plink_freelist == 0:
        amt = 100
        plink_freelist = calloc(amt, sizeof())
        if plink_freelist == 0:
            fprintf(stderr, "Unable to allocate memory for a new follow-set propagation link.\n")
            exit(1)

        for (i = 0; i < (amt - 1); i++):
            plink_freelist[i].next = &plink_freelist[i + 1]

        plink_freelist[amt - 1].next = 0

    new = plink_freelist
    plink_freelist = plink_freelist.next
    return new

def Plink_add(plpp, cfp):
    new = Plink_new()
    new.next = plpp[00]
    plpp[00] = new
    new.cfp = cfp

def Plink_copy(to, _from):
    while _from:
        nextpl = _from.next
        _from.next = to[00]
        to[00] = _from
        _from = nextpl


def Plink_delete(plp):
    while plp:
        nextpl = plp.next
        plp.next = plink_freelist
        plink_freelist = plp
        plp = nextpl



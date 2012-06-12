
def merge(a, b, cmp, offset):
    if a == 0:
        head = b
    elif b == 0:
        head = a
    else:
        if (cmp[00])(a, b) < 0:
            ptr = a
            a = ((a) + offset)[00]
        else:
            ptr = b
            b = ((b) + offset)[00]

        head = ptr
        while a and b:
            if (cmp[00])(a, b) < 0:
                ((ptr) + offset)[00] = a
                ptr = a
                a = ((a) + offset)[00]
            else:
                ((ptr) + offset)[00] = b
                ptr = b
                b = ((b) + offset)[00]


        if a:
            ((ptr) + offset)[00] = a
        else:
            ((ptr) + offset)[00] = b


    return head

def msort(list, next, cmp):
    offset = (next) - (list)
    for (i = 0; i < 30; i++):
        set[i] = 0

    while list:
        ep = list
        list = ((list) + offset)[00]
        ((ep) + offset)[00] = 0
        for (i = 0; (i < (30 - 1)) and (set[i] != 0); i++):
            ep = merge(ep, set[i], cmp, offset)
            set[i] = 0

        set[i] = ep

    ep = 0
    for (i = 0; i < 30; i++):
        if set[i]:
        ep = merge(ep, set[i], cmp, offset)


    return ep



def strhash(x):
    h = 0
    while x[00]:
        h = (h * 13) + ((x++)[00])

    return h

def Strsafe(y):
    if y == 0:
        return 0

    z = Strsafe_find(y)
    if (z == 0) and ((z = malloc(strlen(y) + 1)) != 0):
        strcpy(z, y)
        Strsafe_insert(z)

    if z == 0:
        memory_error()

    pass
    return z



x1a = None
def Strsafe_init():
    if x1a:
        return

    x1a = malloc(sizeof())
    if x1a:
        x1a.size = 1024
        x1a.count = 0
        x1a.tbl = malloc(((sizeof()) + (sizeof())) * 1024)
        if x1a.tbl == 0:
            free(x1a)
            x1a = 0
        else:
            x1a.ht = &x1a.tbl[1024]
            for (i = 0; i < 1024; i++):
                x1a.ht[i] = 0




def Strsafe_insert(data):
    if x1a == 0:
        return 0

    ph = strhash(data)
    h = ph & (x1a.size - 1)
    np = x1a.ht[h]
    while np:
        if strcmp(np.data, data) == 0:
            return 0

        np = np.next

    if x1a.count >= x1a.size:
        array.size = (size = x1a.size * 2)
        array.count = x1a.count
        array.tbl = malloc(((sizeof()) + (sizeof())) * size)
        if array.tbl == 0:
            return 0

        array.ht = &array.tbl[size]
        for (i = 0; i < size; i++):
            array.ht[i] = 0

        for (i = 0; i < x1a.count; i++):
            oldnp = &x1a.tbl[i]
            h = strhash(oldnp.data) & (size - 1)
            newnp = &array.tbl[i]
            if array.ht[h]:
                array.ht[h]._from = &newnp.next

            newnp.next = array.ht[h]
            newnp.data = oldnp.data
            newnp._from = &array.ht[h]
            array.ht[h] = newnp

        free(x1a.tbl)
        x1a[00] = array

    h = ph & (x1a.size - 1)
    np = &x1a.tbl[x1a.count++]
    np.data = data
    if x1a.ht[h]:
        x1a.ht[h]._from = &np.next

    np.next = x1a.ht[h]
    x1a.ht[h] = np
    np._from = &x1a.ht[h]
    return 1

def Strsafe_find(key):
    if x1a == 0:
        return 0

    h = strhash(key) & (x1a.size - 1)
    np = x1a.ht[h]
    while np:
        if strcmp(np.data, key) == 0:
            break

        np = np.next

    return np.data if np else 0

def Symbol_new(x):
    sp = Symbol_find(x)
    if sp == 0:
        sp = calloc(1, sizeof())
        if sp == 0:
            memory_error()

        pass
        sp.name = Strsafe(x)
        sp.type = TERMINAL if (__ctype_b_loc()[00])[x[00]] & (_ISupper) else NONTERMINAL
        sp.rule = 0
        sp.fallback = 0
        sp.prec = -1
        sp.assoc = UNK
        sp.firstset = 0
        sp._lambda = False
        sp.destructor = 0
        sp.datatype = 0
        sp.useCnt = 0
        Symbol_insert(sp, sp.name)

    sp.useCnt += 1
    return sp

def Symbolcmpp(a, b):
    i1 = ((a[00])[00]).index + (10000000 * (((a[00])[00]).name[0] > 'Z'))
    i2 = ((b[00])[00]).index + (10000000 * (((b[00])[00]).name[0] > 'Z'))
    return i1 - i2



x2a = None
def Symbol_init():
    if x2a:
        return

    x2a = malloc(sizeof())
    if x2a:
        x2a.size = 128
        x2a.count = 0
        x2a.tbl = malloc(((sizeof()) + (sizeof())) * 128)
        if x2a.tbl == 0:
            free(x2a)
            x2a = 0
        else:
            x2a.ht = &x2a.tbl[128]
            for (i = 0; i < 128; i++):
                x2a.ht[i] = 0




def Symbol_insert(data, key):
    if x2a == 0:
        return 0

    ph = strhash(key)
    h = ph & (x2a.size - 1)
    np = x2a.ht[h]
    while np:
        if strcmp(np.key, key) == 0:
            return 0

        np = np.next

    if x2a.count >= x2a.size:
        array.size = (size = x2a.size * 2)
        array.count = x2a.count
        array.tbl = malloc(((sizeof()) + (sizeof())) * size)
        if array.tbl == 0:
            return 0

        array.ht = &array.tbl[size]
        for (i = 0; i < size; i++):
            array.ht[i] = 0

        for (i = 0; i < x2a.count; i++):
            oldnp = &x2a.tbl[i]
            h = strhash(oldnp.key) & (size - 1)
            newnp = &array.tbl[i]
            if array.ht[h]:
                array.ht[h]._from = &newnp.next

            newnp.next = array.ht[h]
            newnp.key = oldnp.key
            newnp.data = oldnp.data
            newnp._from = &array.ht[h]
            array.ht[h] = newnp

        free(x2a.tbl)
        x2a[00] = array

    h = ph & (x2a.size - 1)
    np = &x2a.tbl[x2a.count++]
    np.key = key
    np.data = data
    if x2a.ht[h]:
        x2a.ht[h]._from = &np.next

    np.next = x2a.ht[h]
    x2a.ht[h] = np
    np._from = &x2a.ht[h]
    return 1

def Symbol_find(key):
    if x2a == 0:
        return 0

    h = strhash(key) & (x2a.size - 1)
    np = x2a.ht[h]
    while np:
        if strcmp(np.key, key) == 0:
            break

        np = np.next

    return np.data if np else 0

def Symbol_Nth(n):
    if (x2a and (n > 0)) and (n <= x2a.count):
        data = x2a.tbl[n - 1].data
    else:
        data = 0

    return data

def Symbol_count():
    return x2a.count if x2a else 0

def Symbol_arrayof():
    if x2a == 0:
        return 0

    size = x2a.count
    array = calloc(size, sizeof())
    if array:
        for (i = 0; i < size; i++):
            array[i] = x2a.tbl[i].data


    return array

def Configcmp(a, b):
    x = a.rp.index - b.rp.index
    if x == 0:
        x = a.dot - b.dot

    return x

def statecmp(a, b):
    for (rc = 0; ((rc == 0) and a) and b; a = a.bp, b = b.bp):
        rc = a.rp.index - b.rp.index
        if rc == 0:
            rc = a.dot - b.dot


    if rc == 0:
        if a:
            rc = 1

        if b:
            rc = -1


    return rc

def statehash(a):
    h = 0
    while a:
        h = ((h * 571) + (a.rp.index * 37)) + a.dot
        a = a.bp

    return h

def State_new():
    new = calloc(1, sizeof())
    if new == 0:
        memory_error()

    pass
    return new



x3a = None
def State_init():
    if x3a:
        return

    x3a = malloc(sizeof())
    if x3a:
        x3a.size = 128
        x3a.count = 0
        x3a.tbl = malloc(((sizeof()) + (sizeof())) * 128)
        if x3a.tbl == 0:
            free(x3a)
            x3a = 0
        else:
            x3a.ht = &x3a.tbl[128]
            for (i = 0; i < 128; i++):
                x3a.ht[i] = 0




def State_insert(data, key):
    if x3a == 0:
        return 0

    ph = statehash(key)
    h = ph & (x3a.size - 1)
    np = x3a.ht[h]
    while np:
        if statecmp(np.key, key) == 0:
            return 0

        np = np.next

    if x3a.count >= x3a.size:
        array.size = (size = x3a.size * 2)
        array.count = x3a.count
        array.tbl = malloc(((sizeof()) + (sizeof())) * size)
        if array.tbl == 0:
            return 0

        array.ht = &array.tbl[size]
        for (i = 0; i < size; i++):
            array.ht[i] = 0

        for (i = 0; i < x3a.count; i++):
            oldnp = &x3a.tbl[i]
            h = statehash(oldnp.key) & (size - 1)
            newnp = &array.tbl[i]
            if array.ht[h]:
                array.ht[h]._from = &newnp.next

            newnp.next = array.ht[h]
            newnp.key = oldnp.key
            newnp.data = oldnp.data
            newnp._from = &array.ht[h]
            array.ht[h] = newnp

        free(x3a.tbl)
        x3a[00] = array

    h = ph & (x3a.size - 1)
    np = &x3a.tbl[x3a.count++]
    np.key = key
    np.data = data
    if x3a.ht[h]:
        x3a.ht[h]._from = &np.next

    np.next = x3a.ht[h]
    x3a.ht[h] = np
    np._from = &x3a.ht[h]
    return 1

def State_find(key):
    if x3a == 0:
        return 0

    h = statehash(key) & (x3a.size - 1)
    np = x3a.ht[h]
    while np:
        if statecmp(np.key, key) == 0:
            break

        np = np.next

    return np.data if np else 0

def State_arrayof():
    if x3a == 0:
        return 0

    size = x3a.count
    array = malloc((sizeof()) * size)
    if array:
        for (i = 0; i < size; i++):
            array[i] = x3a.tbl[i].data


    return array

def confighash(a):
    h = 0
    h = ((h * 571) + (a.rp.index * 37)) + a.dot
    return h



x4a = None
def Configtable_init():
    if x4a:
        return

    x4a = malloc(sizeof())
    if x4a:
        x4a.size = 64
        x4a.count = 0
        x4a.tbl = malloc(((sizeof()) + (sizeof())) * 64)
        if x4a.tbl == 0:
            free(x4a)
            x4a = 0
        else:
            x4a.ht = &x4a.tbl[64]
            for (i = 0; i < 64; i++):
                x4a.ht[i] = 0




def Configtable_insert(data):
    if x4a == 0:
        return 0

    ph = confighash(data)
    h = ph & (x4a.size - 1)
    np = x4a.ht[h]
    while np:
        if Configcmp(np.data, data) == 0:
            return 0

        np = np.next

    if x4a.count >= x4a.size:
        array.size = (size = x4a.size * 2)
        array.count = x4a.count
        array.tbl = malloc(((sizeof()) + (sizeof())) * size)
        if array.tbl == 0:
            return 0

        array.ht = &array.tbl[size]
        for (i = 0; i < size; i++):
            array.ht[i] = 0

        for (i = 0; i < x4a.count; i++):
            oldnp = &x4a.tbl[i]
            h = confighash(oldnp.data) & (size - 1)
            newnp = &array.tbl[i]
            if array.ht[h]:
                array.ht[h]._from = &newnp.next

            newnp.next = array.ht[h]
            newnp.data = oldnp.data
            newnp._from = &array.ht[h]
            array.ht[h] = newnp

        free(x4a.tbl)
        x4a[00] = array

    h = ph & (x4a.size - 1)
    np = &x4a.tbl[x4a.count++]
    np.data = data
    if x4a.ht[h]:
        x4a.ht[h]._from = &np.next

    np.next = x4a.ht[h]
    x4a.ht[h] = np
    np._from = &x4a.ht[h]
    return 1

def Configtable_find(key):
    if x4a == 0:
        return 0

    h = confighash(key) & (x4a.size - 1)
    np = x4a.ht[h]
    while np:
        if Configcmp(np.data, key) == 0:
            break

        np = np.next

    return np.data if np else 0

def Configtable_clear(f):
    if (x4a == 0) or (x4a.count == 0):
        return

    if f:
        for (i = 0; i < x4a.count; i++):
        (f[00])(x4a.tbl[i].data)


    for (i = 0; i < x4a.size; i++):
        x4a.ht[i] = 0

    x4a.count = 0
    return



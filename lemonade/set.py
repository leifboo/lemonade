
size = 0
def SetSize(n):
    size = n + 1

def SetNew():
    s = calloc(size, 1)
    if s == 0:
        memory_error()

    return s

def SetFree(s):
    free(s)

def SetAdd(s, e):
    _assert((e >= 0) and (e < size))
    rv = s[e]
    s[e] = 1
    return not rv

def SetUnion(s1, s2):
    progress = 0
    for (i = 0; i < size; i++):
        if s2[i] == 0:
            continue

        if s1[i] == 0:
            progress = 1
            s1[i] = 1


    return progress


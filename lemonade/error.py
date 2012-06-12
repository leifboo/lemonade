
def findbreak(msg, min, max):
    for (i = (spot = min); i <= max; i++):
        c = msg[i]
        if c == '\t':
            msg[i] = ' '

        if c == '\n':
            msg[i] = ' '
            spot = i
            break

        if c == 0:
            spot = i
            break

        if (c == '-') and (i < (max - 1)):
            spot = i + 1

        if c == ' ':
            spot = i


    return spot

def ErrorMsg(filename, lineno, format, *args):
    __builtin_va_start(ap, format)
    if lineno > 0:
        sprintf(prefix, "%.*s:%d: ", 30 - 10, filename, lineno)
    else:
        sprintf(prefix, "%.*s: ", 30 - 10, filename)

    prefixsize = strlen(prefix)
    availablewidth = 79 - prefixsize
    vsprintf(errmsg, format, ap)
    __builtin_va_end(ap)
    errmsgsize = strlen(errmsg)
    while (errmsgsize > 0) and (errmsg[errmsgsize - 1] == '\n'):
        errmsg[--errmsgsize] = 0

    base = 0
    while errmsg[base] != 0:
        end = (restart = findbreak(&errmsg[base], 0, availablewidth))
        restart += base
        while errmsg[restart] == ' ':
            restart += 1

        fprintf(stdout, "%s%.*s\n", prefix, end, &errmsg[base])
        base = restart



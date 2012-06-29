'''
Code for processing tables in the LEMON parser generator.
'''

from struct import *



def insert(d, data, key):
    '''Insert a new record into the dictionary.  Return True if
    successful.  Prior data with the same key is NOT overwritten.
    '''
    
    if d is None:
        return False

    if d.get(key):
        # An existing entry with the same key is found.
        # Fail because overwrite is not allowed.
        return False

    # Insert the new data
    d[key] = data
    return True


def find(d, key):
    '''Return the data assigned to the given key.  Return None if no
    such key.'''
    
    if d is None:
        return None
    return d.get(key)


def arrayof(d):
    '''Return a list of all the data in the table.'''
    if d is None:
        return None
    return list(d.values())



def Strsafe(y):
    if y is None:
        return None
    return intern(y)



def Symbol_new(x):
    '''
    Return a the (terminal or nonterminal) symbol "x".  Create a new
    symbol if this is the first time "x" has been seen.
    '''
    
    sp = Symbol_find(x)

    if sp is None:
        sp = symbol(
            name = Strsafe(x),
            type = TERMINAL if x[0].isupper() else NONTERMINAL,
            rule = None,
            fallback = None,
            prec = -1,
            assoc = UNK,
            firstset = None,
            _lambda = False,
            destructor = None,
            datatype = None,
            useCnt = 0,
            index = 0,
            dtnum = 0,
            nsubsym = 0,
            subsym = None,
            )
        Symbol_insert(sp, sp.name)

    sp.useCnt += 1
    return sp


def Symbolcmpp(a, b):
    '''Compare two symbols for working purposes.'''
    
    # Symbols that begin with upper case letters (terminals or tokens)
    # must sort before symbols that begin with lower case letters
    # (non-terminals).  Other than that, the order does not matter.
    #
    # We find experimentally that leaving the symbols in their
    # original order (the order they appeared in the grammar file)
    # gives the smallest parser tables in SQLite.

    # 2012-06-28 lcs: Additionally, '$' must sort first, and
    # '{default}' must sort last.  I can't figure out how/where the
    # original C version guarantees this.

    if a.name == '$':
        i1 = -1
    elif a.name == '{default}':
        i1 = 20000000
    else:
        i1 = a.index + 10000000*(a.name[0] > 'Z')
    if b.name == '$':
        i2 = -1
    elif b.name == '{default}':
        i2 = 20000000
    else:
        i2 = b.index + 10000000*(b.name[0] > 'Z')
    return i1 - i2



x2a = None

def Symbol_init():
    global x2a
    if x2a is None:
        x2a = {}
    return


def Symbol_insert(data, key):
    return insert(x2a, data, key)


def Symbol_find(key):
    return find(x2a, key)


def Symbol_count():
    '''Return the size of the dictionary.'''
    return len(x2a) if x2a else 0


def Symbol_arrayof():
    return arrayof(x2a)



def Configcmp(a, b):
    '''Compare two configurations.'''
    return cmp(a, b)



def State_new():
    new = state(
        bp = None,
        cfp = None,
        statenum = 0,
        ap = None,
        nTknAct = 0, nNtAct = 0,
        iTknOfst= 0, iNtOfst = 0,
        iDflt = 0,
        )
    return new



x3a = None

def State_init():
    global x3a
    if x3a is None:
        x3a = {}
    return


def State_insert(data, key):
    key = statekey(**key._asdict())
    return insert(x3a, data, key)


def State_find(key):
    key = statekey(**key._asdict())
    return find(x3a, key)


def State_arrayof():
    return arrayof(x3a)



x4a = None

def Configtable_init():
    global x4a
    if x4a is None:
        x4a = {}
    return


def Configtable_insert(data):
    return insert(x4a, data, data)


def Configtable_find(key):
    return find(x4a, key)


def Configtable_clear():
    ''' Remove all data from the table.'''
    if not x4a:
        return
    x4a.clear()
    return


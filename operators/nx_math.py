from sympy import *

"""
Eq['xa'] = ...
"""

# уравнения \\ dict 
Eq = {}
#dF = {}

# all vars
X = {}

"""
надо:
формировать Xc при поступлении новых объектов
ключи в фомате x_+ object.uid
"""

# current X
# to do storage
Xc = {'x_a':2,'y_a':2,'x_b':3,'y_b':4,'x_c':5,'y_c':1,'x_d':2,'y_d':5,'x_e':4,'y_e':5,'x_j':3,'y_j':6}
uid = 0

# l - lenght (float64), id1 (point.uid)
def distTwoPoint(l, id1, id2):
    n = len(X)
    k = 0
    # Массив имен переменных для данного ограничения
    m = []
    # Массив новых переменных (s <= m)
    s = []
    for i in [id1, id2]:
        for j in ['x', 'y']:
            m.append(j+i)
            if Symbol(j + i) in X.values():
                continue
            s.append(j+i)
            X[j+i] = (Symbol(j + i))
            k += 1
    global uid
    uid += 1

    X['ld' + str(uid)] = Symbol('ld' + str(uid))
    Xc['ld' + str(uid)] = 0
    m.append('ld' + str(uid))
    s.append('ld' + str(uid))
    print('m = ',m)
    print('s = ',s)
    k += 1
    Equal = X[m[4]]*((X[m[0]] - X[m[2]])**2 + (X[m[1]] - X[m[3]])**2 - l**2)
    localdF0 = {
        m[0] : X[m[0]] - Xc[m[0]],
        m[2] : X[m[2]] - Xc[m[2]],
        m[1] : X[m[1]] - Xc[m[1]],
        m[3] : X[m[3]] - Xc[m[3]],
        m[4] : 0
    }
    print('\n',*localdF0.items(),sep='\n')
    for var in s:
        Eq[var] = localdF0[var]
    
    print('',Eq, sep='\n')
    for var in m:
        Eq[var] += diff(Equal, X[var])

# ...
def eqTwoPoint(id1, id2):
    n = len(X)
    k = 0
    # Массив имен переменных для данного ограничения
    m = []
    # Массив новых переменных (s <= m)
    s = []
    for i in [id1, id2]:
        for j in ['x', 'y']:
            m.append(j+i)
            if Symbol(j + i) in X.values():
                continue
            s.append(j+i)
            X[j+i] = (Symbol(j + i))
            k += 1
    global uid
    uid += 1

    X['ld' + str(uid)] = Symbol('ld' + str(uid))
    Xc['ld' + str(uid)] = 1
    m.append('ld' + str(uid))
    s.append('ld' + str(uid))
    uid += 1

    X['ld' + str(uid)] = Symbol('ld' + str(uid))
    Xc['ld' + str(uid)] = 1
    m.append('ld' + str(uid))
    s.append('ld' + str(uid))
    print('m = ',m)
    print('s = ',s)
    k += 1
    Equal1 = X[m[4]]*(X[m[0]] - X[m[2]])
    Equal2 = X[m[5]]*(X[m[1]] - X[m[3]])
    localdF0 = {
        m[0] : X[m[0]] - Xc[m[0]],
        m[2] : X[m[2]] - Xc[m[2]],
        m[1] : X[m[1]] - Xc[m[1]],
        m[3] : X[m[3]] - Xc[m[3]],
        m[4] : 0,
        m[5] : 0
    }
    print('\n',*localdF0.items(),sep='\n')
    for var in s:
        Eq[var] = localdF0[var]
    
    print('',Eq, sep='\n')
    for var in m:
        Eq[var] += diff(Equal1, X[var])
        Eq[var] += diff(Equal2, X[var])

    res = nsolve(list(Eq.values()), list(X.values()), [Xc[i] for i in X.keys()])
    print("########RESUUUULT#######")
    print(res)
    print(res.values())
    print([*X.values()])
    print(list(zip(res.values(), [*X.values()])))
    print({item: res.values()[pos] for pos, item in enumerate([*X.values()]) if pos < len(res.values())})
    return {str(item): res.values()[pos] for pos, item in enumerate([*X.values()]) if pos < len(res.values())}

# id1 point1.uid...
def perpTwoLines(id1, id2, id3, id4):
    n = len(X)
    k = 0
    # Массив имен переменных для данного ограничения
    m = []
    # Массив новых переменных (s <= m)
    s = []
    for i in [id1, id2, id3, id4]:
        for j in ['x', 'y']:
            m.append(j+i)
            if Symbol(j + i) in X.values():
                continue
            s.append(j+i)
            X[j+i] = (Symbol(j + i))
            k += 1
    global uid

    uid += 1

    X['ld' + str(uid)] = Symbol('ld' + str(uid))
    Xc['ld' + str(uid)] = 0
    m.append('ld' + str(uid))
    s.append('ld' + str(uid))
    print('m = ',m)
    print('s = ',s)
    print("X ", X)

    k += 1
    Equal = X[m[8]]*((X[m[2]] - X[m[0]])*(X[m[6]] - X[m[4]]) + (X[m[3]] - X[m[1]])*(X[m[7]] - X[m[5]]))
    localdF0 = {
        m[0] : X[m[0]] - Xc[m[0]],
        m[2] : X[m[2]] - Xc[m[2]],
        m[1] : X[m[1]] - Xc[m[1]],
        m[3] : X[m[3]] - Xc[m[3]],
        m[4] : X[m[4]] - Xc[m[4]],
        m[5] : X[m[5]] - Xc[m[5]],
        m[6] : X[m[6]] - Xc[m[6]],
        m[7] : X[m[7]] - Xc[m[7]],
        m[8] : 0
    }
    print('\n',*localdF0.items(),sep='\n')
    for var in s:
        Eq[var] = localdF0[var]
    
    print('',Eq, sep='\n')
    for var in m:
        Eq[var] += diff(Equal, X[var])

    res = nsolve(list(Eq.values()), list(X.values()), [Xc[i] for i in X.keys()])
    print(res)
    print({item: res.values()[pos] for pos, item in enumerate([*X.values()])})
    return {str(item): res.values()[pos] for pos, item in enumerate([*X.values()])}

# ....
def parTwoLines(id1, id2, id3, id4):
    n = len(X)
    k = 0
    # Массив имен переменных для данного ограничения
    m = []
    # Массив новых переменных (s <= m)
    s = []
    for i in [id1, id2, id3, id4]:
        for j in ['x', 'y']:
            m.append(j+i)
            if Symbol(j+i) in X.values():
                continue
            s.append(j+i)
            X[j+i] = (Symbol(j + i))
            k += 1
    global uid

    uid += 1

    X['ld' + str(uid)] = Symbol('ld' + str(uid))
    Xc['ld' + str(uid)] = 0
    m.append('ld' + str(uid))
    s.append('ld' + str(uid))
    print('m = ',m)
    print('s = ',s)

    k += 1
    l1 = ((X[m[2]] - X[m[0]])**2 + (X[m[3]] - X[m[1]])**2)**0.5
    l2 = ((X[m[6]] - X[m[4]])**2 + (X[m[7]] - X[m[5]])**2)**0.5
    Equal = X[m[8]]*((X[m[2]]-X[m[0]])*(X[m[7]] - X[m[5]]) -\
     (X[m[6]] - X[m[4]])*(X[m[3]] - X[m[1]]))
     #X[m[8]]*(((X[m[2]] - X[m[0]])*(X[m[6]] - X[m[4]]) + (X[m[3]] - X[m[1]])*(X[m[7]] - X[m[5]])) / l1 / l2 - 1) 
    localdF0 = {
        m[0] : X[m[0]] - Xc[m[0]],
        m[2] : X[m[2]] - Xc[m[2]],
        m[1] : X[m[1]] - Xc[m[1]],
        m[3] : X[m[3]] - Xc[m[3]],
        m[4] : X[m[4]] - Xc[m[4]],
        m[5] : X[m[5]] - Xc[m[5]],
        m[6] : X[m[6]] - Xc[m[6]],
        m[7] : X[m[7]] - Xc[m[7]],
        m[8] : 0
    }
    print('\n',*localdF0.items(),sep='\n')
    for var in s:
        Eq[var] = localdF0[var]
    
    print('',Eq, sep='\n')
    for var in m:
        Eq[var] += diff(Equal, X[var])

    res = nsolve(list(Eq.values()), list(X.values()), [Xc[i] for i in X.keys()])
    print(res)
    print({item: res.values()[pos] for pos, item in enumerate([*X.values()])})
    return {str(item): res.values()[pos] for pos, item in enumerate([*X.values()])}



from scipy.optimize import *
from math import *
Eq = {}
dF = {}

X = []
Xt = {}
Xc = {'xa':1.,'ya':1.,'xb':4.,'yb':3.,'xc':2.,'yc':1.,'xd':2.,'yd':3,'xaa':1,'yaa':2,'xbb':3,'ybb':2,'xcc':2,'ycc':1,'xdd':2.1,'ydd':3}
uid = 0
xid = 0
k = {}

def hor(id1, id2):
    global xid
    global uid
    s = []
    m = []
    for i in [id1, id2]:
        for j in ['x', 'y']:
            m.append(j+i)
            if j+i in Eq.keys():
                continue
            s.append(j+i)
    lcur = 'ld'+str(uid)
    m.append(lcur)
    s.append(lcur)
    Xc[lcur] = 0
    uid+=1
    c = len(Eq.keys())
    print(s)
    for var in s:
        k[var] = c
        c+=1
    localdF0 = {
        'x'+id1 : lambda v: v[k['x'+id1]] - Xc['x'+id1],
        'y'+id1 : lambda v: v[k['y'+id1]] - Xc['y'+id1],
        'x'+id2 : lambda v: v[k['x'+id2]] - Xc['x'+id2],
        'y'+id2 : lambda v: v[k['y'+id2]] - Xc['y'+id2],
        lcur    : lambda v: 0
    }
    dF = {
        'x'+id1 : lambda v: 0,
        'y'+id1 : lambda v: -v[k[lcur]],
        'x'+id2 : lambda v: 0,
        'y'+id2 : lambda v: v[k[lcur]],
        lcur    : lambda v: v[k['y'+id2]] - v[k['y'+id1]]
    }
    for var in s:
        Eq[var] = localdF0[var]
    Eq2 = Eq.copy()
    for var in m:
        Eq[var] = lambda v: Eq2[var](v) + dF[var](v)
    def f(vars):
        return [i(vars) for i in Eq.values()]
    print(Eq.keys())
    print(Xc)
    print([Xc[i] for i in Eq.keys()])
    oldX1 = Xc['x'+id1]
    oldX2 = Xc['x'+id2]
    oldY1 = Xc['y'+id1]
    oldY2 = Xc['y'+id2]
    X = oldX2 - oldX1
    Y = oldY2 - oldY1
    alfa  = pi / 2. + acos((oldY2 - oldY1) / ((oldY2 - oldY1)**2 + (oldX2 - oldX1)**2)**0.5)

    newX = X*cos(alfa)-Y*sin(alfa)
    newY = X*sin(alfa)+Y*cos(alfa)
    print(X)
    Xc['y'+id1] = Xc['y'+id2] = (oldY2 + oldY1) / 2.
    Xc['x'+id1] = (oldX2 + oldX1 + newX ) / 2.
    Xc['x'+id2] = (oldX2 + oldX1 - newX ) / 2.
    print(Xc)
    sol = root(f,[Xc[i] for i in Eq.keys()])
    if sol.success:
        keys = [k for k in k.keys()]
        print(keys)
        i = 0
        for x in sol.x:
            Xc[keys[i]] = x
            i+=1
    print(Xc)
    #return sol.x
    return {key: Xc[key] for pos, key in enumerate(keys)}

def ver(id1, id2):
    global xid
    global uid
    s = []
    m = []
    for i in [id1, id2]:
        for j in ['x', 'y']:
            m.append(j+i)
            if j+i in Eq.keys():
                continue
            s.append(j+i)
    lcur = 'ld'+str(uid)
    m.append(lcur)
    s.append(lcur)
    Xc[lcur] = 0.0
    uid+=1
    c = len(Eq.keys())
    print(s)
    for var in s:
        k[var] = c
        c+=1
    print(k)
    localdF0 = {
        'x'+id1 : lambda v: v[k['x'+id1]] - Xc['x'+id1],
        'y'+id1 : lambda v: v[k['y'+id1]] - Xc['y'+id1],
        'x'+id2 : lambda v: v[k['x'+id2]] - Xc['x'+id2],
        'y'+id2 : lambda v: v[k['y'+id2]] - Xc['y'+id2],
        lcur    : lambda v: 0
    }
    dF = {
        'x'+id1 : lambda v: -v[k[lcur]],
        'y'+id1 : lambda v: 0,
        'x'+id2 : lambda v: v[k[lcur]],
        'y'+id2 : lambda v: 0,
        lcur    : lambda v: v[k['x'+id2]] - v[k['x'+id1]]
    }
    for var in s:
        Eq[var] = localdF0[var]
    Eq2 = Eq.copy()
    for var in m:
        Eq[var] = lambda v: Eq2[var](v) + dF[var](v)
    def f(vars):
        return [i(vars) for i in Eq.values()]
    oldX1 = Xc['x'+id1]
    oldX2 = Xc['x'+id2]
    oldY1 = Xc['y'+id1]
    oldY2 = Xc['y'+id2]
    X = oldX2 - oldX1
    Y = oldY2 - oldY1
    alfa  = acos((oldY2 - oldY1) / ((oldY2 - oldY1)**2 + (oldX2 - oldX1)**2)**0.5)

    newX = X*cos(alfa)-Y*sin(alfa)
    newY = X*sin(alfa)+Y*cos(alfa)
    print(X)
    Xc['x'+id1] = Xc['x'+id2] = (oldX2 + oldX1) / 2.
    Xc['y'+id1] = (oldY2 + oldY1 + newY ) / 2.
    Xc['y'+id2] = (oldY2 + oldY1 - newY ) / 2.
    print(Xc)

    sol = root(f,[Xc[i] for i in Eq.keys()])
    if sol.success:
        keys = [k for k in k.keys()]
        print(keys)
        i = 0
        for x in sol.x:
            Xc[keys[i]] = x
            i+=1
    print("XXXXXXXXXXCCCCCCCCCCCCCCCCC")
    print(Xc)

    #return sol.x
    return {key: Xc[key] for pos, key in enumerate(keys)}


def fixPoint(id1):
    global xid
    global uid
    s = []
    m = []
    for i in [id1]:
        for j in ['x', 'y']:
            m.append(j+i)
            if j+i in Eq.keys():
                continue
            s.append(j+i)
    lcur1 = 'ld'+str(uid)
    m.append(lcur1)
    s.append(lcur1)
    Xc[lcur1] = 0.0
    uid+=1
    lcur2 = 'ld'+str(uid)
    m.append(lcur2)
    s.append(lcur2)
    Xc[lcur2] = 0.0
    uid+=1
    print(s)
    c = len(Eq.keys())
    for var in s:
        k[var] = c
        c+=1
    print(k)
    xf = Xc['x'+id1]
    yf = Xc['y'+id1]
    localdF0 = {
        'x'+id1 : lambda v: v[k['x'+id1]] - xf + v[k[lcur1]],
        'y'+id1 : lambda v: v[k['y'+id1]] - yf + v[k[lcur2]],
        lcur1   : lambda v: v[k['x'+id1]] - xf,
        lcur2   : lambda v: v[k['y'+id1]] - yf
    }
    for var in s:
        Eq[var] = localdF0[var]
    def f(vars):
        return [i(vars) for i in Eq.values()]
    sol = root(f,[Xc[i] for i in Eq.keys()])
    if sol.success:
        keys = [k for k in k.keys()]
        print(keys)
        i = 0
        for x in sol.x:
            Xc[keys[i]] = x
            i+=1
    print(Xc)
    return sol.x


def eqTwoPoint(id1,id2):
    global uid
    global Eq
    s = []
    m = []
    for i in [id1, id2]:
        for j in ['x', 'y']:
            m.append(j+i)
            if j+i in Eq.keys():
                continue
            s.append(j+i)
    lcur1 = 'ld'+str(uid)
    m.append(lcur1)
    s.append(lcur1)
    Xc[lcur1] = 0.0
    uid+=1
    lcur2 = 'ld'+str(uid)
    m.append(lcur2)
    s.append(lcur2)
    Xc[lcur2] = 0.0
    uid+=1
    c = len(Eq.keys())
    for var in s:
        k[var] = c
        c+=1
    print(k)
    localdF0 = {
        'x'+id1 : lambda v: v[k['x'+id1]] - Xc['x'+id1],
        'y'+id1 : lambda v: v[k['y'+id1]] - Xc['y'+id1],
        'x'+id2 : lambda v: v[k['x'+id2]] - Xc['x'+id2],
        'y'+id2 : lambda v: v[k['y'+id2]] - Xc['y'+id2],
        lcur2   : lambda v: 0.,
        lcur1   : lambda v: 0.,
    }
    dF = {
        'x'+id1 : lambda v: v[k[lcur1]],
        'y'+id1 : lambda v: v[k[lcur2]],
        'x'+id2 : lambda v: v[k[lcur1]],
        'y'+id2 : lambda v: v[k[lcur2]],
        lcur1   : lambda v: v[k['x'+id2]] - v[k['x'+id1]],
        lcur2   : lambda v: v[k['y'+id2]] - v[k['y'+id1]]
    }
    print(m)
    print(s)
    for var in s:
        Eq[var] = localdF0[var]
    Eq2 = Eq.copy()
    for var in m:
        Eq[var] = lambda v: Eq2[var](v) + dF[var](v)
    def f(vars):
        return [i(vars) for i in Eq.values()]
    
    print([Xc[i] for i in Eq.keys()])
    Xc['x'+id2] = Xc['x'+id1]
    Xc['y'+id2] = Xc['y'+id1]

    sol = root(f,[Xc[i] for i in Eq.keys()])
    if sol.success:
        keys = [k for k in k.keys()]
        print(keys)
        i = 0
        for x in sol.x:
            Xc[keys[i]] = x
            i+=1
    print(Xc)
    return sol.x


def distTwoPoint(l, id1, id2):
    global uid
    # Массив имен переменных для данного ограничения
    m = []
    # Массив новых переменных (s <= m)
    s = []
    for i in [id1, id2]:
        for j in ['x', 'y']:
            m.append(j+i)
            if j+i in Eq.keys():
                continue
            s.append(j+i)
    lcur1 = 'ld'+str(uid)
    m.append(lcur1)
    s.append(lcur1)
    Xc[lcur1] = 0.0
    uid+=1
    c = len(Eq.keys())
    for var in s:
        k[var] = c
        c+=1
    # Equal = X[m[4]]*((X[m[0]] - X[m[2]])**2 + (X[m[1]] - X[m[3]])**2 - l**2)
    localdF0 = {
        'x'+id1 : lambda v: v[k['x'+id1]] - Xc['x'+id1],
        'y'+id1 : lambda v: v[k['y'+id1]] - Xc['y'+id1],
        'x'+id2 : lambda v: v[k['x'+id2]] - Xc['x'+id2],
        'y'+id2 : lambda v: v[k['y'+id2]] - Xc['y'+id2],
        lcur1   : lambda v: 0.
    }
    dF = {
        'x'+id1 : lambda v: -v[k[lcur1]]*(v[k['x'+id2]] - v[k['x'+id1]])*2.,
        'y'+id1 : lambda v: -v[k[lcur1]]*(v[k['y'+id2]] - v[k['y'+id1]])*2,
        'x'+id2 : lambda v: v[k[lcur1]]*(v[k['x'+id2]] - v[k['x'+id1]])*2.,
        'y'+id2 : lambda v: v[k[lcur1]]*(v[k['y'+id2]] - v[k['y'+id1]])*2.,
        lcur1   : lambda v: (v[k['x'+id2]] - v[k['x'+id1]])**2+(v[k['y'+id2]] - v[k['y'+id1]])**2 - l**2
    }
    print(m,s)
    for var in s:
        Eq[var] = localdF0[var]
    Eq2 = Eq.copy()
    for var in m:
        Eq[var] = lambda v: Eq2[var](v) + dF[var](v)
    def f(vars):
        return [i(vars) for i in Eq.values()]
    print([Xc[i] for i in Eq.keys()])
    print([Xc[i] for i in Eq.keys()])
    oldX1 = Xc['x'+id1]
    oldX2 = Xc['x'+id2]
    oldY1 = Xc['y'+id1]
    oldY2 = Xc['y'+id2]
    XA = oldX2 - oldX1
    YA = oldY2 - oldY1
    print(XA,YA)
    l1 = (XA**2. + YA**2.)**0.5
    Xc['x'+id2] = l * XA / l1 + Xc['x'+id1]
    Xc['y'+id2] = l * YA / l1 + Xc['y'+id1]
    print([Xc[i] for i in Eq.keys()])
    sol = root(f,[Xc[i] for i in Eq.keys()])

    if sol.success:
        keys = [k for k in k.keys()]
        print(keys)
        i = 0
        for x in sol.x:
            Xc[keys[i]] = x
            i+=1
    print(Xc)
    return sol.x


def angleTwoLines(angle, id1, id2, id3, id4):
    global xid
    global uid
    s = []
    m = []
    for i in [id1, id2, id3, id4]:
        for j in ['x', 'y']:
            m.append(j+i)
            if j+i in Xt.keys():
                continue
            s.append(j+i)
    lcur = 'ld'+str(uid)
    m.append(lcur)
    s.append(lcur)
    Xc[lcur] = 0.0
    uid+=1
    c = len(Eq.keys())
    for var in s:
        k[var] = c
        c+=1
    print(k)
    localdF0 = {
        'x'+id1 : lambda v: v[k['x'+id1]] - Xc['x'+id1],
        'y'+id1 : lambda v: v[k['y'+id1]] - Xc['y'+id1],
        'x'+id2 : lambda v: v[k['x'+id2]] - Xc['x'+id2],
        'y'+id2 : lambda v: v[k['y'+id2]] - Xc['y'+id2],
        'x'+id3 : lambda v: v[k['x'+id3]] - Xc['x'+id3],
        'y'+id3 : lambda v: v[k['y'+id3]] - Xc['y'+id3],
        'x'+id4 : lambda v: v[k['x'+id4]] - Xc['x'+id4],
        'y'+id4 : lambda v: v[k['y'+id4]] - Xc['y'+id4],
        lcur    : lambda v: 0
    }
    dF = {
        'x'+id1 : lambda v: v[k[lcur]]*((-1.0*v[k['x'+id1]] + 1.0*v[k['x'+id2]])*((-v[k['x'+id1]] + v[k['x'+id2]])*(-v[k['x'+id3]] + v[k['x'+id4]]) + (-v[k['y'+id1]] + v[k['y'+id2]])*(-v[k['y'+id3]] + v[k['y'+id4]]))*((-v[k['x'+id1]] + v[k['x'+id2]])**2 + (-v[k['y'+id1]] + v[k['y'+id2]])**2)**(-1.5)*((-v[k['x'+id3]] + v[k['x'+id4]])**2 + (-v[k['y'+id3]] + v[k['y'+id4]])**2)**(-0.5) + (v[k['x'+id3]] - v[k['x'+id4]])*((-v[k['x'+id1]] + v[k['x'+id2]])**2 + (-v[k['y'+id1]] + v[k['y'+id2]])**2)**(-0.5)*((-v[k['x'+id3]] + v[k['x'+id4]])**2 + (-v[k['y'+id3]] + v[k['y'+id4]])**2)**(-0.5)),
        'y'+id1 : lambda v: v[k[lcur]]*((-1.0*v[k['y'+id1]] + 1.0*v[k['y'+id2]])*((-v[k['x'+id1]] + v[k['x'+id2]])*(-v[k['x'+id3]] + v[k['x'+id4]]) + (-v[k['y'+id1]] + v[k['y'+id2]])*(-v[k['y'+id3]] + v[k['y'+id4]]))*((-v[k['x'+id1]] + v[k['x'+id2]])**2 + (-v[k['y'+id1]] + v[k['y'+id2]])**2)**(-1.5)*((-v[k['x'+id3]] + v[k['x'+id4]])**2 + (-v[k['y'+id3]] + v[k['y'+id4]])**2)**(-0.5) + (v[k['y'+id3]] - v[k['y'+id4]])*((-v[k['x'+id1]] + v[k['x'+id2]])**2 + (-v[k['y'+id1]] + v[k['y'+id2]])**2)**(-0.5)*((-v[k['x'+id3]] + v[k['x'+id4]])**2 + (-v[k['y'+id3]] + v[k['y'+id4]])**2)**(-0.5)),
        'x'+id2 : lambda v: v[k[lcur]]*((1.0*v[k['x'+id1]] - 1.0*v[k['x'+id2]])*((-v[k['x'+id1]] + v[k['x'+id2]])*(-v[k['x'+id3]] + v[k['x'+id4]]) + (-v[k['y'+id1]] + v[k['y'+id2]])*(-v[k['y'+id3]] + v[k['y'+id4]]))*((-v[k['x'+id1]] + v[k['x'+id2]])**2 + (-v[k['y'+id1]] + v[k['y'+id2]])**2)**(-1.5)*((-v[k['x'+id3]] + v[k['x'+id4]])**2 + (-v[k['y'+id3]] + v[k['y'+id4]])**2)**(-0.5) + (-v[k['x'+id3]] + v[k['x'+id4]])*((-v[k['x'+id1]] + v[k['x'+id2]])**2 + (-v[k['y'+id1]] + v[k['y'+id2]])**2)**(-0.5)*((-v[k['x'+id3]] + v[k['x'+id4]])**2 + (-v[k['y'+id3]] + v[k['y'+id4]])**2)**(-0.5)),
        'y'+id2 : lambda v: v[k[lcur]]*((1.0*v[k['y'+id1]] - 1.0*v[k['y'+id2]])*((-v[k['x'+id1]] + v[k['x'+id2]])*(-v[k['x'+id3]] + v[k['x'+id4]]) + (-v[k['y'+id1]] + v[k['y'+id2]])*(-v[k['y'+id3]] + v[k['y'+id4]]))*((-v[k['x'+id1]] + v[k['x'+id2]])**2 + (-v[k['y'+id1]] + v[k['y'+id2]])**2)**(-1.5)*((-v[k['x'+id3]] + v[k['x'+id4]])**2 + (-v[k['y'+id3]] + v[k['y'+id4]])**2)**(-0.5) + (-v[k['y'+id3]] + v[k['y'+id4]])*((-v[k['x'+id1]] + v[k['x'+id2]])**2 + (-v[k['y'+id1]] + v[k['y'+id2]])**2)**(-0.5)*((-v[k['x'+id3]] + v[k['x'+id4]])**2 + (-v[k['y'+id3]] + v[k['y'+id4]])**2)**(-0.5)),
        'x'+id3 : lambda v: v[k[lcur]]*((v[k['x'+id1]] - v[k['x'+id2]])*((-v[k['x'+id1]] + v[k['x'+id2]])**2 + (-v[k['y'+id1]] + v[k['y'+id2]])**2)**(-0.5)*((-v[k['x'+id3]] + v[k['x'+id4]])**2 + (-v[k['y'+id3]] + v[k['y'+id4]])**2)**(-0.5) + (-1.0*v[k['x'+id3]] + 1.0*v[k['x'+id4]])*((-v[k['x'+id1]] + v[k['x'+id2]])*(-v[k['x'+id3]] + v[k['x'+id4]]) + (-v[k['y'+id1]] + v[k['y'+id2]])*(-v[k['y'+id3]] + v[k['y'+id4]]))*((-v[k['x'+id1]] + v[k['x'+id2]])**2 + (-v[k['y'+id1]] + v[k['y'+id2]])**2)**(-0.5)*((-v[k['x'+id3]] + v[k['x'+id4]])**2 + (-v[k['y'+id3]] + v[k['y'+id4]])**2)**(-1.5)),
        'y'+id3 : lambda v: v[k[lcur]]*((v[k['y'+id1]] - v[k['y'+id2]])*((-v[k['x'+id1]] + v[k['x'+id2]])**2 + (-v[k['y'+id1]] + v[k['y'+id2]])**2)**(-0.5)*((-v[k['x'+id3]] + v[k['x'+id4]])**2 + (-v[k['y'+id3]] + v[k['y'+id4]])**2)**(-0.5) + (-1.0*v[k['y'+id3]] + 1.0*v[k['y'+id4]])*((-v[k['x'+id1]] + v[k['x'+id2]])*(-v[k['x'+id3]] + v[k['x'+id4]]) + (-v[k['y'+id1]] + v[k['y'+id2]])*(-v[k['y'+id3]] + v[k['y'+id4]]))*((-v[k['x'+id1]] + v[k['x'+id2]])**2 + (-v[k['y'+id1]] + v[k['y'+id2]])**2)**(-0.5)*((-v[k['x'+id3]] + v[k['x'+id4]])**2 + (-v[k['y'+id3]] + v[k['y'+id4]])**2)**(-1.5)),
        'x'+id4 : lambda v: v[k[lcur]]*((-v[k['x'+id1]] + v[k['x'+id2]])*((-v[k['x'+id1]] + v[k['x'+id2]])**2 + (-v[k['y'+id1]] + v[k['y'+id2]])**2)**(-0.5)*((-v[k['x'+id3]] + v[k['x'+id4]])**2 + (-v[k['y'+id3]] + v[k['y'+id4]])**2)**(-0.5) + (1.0*v[k['x'+id3]] - 1.0*v[k['x'+id4]])*((-v[k['x'+id1]] + v[k['x'+id2]])*(-v[k['x'+id3]] + v[k['x'+id4]]) + (-v[k['y'+id1]] + v[k['y'+id2]])*(-v[k['y'+id3]] + v[k['y'+id4]]))*((-v[k['x'+id1]] + v[k['x'+id2]])**2 + (-v[k['y'+id1]] + v[k['y'+id2]])**2)**(-0.5)*((-v[k['x'+id3]] + v[k['x'+id4]])**2 + (-v[k['y'+id3]] + v[k['y'+id4]])**2)**(-1.5)),
        'y'+id4 : lambda v: v[k[lcur]]*((-v[k['y'+id1]] + v[k['y'+id2]])*((-v[k['x'+id1]] + v[k['x'+id2]])**2 + (-v[k['y'+id1]] + v[k['y'+id2]])**2)**(-0.5)*((-v[k['x'+id3]] + v[k['x'+id4]])**2 + (-v[k['y'+id3]] + v[k['y'+id4]])**2)**(-0.5) + (1.0*v[k['y'+id3]] - 1.0*v[k['y'+id4]])*((-v[k['x'+id1]] + v[k['x'+id2]])*(-v[k['x'+id3]] + v[k['x'+id4]]) + (-v[k['y'+id1]] + v[k['y'+id2]])*(-v[k['y'+id3]] + v[k['y'+id4]]))*((-v[k['x'+id1]] + v[k['x'+id2]])**2 + (-v[k['y'+id1]] + v[k['y'+id2]])**2)**(-0.5)*((-v[k['x'+id3]] + v[k['x'+id4]])**2 + (-v[k['y'+id3]] + v[k['y'+id4]])**2)**(-1.5)),
        lcur    : lambda v: ((-v[k['x'+id1]] + v[k['x'+id2]])*(-v[k['x'+id3]] + v[k['x'+id4]]) + (-v[k['y'+id1]] + v[k['y'+id2]])*(-v[k['y'+id3]] + v[k['y'+id4]]))*((-v[k['x'+id1]] + v[k['x'+id2]])**2 + (-v[k['y'+id1]] + v[k['y'+id2]])**2)**(-0.5)*((-v[k['x'+id3]] + v[k['x'+id4]])**2 + (-v[k['y'+id3]] + v[k['y'+id4]])**2)**(-0.5) - cos(angle / 180 * pi)
    }
    print(s)
    print(m)
    for var in s:
        Eq[var] = localdF0[var]
    Eq2 = Eq.copy()
    for var in m:
        Eq[var] = lambda v: Eq2[var](v) + dF[var](v)
    print(Eq.keys())

    def f(vars):
        return [i(vars) for i in Eq.values()]
    print([Xc[i] for i in Eq.keys()])
    oldX1 = Xc['x'+id1]
    oldX2 = Xc['x'+id2]
    oldY1 = Xc['y'+id1]
    oldY2 = Xc['y'+id2]
    XA = oldX2 - oldX1
    YA = oldY2 - oldY1
    oldX3 = Xc['x'+id3]
    oldX4 = Xc['x'+id4]
    oldY3 = Xc['y'+id3]
    oldY4 = Xc['y'+id4]
    XB = oldX4 - oldX3
    YB = oldY4 - oldY3
    print(XA,YA)
    print(XB,YB)
    l1 = (XA**2. + YA**2.)**0.5
    l2 = (XB**2. + YB**2.)**0.5
    print(l2)
    alfa0  = acos((XA*XB + YA*YB) / (l1*l2))
    alfa = (angle - alfa0 / pi * 180.) / 180. * pi + pi
    print(180. * alfa / pi)
    newX = XB*cos(alfa)-YB*sin(alfa)
    newY = XB*sin(alfa)+YB*cos(alfa)
    print(newX, newY)
    # print(180. / pi *acos((XA*newX + YA*newY) / (l1*l2)))
    XC = (oldX3 + oldX4) / 2.
    YC = (oldY3 + oldY4) / 2.

    Xc['x'+id3] = XC + newX / 2.
    Xc['x'+id4] = XC - newX / 2.
    Xc['y'+id3] = YC + newY / 2.
    Xc['y'+id4] = YC - newY / 2.
    print(Xc)
    sol = root(f,[Xc[i] for i in Eq.keys()])
    if sol.success:
        keys = [k for k in k.keys()]
        print(keys)
        i = 0
        for x in sol.x:
            Xc[keys[i]] = x
            i+=1
    print(Xc)
    return sol.x

# print(fixPoint('b'))
# print(fixPoint('b'))
# print(eqTwoPoint('a','b'))
# print(ver('a','b'))
# print(hor('a','b'))
# print("After fix:")
# print(Xc)
# print()
# angleTwoLines(90,'a','b','c','d')
#print(distTwoPoint(2,'a','b'))
# print(hor('a','b'))
def f(vars):
        return [i(vars) for i in Eq.values()]
#delta = 0.05
#Xc['xa']+=delta
#print(Xc)
#while True:
#    sol = root(f,[Xc[i] for i in Eq.keys()])
#    print(sol.x)
#    if sol.success:
#        keys = [k for k in k.keys()]
#        print(keys)
#        i = 0
#        for x in sol.x:
#            Xc[keys[i]] = x
#            i+=1
#    print(Xc)
#    Xc['xa']+=delta
#    input()


# print(eqTwoPoint('a','b'))
# print([i for i in Eq.keys()])
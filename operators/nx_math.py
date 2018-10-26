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

# ...
def angleTwoLines(angle, id1, id2, id3, id4):
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

    k += 1
    l1 = ((X[m[2]] - X[m[0]])**2 + (X[m[3]] - X[m[1]])**2)**0.5
    l2 = ((X[m[6]] - X[m[4]])**2 + (X[m[7]] - X[m[5]])**2)**0.5
    # l1 = expand(l1)
    # l2 = expand(l2)
    print(l1)
    print(l2)
    Equal = X[m[8]]*(((X[m[2]] - X[m[0]])*(X[m[6]] - X[m[4]]) + \
        (X[m[3]] - X[m[1]])*(X[m[7]] - X[m[5]])) / (l1 * l2) - cos(angle / 180 * pi))
    # Equal = simplify(Equal)
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

# ...
def hor(id1, id2):
    n = len(X)
    k = 0
    # Массив имен переменных для данного ограничения
    m = []
    # Массив новых переменных (s <= m)
    s = []
    for i in [id1, id2]:
        for j in ['x', 'y']:
            m.append(j+"_"+i)
            if Symbol(j + "_" + i) in X.values():
                continue
            s.append(j+"_"+i)
            X[j+"_"+i] = (Symbol(j +"_"+ i))
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
    Equal = X[m[4]]*(X[m[1]] - X[m[3]])
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

    res = nsolve(list(Eq.values()), list(X.values()), [Xc[i] for i in X.keys()])
    print(res)
    print({item: res.values()[pos] for pos, item in enumerate([*X.values()])})
    return {str(item): res.values()[pos] for pos, item in enumerate([*X.values()])}

# ...
def ver(id1, id2):

    n = len(X)
    k = 0
    # Массив имен переменных для данного ограничения
    m = []
    # Массив новых переменных (s <= m)
    s = []
    for i in [id1, id2]:
        for j in ['x', 'y']:
            m.append(j+"_"+i)
            if Symbol(j + "_" +i) in X.values():
                continue
            s.append(j+"_"+i)
            X[j+"_"+i] = (Symbol(j + "_" +i))
            k += 1
    global uid

    uid += 1

    X['ld' + str(uid)] = Symbol('ld' + str(uid))
    Xc['ld' + str(uid)] = 0
    m.append('ld' + str(uid))
    s.append('ld' + str(uid))
    print('m = ',m)
    print('s = ',s)
    print('X = ', X)

    k += 1
    Equal = X[m[4]]*(X[m[0]] - X[m[2]])
    localdF0 = {
        m[0] : X[m[0]] - Xc[m[0]],
        m[2] : X[m[2]] - Xc[m[2]],
        m[1] : X[m[1]] - Xc[m[1]],
        m[3] : X[m[3]] - Xc[m[3]],
        m[4] : 0
    }

    print("LOCALF0")
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

#ver('a','b')
#hor('a','c')

#distTwoPoint(2,'a','b')
#angleTwoLines(45,'a','b','c','b')

"""
print('',*Eq.items(),sep="\n")
print(Xc)
print("EQ.values")
print(Eq.values())
print("X.values")
print(X.values())
print("Xc")
print(Xc)
res = nsolve(list(Eq.values()), list(X.values()), [Xc[i] for i in X.keys()])
print(res)
print({item: res.values()[pos] for pos, item in enumerate([*X.values()])})
"""

import time
import operator


def get_a(U, pi, tasks, b):
    q = tasks[b][2]
    idx_b = pi.index(b)
    for val in pi:
        p = 0
        r = tasks[val][0]
        mi = pi.index(val)
        for a in range(mi, idx_b+1):
            p += tasks[pi[a]][1]
        if U == r+p+q:
            return val


def get_b(U, pi, tasks):
    p = 0
    for val in pi:
        r = tasks[val][0]
        p = max(p, r) + tasks[val][1]
        if U == p + tasks[val][2]:
            j = val
    return j


def get_c(pi, tasks, a, b):
    flag = 0
    a = pi.index(a)
    b = pi.index(b)
    for val in range(a, b+1):
        if tasks[pi[val]][2] < tasks[pi[b]][2]:
            j = pi[val]
            flag = 1
    if flag == 1:
        return j
    else:
        return []


################################################# CLASSICAL APPROACH #################################################
def Carlier(tasks):
    global UB
    global n
    pi, U = Schrage(tasks)
    if U < UB:
        UB = U
    b = get_b(U, pi, tasks)
    a = get_a(U, pi, tasks, b)
    c = get_c(pi, tasks, a, b)
    if c == []:
        return UB, tasks
    K = []

    for i in pi[pi.index(c)+1:pi.index(b)+1]:
        K.append(i)

    rK = []
    qK = []
    pK = 0
    for val in K:
        rK.append(tasks[val][0])
        qK.append(tasks[val][2])
        pK += tasks[val][1]
    qK = min(qK)
    rK = min(rK)
    rpq = [rK, pK, qK]
    LB = Schrage_pmtn(tasks)
    remember_R = tasks[c][0]
    tasks[c][0] = max(tasks[c][0], rK+pK)
    hkc = min(rK, tasks[c][0])+pK+tasks[c][1]+min(qK, tasks[c][2])
    LBL = max(sum(rpq), LB, hkc)
    if LBL < UB:
        Carlier(tasks)
    tasks[c][0] = remember_R
    remember_Q = tasks[c][2]
    tasks[c][2] = max(tasks[c][2], qK + pK)
    hkc = min(rK, tasks[c][0]) + pK + tasks[c][1] + min(qK, tasks[c][2])
    LBP = max(sum(rpq), hkc, LB)
    if LBP < UB:
        Carlier(tasks)
    tasks[c][2] = remember_Q
    return UB


################################################### CARLIER WITH ELIMINATION ##########################################
def Carlier_Elim(tasks):
    global UB
    global n
    pi, U = Schrage(tasks)
    if U < UB:
        UB = U
    b = get_b(U, pi, tasks)
    a = get_a(U, pi, tasks, b)
    c = get_c(pi, tasks, a, b)
    if c == []:
        return UB, tasks
    K = []

    for i in pi[pi.index(c)+1:pi.index(b)+1]:
        K.append(i)

    rK = []
    qK = []
    pK = 0
    for i in K:
        rK.append(tasks[i][0])
        qK.append(tasks[i][2])
        pK += tasks[i][1]
    qK = min(qK)
    rK = min(rK)
    rpq = [rK, pK, qK]
    LB = Schrage_pmtn(tasks)

    L = []
    for i in pi[0:pi.index(c)]:
        L.append(i)
    for i in pi[pi.index(b)+1:]:
        L.append(i)
    for i in L:
        if UB - sum(rpq) >= tasks[i][1]:
            L.pop(L.index(i))

    for i in L:
        if UB <= tasks[i][0] + tasks[i][1] + rpq[1] + tasks[b][2]:
            tasks[i][0] = max(tasks[i][0], rpq[0]+rpq[1])
        if UB <= rpq[0] + tasks[i][1] + rpq[1] + tasks[i][2]:
            tasks[i][2] = max(tasks[i][2], rpq[2]+rpq[1])

    remember_R = tasks[c][0]
    tasks[c][0] = max(tasks[c][0], rK+pK)
    hkc = min(rK, tasks[c][0])+pK+tasks[c][1]+min(qK, tasks[c][2])
    LBL = max(sum(rpq), LB, hkc)
    if LBL < UB:
        Carlier_Elim(tasks)
    tasks[c][0] = remember_R
    remember_Q = tasks[c][2]
    tasks[c][2] = max(tasks[c][2], qK + pK)
    hkc = min(rK, tasks[c][0]) + pK + tasks[c][1] + min(qK, tasks[c][2])
    LBP = max(sum(rpq), hkc, LB)
    if LBP < UB:
        Carlier_Elim(tasks)
    tasks[c][2] = remember_Q
    return UB

############################################## SCHRAGE ALGORITHMS #####################################################
def Schrage(N):
    teta = []
    NG = []
    NN = []
    a = 0
    for i in N:
        NN.append([a, i[0], i[1], i[2]])
        a += 1
    t = min(NN, key=operator.itemgetter(1))[1]
    Cmax = 0
    while (NN != [] or NG != []):
        while (NN != [] and t >= min(NN, key=operator.itemgetter(1))[1]):
            j = NN.index(min(NN, key=operator.itemgetter(1)))
            NG.append(NN[j])
            NN.pop(j)

        if NG == []:
            t = min(NN, key=operator.itemgetter(1))[1]
        else:
            i = NG.index(max(NG, key=operator.itemgetter(3)))
            j = NG[i]
            NG.pop(i)
            teta.append(j[0])
            t = t + j[2]
            Cmax = max(Cmax, t+j[3])
    return teta, Cmax


def Schrage_pmtn(N):
    NG = []
    NN = []
    a = 0
    for i in N:
        NN.append([a, i[0], i[1], i[2]])
        a += 1
    t = min(NN, key=operator.itemgetter(1))[1]
    Cmax = 0
    l = [0, 0, 0, 100000000]
    while (NN != [] or NG != []):
        while (NN != [] and t >= min(NN, key=operator.itemgetter(1))[1]):
            j = NN.index(min(NN, key=operator.itemgetter(1)))
            i = NN[j]
            NG.append(NN[j])
            NN.pop(j)
            if i[3] > l[3]:
                l[2] = t - i[1]
                t = i[1]
                if l[2] > 0:
                    NG.append(l)
        if NG == []:
            t = min(NN, key=operator.itemgetter(1))[1]
        else:
            i = NG.index(max(NG, key=operator.itemgetter(3)))
            j = NG[i]
            NG.pop(i)
            l = j
            t = t + j[2]
            Cmax = max(Cmax, t+j[3])
    return Cmax



def read_data_2list(filename):
    file = open(filename, "r")
    tasks_val, columns_val = file.readline().split()
    tasks_val = int(tasks_val)
    columns_val = int(columns_val)
    tasks = []
    values = []
    for val in file.read().split():
        values.append(float(val))

    for a in range(0, len(values), 3):
        tmp_tab = []
        for b in range(0,3):
            tmp_tab = tmp_tab + [values[a+b]]
        tasks.append(tmp_tab)

    file.close()
    return tasks_val, columns_val, tasks


if __name__=="__main__":

    print("Main algorithm")
    data = [0, 1, 3, 4]
    correct = [228, 3026, 3309, 3191]
    tmp = 0
    for i in data:
        UB = 9999999
        plik = "../data/carlier_data" + str(i) + ".txt"
        tasks_val, columns_val, tasks = read_data_2list(plik)
        start = time.perf_counter()
        UB = Carlier(tasks)
        stop = time.perf_counter()
        czas = round((stop - start), 5)
        print("{} {}  Correct: {}  Time: {}".format(plik, UB, correct[tmp], czas))
        tmp += 1

    print("-"*23)
    print("\nWith elimination")
    data = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    correct = [228, 3026, 3665, 3309, 3191, 3618, 3446, 3821, 3634]

    for i in data:
        UB = 9999999
        plik = "../data/carlier_data" + str(i) + ".txt"
        tasks_val, columns_val, tasks = read_data_2list(plik)
        start = time.perf_counter()
        UB = Carlier_Elim(tasks)
        stop = time.perf_counter()
        czas = round((stop - start), 5)
        print("{} {}  Correct: {}  Time: {}".format(plik, UB, correct[i], czas))




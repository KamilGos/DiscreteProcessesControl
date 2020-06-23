import numpy as np
from prettytable import PrettyTable


def johnson_algorithm(machines_val, tasks):
    print("\n Johnson algorithm: START")
    if(machines_val == 2):
        print("Two machines algorithm: START")
        return johnson2m(tasks)
    if (machines_val == 3):
        print("Three machines algorithm")
        return johnson3m(tasks)


def johnson2m(tasks):
    tmp_tasks = tasks.copy()

    mt_row = 0
    mt_column = 0
    tab1 = []
    tab2 = []
    iter = 0
    while(iter != len(tasks)):
        min_time = 100
        for i in range(0, len(tasks)):
            for j in range(0, len(tasks[i])):
                if(min_time > tasks[i][j]):
                    min_time = tasks[i][j]
                    mt_row = i
                    mt_column = j
        tasks[mt_row] = 1000

        if (mt_column == 0):
            tab1.append(mt_row)
        if (mt_column == 1):
            tab2.append(mt_row)
        iter = iter +1

    sequence = tab1 + list(reversed(tab2))


    print("Best sequence: ", sequence)
    print("Two machines algorithm: DONE")


def transform3to2(tasks):
    virtual = np.zeros((len(tasks),2))

    for i in range(0, len(tasks)):
        virtual[i][0] = tasks[i][0] + tasks[i][1]
        virtual[i][1] = tasks[i][1] + tasks[i][2]

    print("Virtual machines: \n", virtual)
    return virtual


def johnson3m(tasks):
    print("Three machines algorithm: START")
    virtual_machine = transform3to2(tasks)
    johnson2m(virtual_machine)
    print("Three machines algorithm: DONE")

def permute(x, index=0):
    if index+1 >= len(x):
        yield x
    else:
        for p in permute(x, index+1):
            yield p
        for i in range(index+1,len(x)):
            x[index], x[i]=x[i], x[index]
            for p in permute(x,index+1):
                yield p
            x[index], x[i]=x[i], x[index]


def makespan(order, tasks, machines_val):
    times = []
    for i in range(0, machines_val):
        times.append(0)
    for j in order:
        times[0] += tasks[j][0]
        for k in range(1, machines_val):
            if times[k] < times[k-1]:
                times[k] = times[k-1]
            times[k] += tasks[j][k]
    return max(times)


def bruteforce(tasks, machines_val, tasks_val):
    figure = PrettyTable()
    figure.field_names = ["Sequence", "Makespan"]
    print("Starting bruteforce")
    t = []
    min_time = 1000
    for z in range(0, tasks_val):
        t.append(z)
    for p in permute(t):
        tmp = makespan(p, tasks, machines_val)
        figure.add_row([format(p), tmp ])
        if (tmp < min_time):
            min_time = tmp
            best_permute = format(p)
    print(figure)
    print("Min time:", min_time, "  for :", format(best_permute), "permutation")
    print("Bruteforce: DONE")


def read_data(filename):
    file = open(filename, "r")

    tasks_val, machines_val = file.readline().split()
    tasks_val = int(tasks_val)
    machines_val = int(machines_val)

    tasks = np.zeros((tasks_val,machines_val))
    for i in range(tasks_val):
        tmp = file.readline().split()
        for j in range(machines_val):
            tasks[i][j] = int(tmp[j])

    print("Number of tasks: ", tasks_val)
    print("Number of machines: ", machines_val)
    print("Tasks: \n", tasks)
    file.close()
    return tasks_val, machines_val, tasks

if __name__=="__main__":
    ##############################################
    TWO_OR_THREE = 3  # Two or three machines algorithm??
    ##############################################
    print("Starting program...")

    ##MAIN##
    if (TWO_OR_THREE == 2):
        tasks_num, machines_num, tasks = read_data("../data/flowshop_2machines.txt")
    if (TWO_OR_THREE == 3):
        tasks_num, machines_num, tasks = read_data("../data/flowshop_3machines.txt")
        print("The package ta000 has been loaded")

    bruteforce(tasks, machines_num, tasks_num)
    johnson_algorithm(machines_num, tasks)
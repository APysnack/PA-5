from collections import defaultdict
from operator import attrgetter
from itertools import permutations


class Tasks:
    def __init__(self, task_id, earnings, start_time, end_time):
        self.task_id = task_id
        self.earnings = earnings
        self.start_time = start_time
        self.end_time = end_time
        self.duration = (end_time - start_time)
        self.bang_4_buck = (self.earnings / self.duration)


def is_valid(num_list):
    length = len(num_list)
    i = 0
    valid = False

    while i < length:
        if i+2 > length:
            break
        if task_list[num_list[i] - 1].end_time <= task_list[num_list[i+1] - 1].start_time:
            valid = True
        else:
            valid = False
            break
        i += 1

    return valid


def brute_force():
    length = len(task_list)
    num_list = range(1, 9)
    valid_list = []
    earning_list = []

    # creates every possible permutation of the list items
    for i in range(1, length + 1):
        perm = permutations(num_list, i)

        # finds all permutations that have valid path sequences
        for j in perm:
            if is_valid(j):
                # creates a list of all the valid sequences
                valid_list.append(j)

    # sums up the totals of the valid sequences
    for item in valid_list:
        total = 0
        for instance in item:
            total += task_list[instance-1].earnings
        earning_list.append(total)

    return max(earning_list)


# ---------------------------------------------------------------- #
def add_tasks():
    task_continue = 'y'
    i = 1

    while task_continue == 'y' or task_continue == 'Y':
        try:
            task_earnings = int(input("Please enter the earnings value for this task:\n"))
            task_start = int(input("Please enter the start time for this task:\n"))
            task_end = int(input("Please enter the end time for this task:\n"))

            while task_end < task_start:
                task_end = int(input(f"Please select a task end time greater than the start time ({task_start}):\n"))

            task_list.append(Tasks(i, task_earnings, task_start, task_end))
            i += 1
            task_continue = input("Would you like to add another task? Y/N?\n")

        except ValueError:
            print("Please only use integer values")

    return task_list


# ---------------------------------------------------------------- #
def prev(n):
    n_start = task_list[n-1].start_time
    n_prev = 0

    # cycles through list of tasks
    for i, task in enumerate(task_list):
        # if n_prev has been changed from its initial value of 0
        if n_prev > 0:
            # finds the latest task end time that's less than or equal to the start of n
            if n_start >= task.end_time > task_list[n_prev-1].end_time:
                n_prev = task.task_id
        else:
            # else, n_prev is 0 and assigns it to the first task that ends before n starts
            if n_start >= task.end_time:
                n_prev = task.task_id

    return n_prev


# ---------------------------------------------------------------- #
def recursive_max(n):

    if n == 0:
        return 0

    previous = prev(n)

    # foo, can i remove this and only use the recursive function?
    if previous in path_dict:
        do_task = value(n) + value_dict[previous][0]

    else:
        do_task = value(n) + recursive_max(previous)

    if n-1 in path_dict:
       dont_do_task = value_dict[n-1][0]
    else:
        dont_do_task = recursive_max(n - 1)

    if do_task > dont_do_task:
        if n not in path_dict:
            if previous > 0:
                for path in path_dict[previous]:
                    path_dict[n].append(path)

            path_dict[n].append(n)

            value_dict[n].append(do_task)

        return do_task

    # otherwise, return the value for not doing the task
    else:
        if n not in path_dict:

            for path in path_dict[n-1]:
                path_dict[n].append(path)

            value_dict[n].append(dont_do_task)

        return dont_do_task


# ---------------------------------------------------------------- #
def value(n):
    n_value = task_list[n-1].earnings
    return n_value

# ---------------------------------------------------------------- #
def non_recursive_max(n):
    prev_list = []
    opt_list = [0]

    # gets a list of each element's previous value
    for task in task_list:
        prev_list.append(prev(task.task_id))

    # for each element in thee array
    for j in range(1, len(task_list) + 1):
        # a is the value of doing the task, j earnings + max(j-1)
        a = task_list[j-1].earnings + opt_list[prev_list[j-1]]

        # b is the value of not doing the task, the max(j-1)
        b = opt_list[j-1]

        # if do task > dont do task
        if a > b:
            # if the current value of j does not have a key in the path dict
            if j not in path_dict:

                # if the task has a previous task
                if prev_list[j - 1] > 0:

                    # for each path in the prev dictionary key (e.g. prev = 4 has path [1, 4])
                    for path in path_dict[prev_list[j-1]]:
                        # add those paths to j's list of paths
                        path_dict[j].append(path)
                # finally, add the current path
                path_dict[j].append(j)

        # else if dont do task > do task
        elif b > a:
            # if j is not in the path dictionary
            if j not in path_dict:
                # for each path in the j - 1 path, add it to j's path
                for path in path_dict[j - 1]:
                    path_dict[j].append(path)


        opt_list.append(max(a, b))

    print(path_dict)

    return opt_list[n]

# ---------------------------------------------------------------- #
# takes a number n and the list of all tasks
def calculate():
    # for i in range(6):
    #     recursive_max(i + 1)

    # path_dict[0].append(0)
    # non_recursive_max(3)

    brute_force()


# ---------------------------------------------------------------- #
def user_menu():
    option_list = [1, 2, 3, 4]
    user_input = -2

    while user_input != 4:
        try:
            user_input = int(input("Please select from the following options:\n"
                                   "1. Enter new Tasks\n"
                                   "2. View All Tasks\n"
                                   "3. Delete a Task\n"
                                   "4. Exit Program (Data will be lost)\n"))

            if user_input not in option_list:
                print("Please choose a number from 1 - 4")

            if user_input == 1:
                task_list = add_tasks()

            # elif user_input == 2:
            # elif user_input == 3:
            # elif user_input == 4:

        except ValueError:
            print("Please enter an integer value")

    return task_list


if __name__ == '__main__':
    task_list = [
        Tasks(1, 5, 1, 4),
        Tasks(2, 1, 3, 5),
        Tasks(3, 8, 0, 6),
        Tasks(4, 4, 4, 7),
        Tasks(5, 6, 3, 8),
        Tasks(6, 3, 5, 9),
        Tasks(7, 2, 6, 10),
        Tasks(8, 4, 8, 11)
    ]

    value_dict = defaultdict(list)
    path_dict = defaultdict(list)

    calculate()




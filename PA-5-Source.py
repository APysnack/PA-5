from collections import defaultdict
from operator import attrgetter
from itertools import permutations
from time import perf_counter_ns
import chart


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
        if i + 2 > length:
            break
        if task_list[num_list[i] - 1].end_time <= task_list[num_list[i + 1] - 1].start_time:
            valid = True
        else:
            valid = False
            break
        i += 1

    return valid


def get_valid_paths():
    length = len(task_list)
    num_list = range(1, length + 1)
    valid_list = []

    # creates every possible permutation of the list items
    for i in num_list:
        perm = permutations(num_list, i)

        # finds all permutations that have valid path sequences
        for j in perm:
            if is_valid(j):
                # creates a list of all the valid sequences
                valid_list.append(j)

    return valid_list


def brute_force():
    earning_list = []

    valid_list = get_valid_paths()

    # sums up the totals of the valid sequences
    for item in valid_list:
        total = 0
        for instance in item:
            total += task_list[instance - 1].earnings
        earning_list.append(total)

    max_earnings = 0
    index = 0

    for i, earnings in enumerate(earning_list):
        if earnings > max_earnings:
            max_earnings = earnings
            index = i

    if not valid_list:
        for task in task_list:
            valid_list.append([task.task_id])
            if task.earnings > max_earnings:
                max_earnings = task.earnings


    return max_earnings, valid_list[index], earning_list


# ---------------------------------------------------------------- #
def add_tasks():
    task_list.clear()
    task_continue = 'y'
    i = 1
    j = 1

    print("\nThe task list has been emptied.\n")

    while task_continue == 'y' or task_continue == 'Y':
        try:
            task_earnings = int(input(f"Please enter the earnings value for task {j}:\n"))
            while task_earnings < 0:
                task_earnings = int(input(f"Please enter a positive number for the earnings value of Task {j}:\n"))

            task_start = int(input(f"Please enter the start time for task {j}:\n"))
            while task_start < 0:
                task_start = int(input(f"Please enter a positive number for the start time of Task {j}:\n"))

            task_end = int(input(f"Please enter the end time for task {j}:\n"))
            while task_end < 0:
                task_end = int(input(f"Please enter a positive number for the end time of Task {j}:\n"))

            while task_end < task_start:
                task_end = int(input(f"Please select a task end time greater than the start time ({task_start}):\n"))

            task_list.append(Tasks(i, task_earnings, task_start, task_end))
            i += 1
            j += 1
            task_continue = input("Would you like to add another task? Y/N?\n")

        except ValueError:
            print("Please only use integer values")

    return task_list


# ---------------------------------------------------------------- #
def prev(n):
    n_start = task_list[n - 1].start_time
    n_prev = 0

    # cycles through list of tasks
    for i, task in enumerate(task_list):
        # if n_prev has been changed from its initial value of 0
        if n_prev > 0:
            # finds the latest task end time that's less than or equal to the start of n
            if n_start >= task.end_time > task_list[n_prev - 1].end_time:
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

    if n - 1 in path_dict:
        dont_do_task = value_dict[n - 1][0]
    else:
        dont_do_task = recursive_max(n - 1)

    if do_task > dont_do_task:
        if n not in path_dict:
            if previous > 0:
                for path in path_dict[previous]:
                    path_dict[n].append(path)

            path_dict[n].append(n)

            value_dict[n].append(do_task)
        return do_task, path_dict[n]

    # otherwise, return the value for not doing the task
    else:
        if n not in path_dict:

            for path in path_dict[n - 1]:
                path_dict[n].append(path)

            value_dict[n].append(dont_do_task)

        return dont_do_task, path_dict[n - 1]


# ---------------------------------------------------------------- #
def value(n):
    n_value = task_list[n - 1].earnings
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
        a = task_list[j - 1].earnings + opt_list[prev_list[j - 1]]

        # b is the value of not doing the task, the max(j-1)
        b = opt_list[j - 1]

        # if do task > dont do task
        if a > b:
            # if the current value of j does not have a key in the path dict
            if j not in path_dict:

                # if the task has a previous task
                if prev_list[j - 1] > 0:

                    # for each path in the prev dictionary key (e.g. prev = 4 has path [1, 4])
                    for path in path_dict[prev_list[j - 1]]:
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

    return opt_list[n], path_dict[n]


def format_output(r_max, r_path, r_time, nr_max, nr_path, nr_time, bf_max, bf_path, bf_time, valid_paths, earning_list):
    num_paths = len(valid_paths)

    output = ''
    output += f'The time elapsed in the brute-force algorithm is {bf_time} nanoseconds\n'
    output += f'The time elapsed in the recursive DP algorithm is {r_time} nanoseconds\n'
    output += f'The time elapsed in the non-recursive DP algorithm is {nr_time} nanoseconds\n\n'

    output += f'Bruteforce Optimum:'
    for item in bf_path:
       output += f' Task {item} -->'
    output += f' With a total earning of {bf_max}\n'

    output += f'Recursive DP Optimum:'
    for item in r_path:
        output += f' Task {item} -->'
    output += f' With a total earning of {r_max}\n'

    output += f'Bruteforce Optimum:'
    for item in nr_path:
        output += f' Task {item} -->'
    output += f' With a total earning of {nr_max}\n\n'

    output += f'There are {num_paths} ways to select non-individual sets of tasks: \n'
    for i, valid_path in enumerate(valid_paths):
        output += f'Option {i+1}: '
        for path in valid_path:
            output += f' {path} --> '
        output += f'with a total earning of {earning_list[i]}\n'



    return output


# ---------------------------------------------------------------- #
# takes a number n and the list of all tasks
def calculate():

    if not task_list:
        print("List is empty, please try again after entering values")
        return

    length = len(task_list)
    r_max_earnings, nr_max_earnings, bf_max_earnings = 0, 0, 0
    r_path, nr_path, bf_path = [], [], ()

    start_time = perf_counter_ns()
    for i in range(length):
        r_max_earnings, r_path = recursive_max(i + 1)
    end_time = perf_counter_ns()
    recursive_elapsed = end_time - start_time

    value_dict.clear()
    path_dict.clear()

    path_dict[0].append(0)
    start_time = perf_counter_ns()
    nr_max_earnings, nr_path = non_recursive_max(length)
    end_time = perf_counter_ns()
    non_recursive_elapsed = end_time - start_time

    value_dict.clear()
    path_dict.clear()

    start_time = perf_counter_ns()
    bf_max_earnings, bf_path, earning_list = brute_force()
    end_time = perf_counter_ns()
    bf_elapsed = end_time - start_time

    valid_paths = get_valid_paths()

    output_string = format_output(r_max_earnings, r_path, recursive_elapsed, nr_max_earnings, nr_path,
                           non_recursive_elapsed, bf_max_earnings, bf_path, bf_elapsed, valid_paths, earning_list)

    return output_string


def view_tasks():
    out_str = '\nCurrent Task List\n'
    out_str += '--------------------------------------------------------\n'

    for item in task_list:
        out_str += f'Task ID: {item.task_id} || Start Time: {item.start_time} || End Time: {item.end_time} || ' \
                   f'Value: {item.earnings}\n'

    out_str += '--------------------------------------------------------\n'

    print(out_str)


def delete_task():
    num_list = []
    num_range = range(1, len(task_list) + 1)
    for num in num_range:
        num_list.append(num)

    del_id = int(input("Please select a Task ID that you would like to delete\n"))

    if del_id in num_list:
        task_list.pop(del_id - 1)
        copy_list = task_list.copy()
        task_list.clear()
        i = 1

        print(copy_list)

        for item in copy_list:
            task_list.append(Tasks(i, item.earnings, item.start_time, item.end_time))
            i += 1

        print("Task deleted from list!\n")

    else:
        print("Not in list")

# ---------------------------------------------------------------- #
def user_menu():
    option_list = [1, 2, 3, 4, 5]
    user_input = -1

    while user_input != 5:
        try:
            user_input = int(input("\nPlease select from the following options:\n"
                                   "1. Enter new Tasks\n"
                                   "2. View List of Tasks\n"
                                   "3. Delete a Task\n"
                                   "4. Calculate Optimal Path\n"
                                   "5. Terminate Program Immediately\n"))

            if user_input not in option_list:
                print("Please choose a number from 1 - 5")

            if user_input == 1:
                task_list = add_tasks()

            elif user_input == 2:
                view_tasks()

            elif user_input == 3:
                delete_task()

            elif user_input == 4:
                return -2

            elif user_input == 5:
                print("Goodbye")
                return -1

        except ValueError:
            print("Please enter an integer value")

    return task_list


if __name__ == '__main__':
    task_list = []
    value_dict = defaultdict(list)
    path_dict = defaultdict(list)

    user_continue = user_menu()

    if user_continue == -2:
        output = calculate()
        ordered_list = sorted(task_list, key=attrgetter("end_time"), reverse=True)
        chart.display_chart(ordered_list, output)
        calculate()
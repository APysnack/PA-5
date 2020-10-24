import matplotlib.pyplot as plt
import random


def display_chart(task_list):

    fig, gnt = plt.subplots()
    end = task_list[0].end_time
    list_range = range(1, end + 1)
    range_list = []
    name_list = []
    tick_list = [0]

    for num in list_range:
        range_list.append(num)
        tick_list.append(num*10)

    duration_list = []

    for task in task_list:
        start = task.start_time
        duration = task.duration
        duration_list.append((start, duration))
        name_list.append(task.task_id)

    for i, x in enumerate(duration_list):
        b = random.random()
        r = random.random()
        g = (random.randrange(2, 9, 1) / 10)
        color = (r, g, b)
        gnt.broken_barh([duration_list[i]], ((i+1)*10, 10), color=color, edgecolor='b', label=f'Task #{name_list[i]}: {task_list[i].earnings}')

    handles, labels = gnt.get_legend_handles_labels()
    gnt.legend(reversed(handles), reversed(labels), loc='upper right')
    gnt.grid(True)
    gnt.set_yticklabels([])
    gnt.set_yticks(tick_list)
    gnt.set_xticks(range_list)
    gnt.set_xlabel('Time')
    gnt.set_ylabel('Processes')
    gnt.set_title('Weighted Job Scheduling')

    plt.show()
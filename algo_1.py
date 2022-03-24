import numpy as np
from task import Task

def NIRR(task_dataset: list):
    ARRIVE_QUEUE = list()
    REQUEST_QUEUE = list()
    DONE_LIST = list()

    # Adding the first arrived task with arrival time 0
    while (task_dataset[0].get_arrival_time() == 0):
        ARRIVE_QUEUE.append(task_dataset.pop(0))

    QT = 0; TIME = 0; CS = 0; number_of_QT_calculations = 0
    while len(ARRIVE_QUEUE) > 0:

        # Move all the current tasks in the arrive queue to the REQUEST
        REQUEST_QUEUE.extend(ARRIVE_QUEUE[:])
        ARRIVE_QUEUE.clear()

        # Calculate the quantum time 
        number_of_QT_calculations += 1
        if len(REQUEST_QUEUE) == 1 & REQUEST_QUEUE[0].get_id() == 1:
                QT = REQUEST_QUEUE[0].get_burst_time()
        else:
            QT = round(np.mean([task.get_remaining_burst_time() for task in REQUEST_QUEUE]))
            REQUEST_QUEUE.sort(key = lambda TASK: TASK.get_remaining_burst_time(), reverse=False)

        while len(REQUEST_QUEUE) > 0:
            current_task = REQUEST_QUEUE[0]
            
            # CPU allocation 
            # print('[CPU] Allocating task: ', current_task.get_id(), 'QT: ', QT)
            TIME += current_task.allocate_to_CPU(TIME, QT)
            CS += 1
            if current_task.get_remaining_burst_time() == 0: # Finished
                current_task.is_finished(TIME)
                DONE_LIST.append(current_task)
                REQUEST_QUEUE.pop(0)

            # Short enought Bt to finish anyway?
            elif current_task.get_remaining_burst_time() <= QT/2:
                # CPU allocation 
                TIME += current_task.allocate_to_CPU(TIME, QT)
                # CS += 1 - NO! The task just stays in the CPU
                if current_task.get_remaining_burst_time() == 0: # Finished
                    current_task.is_finished(TIME)
                    DONE_LIST.append(current_task)
                    REQUEST_QUEUE.pop(0)

            # Move task back to arrive queue 
            else:
                ARRIVE_QUEUE.append(current_task)
                REQUEST_QUEUE.pop(0)

        # Insert all the "arrived" tasks in the ARRIVE_QUEUE
        while len(task_dataset) > 0:
            if task_dataset[0].get_arrival_time() <= TIME:
                ARRIVE_QUEUE.append(task_dataset.pop(0))
            else:
                break

    CS -= 1 # It never switches from the last task... 
    return DONE_LIST, CS, number_of_QT_calculations

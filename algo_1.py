from copy import deepcopy
from logging import exception

def IDRR(dataset: list):
    task_dataset = deepcopy(dataset)
    REQUEST_QUEUE = list()
    DONE_LIST = list()

    # Adding the first arrived task with arrival time 0 (from the back!)
    while len(task_dataset) != 0 and task_dataset[-1].get_arrival_time() == 0:
        REQUEST_QUEUE.append(task_dataset.pop())

    QT = 0; TIME = 0; CS = 0; number_of_QT_calculations = 0; FIRST_QT = True; NEW_ROUND = False
    # Move all the current tasks in the arrive queue to the REQUEST

    # Calculate the first QT
    number_of_QT_calculations += 1
    if len(REQUEST_QUEUE) == 1:
        QT = REQUEST_QUEUE[0].get_burst_time()
    else:
        TEMP = sorted(REQUEST_QUEUE, key=lambda TASK: TASK.get_remaining_burst_time())
        QT = round(REQUEST_QUEUE[0].get_remaining_burst_time() + QT)/2 - round(TEMP[0].get_arrival_time() + TEMP[1].get_arrival_time())/2
        FIRST_QT = False

    while len(REQUEST_QUEUE) > 0:
        current_task = REQUEST_QUEUE[-1]

        # CPU allocation
        # print('[CPU] Allocating task: ', current_task.get_id(), 'QT: ', QT, 'TIME: ', TIME)
        TIME += current_task.allocate_to_CPU(TIME, QT); CS += 1
        if current_task.get_remaining_burst_time() == 0:  # Finished?
            current_task.is_finished(TIME)
            DONE_LIST.append(current_task)
            REQUEST_QUEUE.pop()

        # Move task to the back of the request queue 
        else:
            REQUEST_QUEUE.insert(0, current_task)
            REQUEST_QUEUE.pop()

        # Is this a new round?
        if (len(REQUEST_QUEUE) == 0 and len(task_dataset) != 0):
            NEW_ROUND = True
        elif len(REQUEST_QUEUE) != 0 and REQUEST_QUEUE[-1].get_remaining_burst_time() != REQUEST_QUEUE[-1].get_burst_time():
            NEW_ROUND = True
        else:
            NEW_ROUND = False
        
        if NEW_ROUND:
            # Insert all the "arrived" tasks in the ARRIVE_QUEUE
            while len(task_dataset) > 0:
                if task_dataset[-1].get_arrival_time() <= TIME:
                    REQUEST_QUEUE.append(task_dataset.pop())
                else:
                    break
                
            # Calculate the quantum time
            if len(REQUEST_QUEUE) == 0:
                break 
            elif len(REQUEST_QUEUE) == 1:
                number_of_QT_calculations += 1
                QT = REQUEST_QUEUE[0].get_remaining_burst_time()
            else:
                REQUEST_QUEUE.sort(key=lambda TASK: TASK.get_remaining_burst_time(), reverse=True)
                number_of_QT_calculations += 1
                if FIRST_QT:
                    TEMP = sorted(REQUEST_QUEUE, key=lambda TASK: TASK.get_arrival_time())
                    QT = round(REQUEST_QUEUE[0].get_remaining_burst_time() + QT)/2 - round(TEMP[0].get_arrival_time() + TEMP[1].get_arrival_time())/2
                    FIRST_QT = False
                else:
                    TEMP = sorted(REQUEST_QUEUE, key=lambda TASK: TASK.get_arrival_time())
                    QT = round(REQUEST_QUEUE[0].get_remaining_burst_time() + QT)/2 - round(TEMP[0].get_arrival_time()/2)
        
        # Edge case, but can happen even with a reasonable dataset 
        if QT <= 0:
            raise ValueError(f'[IDRR] QT calculated to: {QT}')
        
    CS -= 1  # It never switches from the last task...
    return DONE_LIST, CS, number_of_QT_calculations

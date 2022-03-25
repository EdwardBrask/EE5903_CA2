from copy import deepcopy
from task import Task
from algo_1 import IDRR
from algo_2 import NIRR

# Will always be reverse sorted after arrival time. 
# Task number and arrival time need to match, 
# The first task must have arrival time = 0 
task_dataset = [Task(5, 20, 35), Task(4, 14, 115), Task(3, 8, 65), Task(2, 2, 95), Task(1, 0, 75)]

def calculate_and_print_results(algo_name: str, results: list, CS, n_calcs: int, by_task=False) -> None:
    ART = 0; AWT = 0; ATT = 0
    for done_task in results:
        ART += done_task.response_time; AWT += done_task.waiting_time; ATT += done_task.turnaround_time
    ART = ART/len(results); AWT = AWT/len(results); ATT = ATT/len(results)   
    print(f'Summary of {algo_name} with {len(results)} tasks: \nAverage response time {ART} \nAverage waiting time {AWT}',
        f'\nAverage turnaround time {ATT} \nContext switches: {CS} \nNumber of QT calculations: {n_calcs}')

    if by_task:
        for done_task in results:
            print('Task: ', done_task.get_id(), 
                f'\n-RT: {done_task.response_time},',
                f' -WT: {done_task.waiting_time},',
                f' -TT: {done_task.turnaround_time},')
    print('\n')

if __name__ == "__main__":
    IDRR_tasks = deepcopy(task_dataset)
    [IDRR_RESULTS, IDRR_CS, n_calcs] = IDRR(IDRR_tasks)
    calculate_and_print_results('IDRR', IDRR_RESULTS, IDRR_CS, n_calcs)

    NIRR_tasks = deepcopy(task_dataset)
    [NIRR_RESULTS, NIRR_CS, n_calcs] = NIRR(NIRR_tasks)
    calculate_and_print_results('NIRR', NIRR_RESULTS, NIRR_CS, n_calcs)

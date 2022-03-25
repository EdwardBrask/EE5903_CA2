from task import Task
from random import random
from algo_1 import IDRR
from algo_2 import NIRR

# Will always be reverse sorted after arrival time. 
# Task number and arrival time need to match, 
# The first task must have arrival time = 0 

# task_dataset = [Task(5, 20, 35), Task(4, 14, 115), Task(3, 8, 65), Task(2, 2, 95), Task(1, 0, 75)]

def generate_dataset(N: int , ART_bound: list, BT_bound: list) -> list:
    arrival_times = list()
    output = list()
    for _ in range(N):
        arrival_times.append(round(random()*(ART_bound[1] - ART_bound[0]) + ART_bound[0]))
    arrival_times.sort(reverse=True)

    arrival_times[N-1] = 0 # Need to force this 

    for art, i in zip(arrival_times, range(N)):
        bt = round(random()*(BT_bound[1] - BT_bound[0]) + BT_bound[0])
        output.append(Task(N-i, art, bt))
    
    return output

def calculate_and_print_results(algo_name: str, results: list, CS, n_calcs: int, by_task=False) -> list:
    ART = 0; AWT = 0; ATT = 0
    for done_task in results:
        ART += done_task.response_time; AWT += done_task.waiting_time; ATT += done_task.turnaround_time
    ART = ART/len(results); AWT = AWT/len(results); ATT = ATT/len(results)   
    print(f'Summary of {algo_name} with {len(results)} tasks: \nART {ART:.2f} \nAWT: {AWT:.2f}',
        f'\nATT: {ATT:.2f} \nCS: {CS} \nNQTC: {n_calcs}')

    if by_task:
        for done_task in results:
            print('Task: ', done_task.get_id(), 
                f'\n-RT: {done_task.response_time},',
                f' -WT: {done_task.waiting_time},',
                f' -TT: {done_task.turnaround_time},')
    print('\n')
    return ART, AWT, ATT

if __name__ == "__main__":

    task_dataset = generate_dataset(10, [0, 10], [10, 100])
    
    #[IDRR_RESULTS, IDRR_CS, n_calcs] = IDRR(task_dataset)
    #[ART, AWT, ATT] = calculate_and_print_results('IDRR', IDRR_RESULTS, IDRR_CS, n_calcs)

    [NIRR_RESULTS, NIRR_CS, n_calcs] = NIRR(task_dataset)
    [ART, AWT, ATT] = calculate_and_print_results('NIRR', NIRR_RESULTS, NIRR_CS, n_calcs)
    

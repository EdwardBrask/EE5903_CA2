import numpy as np
from time import time
import matplotlib.pyplot as plt
from random import random
from algo_1 import IDRR
from algo_2 import NIRR

class Task:
    def __init__(self, id=int, arrival_time=int, burst_time=int):
        self.data = [id, arrival_time, burst_time]
        self.allocated = False
        self.response_time = 0
        self.remaining_burst_time = burst_time
        self.finish_time = 0
        self.waiting_time = 0
        self.turnaround_time = 0
    
    def __repr__(self) -> str:
        return f'T_{self.data[0]}({self.data[1]}, {self.data[2]})'
    
    def get_id(self) -> int: 
        return self.data[0]
    
    def get_arrival_time(self) -> int: 
        return self.data[1]
    
    def get_burst_time(self) -> int: 
        return self.data[2]
    
    def get_remaining_burst_time(self) -> int: 
        return self.remaining_burst_time
    
    def allocate_to_CPU(self, time: int, QT: int) -> int: 
        if not self.allocated:
            self.response_time = time - self.get_arrival_time()
            self.allocated = True
        
        # Return the time the task is processed in the CPU
        if QT >= self.remaining_burst_time:
            output = self.remaining_burst_time; self.remaining_burst_time = 0
            return output
        else: 
            self.remaining_burst_time -= QT
            return QT
    
    def calculate_results(self) -> None:
        self.turnaround_time = self.finish_time - self.get_arrival_time()
        self.waiting_time = self.turnaround_time - self.get_burst_time()
        
    def is_finished(self, time: int) -> None: 
        self.finish_time = time
        self.calculate_results()

def generate_dataset(N: int , ART_bound: list, BT_bound: list) -> list:
    # Will always be reverse sorted after arrival time. 
    # Task number and arrival time need to match, 
    # The first task must have arrival time = 0 
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

def calculate_results(algo_name: str, results: list, CS, NOQTC: int, print_results=False, print_by_task=False) -> list:
    ART = 0; AWT = 0; ATT = 0
    for done_task in results:
        ART += done_task.response_time; AWT += done_task.waiting_time; ATT += done_task.turnaround_time
    ART = ART/len(results); AWT = AWT/len(results); ATT = ATT/len(results)   

    if print_results:
        print(f'\nSummary of {algo_name} with {len(results)} tasks: \nART {ART:.2f} \nAWT: {AWT:.2f}',
            f'\nCS: {CS} \nNOQTC: {NOQTC}')

    if print_by_task:
        for done_task in results:
            print('Task: ', done_task.get_id(), 
                f'\n-RT: {done_task.response_time},',
                f' -WT: {done_task.waiting_time},',
                f' -TT: {done_task.turnaround_time},')

    return ART, AWT, ATT

def simulate_and_plot(N_tasks, interval, task_dataset, IDRR_to_txt=True, NIRR_to_txt=True, plot_ART=True, plot_AWT=True, plot_CS=True, plot_NOQTC=True):
    time_start = time()
    print(f'Starting simulation with {N_tasks} tasks, evaluated at every {interval} number of tasks.')
    number_of_tasks = np.linspace(interval, N_tasks, int(N_tasks/interval))

    IDRR_art = list(); IDRR_awt = list(); IDRR_cs = list(); IDRR_noqtc = list(); 
    NIRR_art = list(); NIRR_awt = list(); NIRR_cs = list(); NIRR_noqtc = list(); 

    for x in number_of_tasks:
        [IDRR_RESULTS, IDRR_CS, IDRR_NOQTC] = IDRR(task_dataset[N_tasks-int(x):])
        [ART, AWT, ATT] = calculate_results('IDRR', IDRR_RESULTS, IDRR_CS, IDRR_NOQTC, print_by_task=False)
        IDRR_art.append(ART); IDRR_awt.append(AWT); IDRR_cs.append(IDRR_CS); IDRR_noqtc.append(IDRR_NOQTC) 

        [NIRR_RESULTS, NIRR_CS, NIRR_NOQTC] = NIRR(task_dataset[N_tasks-int(x):])
        [ART, AWT, ATT] = calculate_results('NIRR', NIRR_RESULTS, NIRR_CS, NIRR_NOQTC, print_by_task=False)
        NIRR_art.append(ART); NIRR_awt.append(AWT); NIRR_cs.append(NIRR_CS); NIRR_noqtc.append(NIRR_NOQTC) 
    
    if (IDRR_to_txt):
        fid = open('IDRR_results.txt', 'w')
        print('ART      |AWT      |CS       |NOQTC    ', file=fid)
        for i in range(int(N_tasks/interval)):
            print('%8.2f |%8.2f |%8.2f |%8.2f' % (IDRR_art[i], IDRR_awt[i], IDRR_cs[i], IDRR_noqtc[i]), file=fid)
        fid.close() 
    
    if (NIRR_to_txt):
        fid = open('NIRR_results.txt', 'w')
        print('ART      |AWT      |CS       |NOQTC    ', file=fid)
        for i in range(int(N_tasks/interval)):
            print('%8.2f |%8.2f |%8.2f |%8.2f' % (NIRR_art[i], NIRR_awt[i], NIRR_cs[i], NIRR_noqtc[i]), file=fid)
        fid.close() 

    if plot_ART:
        plt.plot(number_of_tasks, IDRR_art, 'b--', label='IDRR - ART', linewidth=2)
        plt.plot(number_of_tasks, NIRR_art, 'k--', label='NIRR - ART', linewidth=2)
        plt.legend()
        plt.title("IDRR vs. NIRR")
        plt.xlabel('Number of tasks')
        plt.ylabel('ART')
        plt.savefig('ART.png')
        plt.close()
    
    if plot_AWT:
        plt.plot(number_of_tasks, IDRR_awt, 'b--', label='IDRR - AWT', linewidth=2)
        plt.plot(number_of_tasks, NIRR_awt, 'k--', label='NIRR - AWT', linewidth=2)
        plt.legend()
        plt.title("IDRR vs. NIRR")
        plt.xlabel('Number of tasks')
        plt.ylabel('AWT')
        plt.savefig('AWT.png')
        plt.close()

    if plot_CS:
        plt.plot(number_of_tasks, IDRR_cs, 'b--', label='IDRR - CS', linewidth=2)
        plt.plot(number_of_tasks, NIRR_cs, 'k--', label='NIRR - CS', linewidth=2)
        plt.legend()
        plt.title("IDRR vs. NIRR")
        plt.xlabel('Number of tasks')
        plt.ylabel('CS')
        plt.savefig('CS.png')
        plt.close()
    
    if plot_NOQTC:
        plt.plot(number_of_tasks, IDRR_noqtc, 'b--', label='IDRR - NOQTC', linewidth=2)
        plt.plot(number_of_tasks, NIRR_noqtc, 'k--', label='NIRR - NOQTC', linewidth=2)
        plt.ylim([0, max(IDRR_noqtc)+5])
        plt.legend()
        plt.title("IDRR vs. NIRR")
        plt.xlabel('Number of tasks')
        plt.ylabel('NOQTC')
        plt.savefig('NOQTC.png')
        plt.close()
    
    time_end = time()
    print(f'Simulation finisehd in {time_end - time_start:.2f} seconds!!')
    
    

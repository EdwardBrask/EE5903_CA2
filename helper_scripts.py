import numpy as np
import matplotlib.pyplot as plt
from random import random
from time import time
from algo_1 import IDRR
from algo_2 import NIRR

class Task:
    """
    This is the classs that handles the updates and calculations
    of allocating a task to the CPU and the calculating the relevant metrices.
    """
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

def generate_dataset(N_repetitions: int, N_tasks: int, ART_bound: list, BT_bound: list) -> list:
    """
    This function generates the dataset, which will be a list of the class Tasks. 
    It tales the number of simulations, number of tasks, and the arrival time burst time bounds 
    and outputs random Task(ART, BT). The tasks will always be in reverse sorted after arrival time, 
    where the task number and arrival time need to match. The first Task is forced to have 0 arrival time. 
    """
    OUTPUT = list()
    for _ in range(0, N_repetitions):
        arrival_times = list()
        tasks_n = list()
        for _ in range(N_tasks):
            arrival_times.append(round(random()*(ART_bound[1] - ART_bound[0]) + ART_bound[0]))
        arrival_times.sort(reverse=True)

        arrival_times[N_tasks-1] = 0 # Need to force this 

        for art, i in zip(arrival_times, range(N_tasks)):
            bt = round(random()*(BT_bound[1] - BT_bound[0]) + BT_bound[0])
            tasks_n.append(Task(N_tasks-i, art, bt))
        OUTPUT.append(tasks_n)
        
    return OUTPUT

def calculate_results(algo_name: str, results: list, CS, NOQTC: int, print_results=False, print_by_task=False) -> list:
    """
    This function calculates the average response time, average waiting time and average turnaround time, 
    and returns these results as separate integers. The input is the result from a single run of one of the two algorithms. 
    Extra arguments can be added to print the results. 
    """
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

def simulate_and_plot(N_repetitions: int, N_tasks: int, interval: int, task_dataset: list, IDRR_to_txt=True, NIRR_to_txt=True, plot_ART=True, plot_AWT=True, plot_CS=True, plot_NOQTC=True):
    """
    This function is the main function of the simulation code. It takes the dataset generated earlier and runs both algorithms, 
    calculates the results and writes it to .txt files and/or plots them. 
    """
    time_start = time()
    print(f'Starting {N_repetitions} simulation(s), with {N_tasks} tasks each, evaluated at every {interval} number of tasks.')
    number_of_tasks = np.linspace(interval, N_tasks, int(N_tasks/interval))

    IDRR_art = list(); IDRR_awt = list(); IDRR_cs = list(); IDRR_noqtc = list(); 
    NIRR_art = list(); NIRR_awt = list(); NIRR_cs = list(); NIRR_noqtc = list(); 


    for n in range(0, N_repetitions):
        idrr_art = list(); idrr_awt = list(); idrr_cs = list(); idrr_noqtc = list(); 
        nirr_art = list(); nirr_awt = list(); nirr_cs = list(); nirr_noqtc = list(); 

        for x in number_of_tasks:
            [idrr_results, cs, noqtc] = IDRR(task_dataset[n][N_tasks-int(x):])
            [art, awt, att] = calculate_results('IDRR', idrr_results, cs, noqtc, print_by_task=False)
            idrr_art.append(art); idrr_awt.append(awt); idrr_cs.append(cs); idrr_noqtc.append(noqtc) 

            [nirr_results, cs, noqtc] = NIRR(task_dataset[n][N_tasks-int(x):])
            [art, awt, att] = calculate_results('NIRR', nirr_results, cs, noqtc, print_by_task=False)
            nirr_art.append(art); nirr_awt.append(awt); nirr_cs.append(cs); nirr_noqtc.append(noqtc) 

        IDRR_art.append(idrr_art); IDRR_awt.append(idrr_awt); IDRR_cs.append(idrr_cs); IDRR_noqtc.append(idrr_noqtc)
        NIRR_art.append(nirr_art); NIRR_awt.append(nirr_awt); NIRR_cs.append(nirr_cs); NIRR_noqtc.append(nirr_noqtc)

    if (IDRR_to_txt):
        fid = open('IDRR_results.txt', 'w')
        print('SIM. N|ART      |AWT      |CS       |NOQTC    ', file=fid)
        for n in range(0, N_repetitions):
            for i in range(int(N_tasks/interval)):
                print('%5d |%8.2f |%8.2f |%8.2f |%8.2f' % (n, IDRR_art[n][i], IDRR_awt[n][i], IDRR_cs[n][i], IDRR_noqtc[n][i]), file=fid)
        fid.close() 
    
    if (NIRR_to_txt):
        fid = open('NIRR_results.txt', 'w')
        print('SIM. N|ART      |AWT      |CS       |NOQTC    ', file=fid)
        for n in range(0, N_repetitions):    
            for i in range(int(N_tasks/interval)):
                print('%5d |%8.2f |%8.2f |%8.2f |%8.2f' % (n, NIRR_art[n][i], NIRR_awt[n][i], NIRR_cs[n][i], NIRR_noqtc[n][i]), file=fid)
        fid.close() 

    if plot_ART:
        fig1 = plt.figure(1)
        for n in range(0, N_repetitions):
            if n == 0:
                plt.plot(number_of_tasks, IDRR_art[n], 'b--', label='IDRR - ART', linewidth=2)
                plt.plot(number_of_tasks, NIRR_art[n], 'k--', label='NIRR - ART', linewidth=2)
            else:
                plt.plot(number_of_tasks, IDRR_art[n], 'b--', linewidth=2)
                plt.plot(number_of_tasks, NIRR_art[n], 'k--', linewidth=2)
        plt.legend()
        plt.title("IDRR vs. NIRR")
        plt.xlabel('Number of tasks')
        plt.ylabel('ART')
        plt.savefig('ART.png')
        plt.close()
    
    if plot_AWT:
        for n in range(0, N_repetitions):
            if n == 0:
                plt.plot(number_of_tasks, IDRR_awt[n], 'b--', label='IDRR - AWT', linewidth=2)
                plt.plot(number_of_tasks, NIRR_awt[n], 'k--', label='NIRR - AWT', linewidth=2)
            else:
                plt.plot(number_of_tasks, IDRR_awt[n], 'b--', linewidth=2)
                plt.plot(number_of_tasks, NIRR_awt[n], 'k--', linewidth=2)
        plt.legend()
        plt.title("IDRR vs. NIRR")
        plt.xlabel('Number of tasks')
        plt.ylabel('AWT')
        plt.savefig('AWT.png')
        plt.close()

    if plot_CS:
        for n in range(0, N_repetitions):  
            if n == 0:
                plt.plot(number_of_tasks, IDRR_cs[n], 'b--', label='IDRR - CS', linewidth=2)
                plt.plot(number_of_tasks, NIRR_cs[n], 'k--', label='NIRR - CS', linewidth=2)
            else:
                plt.plot(number_of_tasks, IDRR_cs[n], 'b--', linewidth=2)
                plt.plot(number_of_tasks, NIRR_cs[n], 'k--', linewidth=2)    
        plt.legend()
        plt.title("IDRR vs. NIRR")
        plt.xlabel('Number of tasks')
        plt.ylabel('CS')
        plt.savefig('CS.png')
        plt.close()
    
    if plot_NOQTC:
        ylim_max = 0
        for n in range(0, N_repetitions):
            ylim_max = max(ylim_max, max(IDRR_noqtc[n]))
            if n == 0:
                plt.plot(number_of_tasks, IDRR_noqtc[n], 'b--', label='IDRR - NOQTC', linewidth=2)
                plt.plot(number_of_tasks, NIRR_noqtc[n], 'k--', label='NIRR - NOQTC', linewidth=2)
            else:
                plt.plot(number_of_tasks, IDRR_noqtc[n], 'b--', linewidth=2)
                plt.plot(number_of_tasks, NIRR_noqtc[n], 'k--', linewidth=2)    
        plt.ylim([0, ylim_max+5])
        plt.legend()
        plt.title("IDRR vs. NIRR")
        plt.xlabel('Number of tasks')
        plt.ylabel('NOQTC')
        plt.savefig('NOQTC.png')
        plt.close()
    
    time_end = time()
    print(f'Simulation finished in {time_end - time_start:.2f} seconds!!')
    
    

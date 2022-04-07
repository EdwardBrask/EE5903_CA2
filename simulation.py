import os
current_file = os.path.abspath(__file__)
current_path = os.path.split(current_file)[0]
import numpy as np
import matplotlib.pyplot as plt
from time import time
from helper_scripts import generate_dataset, calculate_results
from algo_1 import IDRR
from algo_2 import NIRR

def simulate(N_simulations: int, N_tasks: int, interval: int, arrival_time_bounds: list, burst_time_bounds: list, uniform=True, normal=False,
        IDRR_to_txt=True, NIRR_to_txt=True, plot_ART=True, plot_AWT=True, plot_CS=True, plot_NOQTC=True):
    """
    This function is the main function of the simulation code. It takes the dataset generated earlier and runs both algorithms, 
    calculates the results and writes it to .txt files and/or plots them. 

    Parameters:
        N_simulations (int): The number of simulations to be carried out consecutively, 
            hence also the number of lines for each algo on every plot. Recommended range - [1, 5]

        N_tasks (int): The number of tasks to be generated and simulated for every simulation. Recommended range - [10, 1000]

        interval (int): In which interval the results (ART/AWT/CS/NOQTC) will be calculated and saved. For instance if interval = 10, 
            for every 10 tasks from 0 to N_tasks the algorithms will be simulated and the results calculated and saved. Recommended range - [1, 100]

        arrival_time_bounds (list(lower (int), upper (int))): The upper and lower bound in which the arrival times will be uniformly distributed. 
            Recommended range, lower - [0 - 0], upper - [0, 50]
        
        burst_time_bounds (list(lower (int), upper (int))): The upper and lower bound in which the burst times will be uniformly distributed. 
            Recommended range, lower - [0 - 0], upper - [0, 50]
        
        uniform (bool): Indicating if the burst times should be uniformly distributed generated within the specified bounds.

        normal (bool): Indicating if the burst times should be normally distributed, with of mean of = 1/2*(upper - lower),
            and a standard deviation 1/4*(upper - lower) of the burst time bounds.

        IDRR_to_txt (bool): Decides if the results at every interval should be saved to a .txt file, 
            located in the 'numerical results' folder for the IDRR algorithm. 

        NIRR_to_txt (bool): Decides if the results at every interval should be saved to a .txt file,
            located in the 'numerical results' folder for the NIRR algorithm. 

        plot_*** (bool): Decides if the relevent metric should be plotted and saved to a '***.png' file located in the 'plots' folder.
    
    Output:
        plots (folder(.png)): A folder with .png plots of all the performance metrics (ART/AWT/CS/NOQTC), 
            in every plot each algorithm has 'N_simulation' number of lines. 
        
        numerical_results (folder(.txt)): A folder with .txt files of all the performance metrics (ART/AWT/CS/NOQTC).

    OBS 1!! The IDRR algorithm can compute a QT that is zero, the code will then throw 'ValueError: [IDRR] QT calculated to: 0.0'.
    This is an obvious flaw of the algorithm, and the simulation would be stuck in an infinite loop if allowed to continue. 
    Hence the program terminates and should be re-simulated. This only happened to me if the upper bound of the arrival time is close
    to the upper bound of the burst time. With 'N_simulations  = 5', 'N_tasks = 500', 'arrival_time_bounds = [0, 35]', 
    'burst_time_bounds = [1, 50]' and uniform=True it happens roughly once every 1000 times. 

    OBS 2!! The complexity of this whole simulation is very large, roughly around O(N_simulations * N_tasks^4). 
    On my machine, a 2020 Macbook Pro M1, with 'N_simulations = 5', 'N_tasks = 500' and 'interval = 10', 
    it takes ~2 seconds to run the whole program. But with 'N_simulations = 10', 'N_tasks = 1000' and 'interval = 10',
    it takes ~80 seonds... To make absolutely sure that the results are corrct the algorithms are reapplied on all the task every interval. 
    So with an interval of 10, first the algorithm run on task 0-10, then on 0-20, then on 0-30, ..., 0-N_tasks. This causes the large complexity,
    but I argue that all relevant results can be achieved within seconds anyway, so just be careful with the input parameters. 
    """
    time_start = time()
    print(f'Starting {N_simulations} simulation(s), with {N_tasks} tasks each, evaluated at every {interval} number of tasks.')
    
    if (uniform and normal) or (not uniform and not normal):
        raise InterruptedError("Choose either uniform or normal!!")

    # Generate the dataset 
    task_dataset = generate_dataset(N_simulations, N_tasks, arrival_time_bounds, burst_time_bounds, uniform, normal) 

    plt.rcParams.update({'font.size': 16}) # Change fontsize on the plots 
    plots_path = os.path.join(current_path, 'plots')
    if not os.path.exists(plots_path):
        os.makedirs(plots_path)
    numerical_results_path = os.path.join(current_path, 'numerical_results')
    if not os.path.exists(numerical_results_path):
        os.makedirs(numerical_results_path)
    
    # Apply the algorithms on the dataset 
    IDRR_ART = list(); IDRR_AWT = list(); IDRR_CS = list(); IDRR_NOQTC = list(); 
    NIRR_ART = list(); NIRR_AWT = list(); NIRR_CS = list(); NIRR_NOQTC = list(); 

    number_of_tasks = np.linspace(interval, N_tasks, int(N_tasks/interval))
    for n in range(0, N_simulations):
        idrr_art = list(); idrr_awt = list(); idrr_cs = list(); idrr_noqtc = list(); 
        nirr_art = list(); nirr_awt = list(); nirr_cs = list(); nirr_noqtc = list(); 

        for x in number_of_tasks:
            [idrr_results, cs, noqtc] = IDRR(task_dataset[n][N_tasks-int(x):])
            [art, awt, att] = calculate_results('IDRR', idrr_results, cs, noqtc, print_by_task=False)
            idrr_art.append(art); idrr_awt.append(awt); idrr_cs.append(cs); idrr_noqtc.append(noqtc) 

            [nirr_results, cs, noqtc] = NIRR(task_dataset[n][N_tasks-int(x):])
            [art, awt, att] = calculate_results('NIRR', nirr_results, cs, noqtc, print_by_task=False)
            nirr_art.append(art); nirr_awt.append(awt); nirr_cs.append(cs); nirr_noqtc.append(noqtc) 

        IDRR_ART.append(idrr_art); IDRR_AWT.append(idrr_awt); IDRR_CS.append(idrr_cs); IDRR_NOQTC.append(idrr_noqtc)
        NIRR_ART.append(nirr_art); NIRR_AWT.append(nirr_awt); NIRR_CS.append(nirr_cs); NIRR_NOQTC.append(nirr_noqtc)

    # Print the results to .txt files saved in the folder 'numerical_results'
    if IDRR_to_txt:
        fid = open(os.path.join(numerical_results_path, 'IDRR_results.txt'), 'w')
        print('SIM. N|ART      |AWT      |CS       |NOQTC    ', file=fid)
        for n in range(0, N_simulations):
            for i in range(int(N_tasks/interval)):
                print('%5d |%8.2f |%8.2f |%8.2f |%8.2f' % (n, IDRR_ART[n][i], IDRR_AWT[n][i], IDRR_CS[n][i], IDRR_NOQTC[n][i]), file=fid)
        fid.close() 
    
    if NIRR_to_txt:
        fid = open(os.path.join(numerical_results_path, 'NIRR_results.txt'), 'w')
        print('SIM. N|ART      |AWT      |CS       |NOQTC    ', file=fid)
        for n in range(0, N_simulations):    
            for i in range(int(N_tasks/interval)):
                print('%5d |%8.2f |%8.2f |%8.2f |%8.2f' % (n, NIRR_ART[n][i], NIRR_AWT[n][i], NIRR_CS[n][i], NIRR_NOQTC[n][i]), file=fid)
        fid.close() 

    # Plot the results to .png files saved in the folder 'plots'

    if uniform:
        main_string = f'Ar_t = Uniform[{arrival_time_bounds[0]}, {arrival_time_bounds[1]}], B_t = Uniform[{burst_time_bounds[0]}, {burst_time_bounds[1]}]'
    elif normal:
        main_string = f'Ar_t = Uniform[{arrival_time_bounds[0]}, {arrival_time_bounds[1]}], B_t = Normal({int(np.mean(burst_time_bounds))}, {int(1/4*(burst_time_bounds[1] - burst_time_bounds[0]))})'
    
    if plot_ART:
        for n in range(0, N_simulations):
            if n == 0:
                plt.plot(number_of_tasks, IDRR_ART[n], 'b--', label='IDRR - ART', linewidth=2)
                plt.plot(number_of_tasks, NIRR_ART[n], 'k--', label='NIRR - ART', linewidth=2)
            else:
                plt.plot(number_of_tasks, IDRR_ART[n], 'b--', linewidth=2)
                plt.plot(number_of_tasks, NIRR_ART[n], 'k--', linewidth=2)
        plt.legend()
        plt.title(main_string)
        plt.xlabel('Number of tasks')
        plt.ylabel('ART')
        plt.savefig(os.path.join(plots_path, 'ART.png'), bbox_inches='tight')
        plt.close()
    
    if plot_AWT:
        for n in range(0, N_simulations):
            if n == 0:
                plt.plot(number_of_tasks, IDRR_AWT[n], 'b--', label='IDRR - AWT', linewidth=2)
                plt.plot(number_of_tasks, NIRR_AWT[n], 'k--', label='NIRR - AWT', linewidth=2)
            else:
                plt.plot(number_of_tasks, IDRR_AWT[n], 'b--', linewidth=2)
                plt.plot(number_of_tasks, NIRR_AWT[n], 'k--', linewidth=2)
        plt.legend()
        plt.title(main_string)
        plt.xlabel('Number of tasks')
        plt.ylabel('AWT')
        plt.savefig(os.path.join(plots_path, 'AWT.png'), bbox_inches='tight')
        plt.close()

    if plot_CS:
        for n in range(0, N_simulations):  
            if n == 0:
                plt.plot(number_of_tasks, IDRR_CS[n], 'b--', label='IDRR - CS', linewidth=2)
                plt.plot(number_of_tasks, NIRR_CS[n], 'k--', label='NIRR - CS', linewidth=2)
            else:
                plt.plot(number_of_tasks, IDRR_CS[n], 'b--', linewidth=2)
                plt.plot(number_of_tasks, NIRR_CS[n], 'k--', linewidth=2)    
        plt.legend()
        plt.title(main_string)
        plt.xlabel('Number of tasks')
        plt.ylabel('CS')
        plt.savefig(os.path.join(plots_path, 'CS.png'), bbox_inches='tight')
        plt.close()
    
    if plot_NOQTC:
        ylim_max = 0
        for n in range(0, N_simulations):
            ylim_max = max(ylim_max, max(IDRR_NOQTC[n]))
            if n == 0:
                plt.plot(number_of_tasks, IDRR_NOQTC[n], 'b--', label='IDRR - NOQTC', linewidth=2)
                plt.plot(number_of_tasks, NIRR_NOQTC[n], 'k--', label='NIRR - NOQTC', linewidth=2)
            else:
                plt.plot(number_of_tasks, IDRR_NOQTC[n], 'b--', linewidth=2)
                plt.plot(number_of_tasks, NIRR_NOQTC[n], 'k--', linewidth=2)    
        plt.ylim([0, ylim_max+3])
        plt.legend(loc = 'upper left')
        plt.title(main_string)
        plt.xlabel('Number of tasks')
        plt.ylabel('NOQTC')
        plt.savefig(os.path.join(plots_path, 'NOQTC.png'), bbox_inches='tight')
        plt.close()
    
    time_end = time()
    print(f'Simulation finished in {time_end - time_start:.2f} seconds!!')
    
    
# EE5903_CA2
This is the project repo for the implementation, simulation and analysis of two improved Round Robin CPU scheduling algorithms, called Improved Dynamic RR and a New Improved RR.

Installation procedure/requirements
    - This project is built on python3.8, but any 3.x should work fine. There is a requirements.txt file included with what I currently have, but the inly packages used are numpy and matplotlib which are very standard. In general it should just be plug and play. 

Running instructions
    - Everything is executed from the main.py file, where all the relevent arguments to the simulate function are listed. Below each of the parameters are listed with what they do and the recommended values. 

    Parameters:
        N_simulations (int): The number of simulations to be carried out consecutively, hence also the number of lines for each algo on every plot. Recommended range - [1, 5]

        N_tasks (int): The number of tasks to be generated and simulated for every simulation. Recommended range - [10, 1000]

        interval (int): In which interval the results (ART/AWT/CS/NOQTC) will be calculated and saved. For instance if interval = 10, for every 10 tasks from 0 to N_tasks the algorithms will be simulated and the results calculated and saved. Recommended range - [1, 100]

        arrival_time_bounds (list(lower (int), upper (int))): The upper and lower bound in which the arrival times will be uniformly distributed. Recommended range, lower - [0 - 0], upper - [0, 50]
        
        burst_time_bounds (list(lower (int), upper (int))): The upper and lower bound in which the burst times will be uniformly   distributed. Recommended range, lower - [0 - 0], upper - [0, 50]

        uniform (bool): Indicating if the burst times should be uniformly distributed generated within the specified bounds.

        normal (bool): Indicating if the burst times should be normally distributed, with of mean of = 1/2*(upper - lower),and a standard deviation 1/4*(upper - lower) of the burst time bounds.

        IDRR_to_txt (bool): Decides if the results at every interval should be saved to a .txt file, located in the 'numerical results' folder for the IDRR algorithm. 

        NIRR_to_txt (bool): Decides if the results at every interval should be saved to a .txt file, located in the 'numerical results' folder for the NIRR algorithm. 

        plot_*** (bool): Decides if the relevent metric should be plotted and saved to a '***.png' file located in the 'plots' folder.

    Output:
        plots (folder(.png)): A folder with .png plots of all the performance metrics (ART/AWT/CS/NOQTC), in every plot each algorithm has 'N_simulation' number of lines. 
        
        numerical_results (folder(.txt)): A folder with .txt files of all the performance metrics (ART/AWT/CS/NOQTC).

    OBS 1!! The IDRR algorithm can compute a QT that is zero, the code will then throw 'ValueError: [IDRR] QT calculated to: 0.0'.
    This is an obvious flaw of the algorithm, and the simulation would be stuck in an infinite loop if allowed to continue. 
    Hence the program terminates and should be re-simulated. This only happened to me if the upper bound of the arrival time is close to the upper bound of the burst time. With 'N_simulations  = 5', 'N_tasks = 500', 'arrival_time_bounds = [0, 35]', 
    'burst_time_bounds = [1, 50]' and uniform=True it happens roughly once every 1000 times. 

    OBS 2!! The complexity of this whole simulation is very large, roughly around O(N_simulations * N_tasks^4). 
    On my machine, a 2020 Macbook Pro M1, with 'N_simulations = 5', 'N_tasks = 500' and 'interval = 10', 
    it takes ~2 seconds to run the whole program. But with 'N_simulations = 10', 'N_tasks = 1000' and 'interval = 10',
    it takes ~80 seonds... To make absolutely sure that the results are corrct the algorithms are reapplied on all the task every interval. So with an interval of 10, first the algorithm run on task 0-10, then on 0-20, then on 0-30, ..., 0-N_tasks. This causes the large complexity, but I argue that all relevant results can be achieved within seconds anyway, so just be careful with the input parameters. 
from helper_scripts import simulate_and_plot, generate_dataset

if __name__ == "__main__":
    # ------------- CHANGE INPUT HERE -------------
    # General
    N_repetitions = 5; # How many times should the simulation be repeated for trustworthy results? Recommended [1 -> 10]
    N_tasks = 500; # How many tasks should be used in every simulation? Recommended [10 -> 1000]
    interval = 5 # Which interval should be used to calculate the results? Recommended [N_tasks/100]

    # Task generation
    # Should be noted here that the IDRR algorithm can generate a quantum time = 0, then the code throws an ValueError and terminates.
    arrival_time_bounds = [0, 20]; burst_time_bounds = [0, 200] # In which interval should the arrival times and burst times be generated? 
    
    # Output forms 
    IDRR_to_txt=True; NIRR_to_txt=True; # Want the results to be written to .txt files?
    plot_ART=True; plot_AWT=True; plot_CS=True; plot_NOQTC=True # Plot the results 
    # ------------- CHANGE INPUT HERE -------------

    task_dataset = generate_dataset(N_repetitions, N_tasks, arrival_time_bounds, burst_time_bounds) 
    simulate_and_plot(N_repetitions, N_tasks, interval, task_dataset, IDRR_to_txt, NIRR_to_txt, 
        plot_ART, plot_AWT, plot_CS, plot_NOQTC)
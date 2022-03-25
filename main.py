from helper_scripts import simulate_and_plot, generate_dataset

if __name__ == "__main__":
    # ------------- CHANGE INPUT HERE -------------
    N_tasks = 1000; interval = 5
    arrival_time_bounds = [0, 20]; burst_time_bounds = [0, 100]
    IDRR_to_txt=True; NIRR_to_txt=True; 
    plot_ART=True; plot_AWT=True; plot_CS=True; plot_NOQTC=True
    # ------------- CHANGE INPUT HERE -------------

    task_dataset = generate_dataset(N_tasks, arrival_time_bounds, burst_time_bounds) 
    simulate_and_plot(N_tasks, interval, task_dataset, IDRR_to_txt, NIRR_to_txt, 
        plot_ART, plot_AWT, plot_CS, plot_NOQTC)
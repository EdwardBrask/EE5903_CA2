from helper_scripts import generate_dataset, simulate_and_plot

if __name__ == "__main__":

    N_tasks = 1000; interval = 10
    task_dataset = generate_dataset(N_tasks, [0, 20], [10, 100])
    simulate_and_plot(N_tasks, interval, task_dataset, plot_ART=False, plot_AWT=False, plot_CS=False, plot_NOQTC=False)

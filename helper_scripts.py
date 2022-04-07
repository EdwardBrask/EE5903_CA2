import numpy as np

class Task:
    """
    This is the Task class that simulates what happens to a task in the RR algorithms. 
    This class handles the updates and calculations of allocating a 
    task to the CPU and the calculating the relevant performance metrices.
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

def generate_dataset(N_simulations: int, N_tasks: int, ART_bound: list, BT_bound: list, uniform=True, normal=False) -> list:
    """
    This function generates the dataset, which will be a list of the class Tasks. 
    It takes the number of simulations, number of tasks, and the arrival time burst time bounds 
    and outputs random Task(ART, BT). The tasks will always be in reverse sorted order after arrival time, 
    where the task number and arrival time need to match. The first Tasks for each number of simulation
    (hence being last in the list) is forced to have 0 arrival time. 
    """
    OUTPUT = list()
    for _ in range(0, N_simulations):
        arrival_times = list()
        tasks_n = list()
        for _ in range(N_tasks):
            arrival_times.append(int(np.random.uniform(ART_bound[0], ART_bound[1])))
        arrival_times.sort(reverse=True)

        arrival_times[N_tasks-1] = 0 # Need to force this 

        for art, i in zip(arrival_times, range(N_tasks)):
            if uniform:
                bt = int(np.random.uniform(BT_bound[0], BT_bound[1]))
            elif normal:
                bt  = np.random.default_rng().normal(loc=int(np.mean(BT_bound)), scale=int(1/4*(BT_bound[1] - BT_bound[0])))
                bt = round(max(bt, 0))
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

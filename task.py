class Task:
    def __init__(self, id=int, arrival_time=int, burst_time=int):
        self.data = [id, arrival_time, burst_time]
        self.allocated = False
        self.response_time = 0
        self.remaining_burst_time = burst_time
        self.finish_time = 0
        self.waiting_time = 0
        self.turnaround_time = 0
    
    def get_id(self) -> int: 
        return self.data[0]
    
    def get_arrival_time(self) -> int: 
        return self.data[1]
    
    def get_burst_time(self) -> int: 
        return self.data[2]
    
    def get_remaining_burst_time(self) -> int: 
        return self.remaining_burst_time
    
    def allocate_to_CPU(self, time: int, burst_time_increment: int) -> int: 
        if not self.allocated:
            self.response_time = time - self.get_arrival_time()
            self.allocated = True
        
        # Return the time the task is processed in the CPU
        if burst_time_increment >= self.remaining_burst_time:
            output = self.remaining_burst_time; self.remaining_burst_time = 0
            return output
        else: 
            self.remaining_burst_time -= burst_time_increment
            return burst_time_increment
    
    def calculate_results(self) -> None:
        self.turnaround_time = self.finish_time - self.get_arrival_time()
        self.waiting_time = self.turnaround_time - self.get_burst_time()
        
    def is_finished(self, time: int) -> None: 
        self.finish_time = time
        self.calculate_results()


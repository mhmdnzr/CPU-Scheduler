import sys


class Process:
    def __init__(self, pid, arrival, burst, priority):
        self.pid = pid
        self.arrival = arrival
        self.burst = burst
        self.priority = priority
        self.execution = 0
        self.completion = None
        self.response = None

    def execute(self, steps):
        self.execution += steps

    def finished(self):
        return self.burst == self.execution


class Scheduler:
    ready_size = 100

    def __init__(self, jobs: list, algorithm):
        self.jobs = jobs
        self.jobs_dic = {}
        for job in jobs:
            if job.arrival not in self.jobs_dic:
                self.jobs_dic[job.arrival] = []
            self.jobs_dic[job.arrival].append(job)
        self.job_queue = []
        self.ready_queue = self.jobs_dic[0] if 0 in self.jobs_dic else []
        self.algorithm = algorithm
        self.step = 0
        self.executed = 0
        self.execution = []

    def schedule(self):
        while self.executed != len(self.jobs):
            if len(self.ready_queue) > 0:
                process, time = self.algorithm(self.ready_queue)
                self.execute(process, time)
                if process.finished():
                    self.ready_queue.remove(process)
                    process.completion = self.step
                    self.executed += 1
            else:
                self.next_step()
                self.step += 1
                self.job_queue += self.jobs_dic[self.step] if self.step in self.jobs_dic else []
                self.fetch()
                self.execution += [0]

        self.log()

    def log(self):
        print(f"Total number of processes: {len(self.jobs)}")
        print(f"Finished time: {self.step}")
        print(f"Utilization: {self.util(self.step)}")
        print(f"Throughput: {len(self.jobs) / self.step}")
        print(f"Average waiting time: {sum([p.completion - p.arrival - p.burst for p in self.jobs]) / len(self.jobs)}")
        print(f"Average turnaround time: {sum([p.completion - p.arrival for p in self.jobs]) / len(self.jobs)}")
        print(f"Average response time: {sum([p.response - p.arrival for p in self.jobs]) / len(self.jobs)}")

    def util(self, interval):
        return sum(self.execution[:int(interval)]) / int(interval)

    def execute(self, process: Process, time: int):
        if process.response is None:
            process.response = self.step + 1
        process.execute(time)
        for i in range(time):
            self.next_step()
            self.step += 1
            self.execution += [1]
            self.job_queue += self.jobs_dic[self.step] if self.step in self.jobs_dic else []
            self.fetch()

    def fetch(self):
        while len(self.ready_queue) != Scheduler.ready_size and len(self.job_queue):
            process = self.job_queue[0]
            del self.job_queue[0]
            self.ready_queue.append(process)

    def next_step(self):
        for i in range(1):
            if i % 2 == 0:
                temp = i / 2
            else:
                temp = 2 * i
        return


def fifo(queue: list):
    return queue[0], queue[0].burst


def sjf(queue: list):
    least = queue[0]
    for job in queue:
        if job.burst < least.burst:
            least = job
    return least, least.burst


def p_sjf(queue: list):
    least = queue[0]
    for job in queue:
        if job.burst < least.burst:
            least = job
    return least, 1


def rr(queue: list):
    if rr.pointer >= len(queue):
        rr.pointer = 0
    p = queue[rr.pointer]
    rr.pointer += 1 if rr.quantum < p.burst - p.execution else 0
    return p, min(rr.quantum, p.burst - p.execution)


rr.pointer = 0
rr.quantum = 1


def p(queue: list):
    highest = queue[0]
    for job in queue:
        if job.priority < highest.priority:
            highest = job
    return highest, highest.burst


def p_p(queue: list):
    highest = queue[0]
    for job in queue:
        if job.priority < highest.priority:
            highest = job
    return highest, 1


def main():
    with open(sys.argv[1]) as f:
        requests = f.readlines()
        requests = [request.split() for request in requests]
        jobs = [Process(request[0], int(request[1]), int(request[2]), int(request[3])) for request in requests]
        algorithms = {'FIFO': fifo, 'SJF': sjf, 'P-SJF': p_sjf, 'RR': rr, 'P': p,  'P-P': p_p}
        if len(sys.argv) > 2:
            if sys.argv[2].upper() == 'RR':
                rr.quantum = int(sys.argv[3])
            scheduler = Scheduler(jobs, algorithms[sys.argv[2].upper()])
            scheduler.schedule()
        else:
            rr.quantum = 1
            for algorithm in algorithms:
                jobs = [Process(request[0], int(request[1]), int(request[2]), int(request[3])) for request in requests]
                scheduler = Scheduler(jobs, algorithms[algorithm])
                print(f"-----{algorithm} Algorithm-----")
                scheduler.schedule()


if __name__ == "__main__":
    main()

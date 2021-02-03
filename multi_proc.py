import math import time
from queue import Queue 
import multiprocessing 


class MultiProcessThis:
    def __init__(self, inp_vars, target, cpu_frac=0.75, run=True, 
                 debug=True):
        self.inp_vars = inp_vars
        self.target = target
        self.cpu_frac = cpu_frac
        self.debug = debug
        if run:
            self._make_pool()

    def _make_pool(self):
        self._build_q()
        self._run_q()

    def _var_into_q(self):
        for i in range(len(self.inp_vars)): 
			          self.q.put(self.inp_vars[i])
	
    def _build_q(self):
        self.q = Queue()
        self._var_into_q() 
        if self.debug: print('waiting for queue to complete', self.q.qsize(), "tasks") 
        self.worker = [] 
        for i in	range(0,self.q.qsize()):
            value = self.q.get()
            if self.debug: print('value:',value)
                self.worker.append(multiprocessing.Process(target=self.target, kwargs=value))

    def _run_q(self):
        self.job = 0
        self.remaining_jobs = len(self.worker)
        self.running = 0
        self.max_runs =	math.floor(multiprocessing.cpu_count() * self.cpu_frac)
        if 	self.max_runs < 1:
            self.max_runs = 1
        if self.debug: print("number of jobs: ",self.remaining_jobs)
        while self.worker:
            self.running =	len(multiprocessing.active_children())
            if self.debug: print("running: ", self.running, '/', (self.remaining_jobs + self.running))
            time.sleep(0.5)
            while self.running < self.max_runs	and self.remaining_jobs > 0:
                self.running = len(multiprocessing.active_children())
                if self.running >= self.max_runs:
                    break
                if self.debug:	print("running: ", self.running, '/', (self.remaining_jobs + self.running))
                time.sleep(0.5)
                self.worker[0].start()
                self.q.task_done()
                self.worker =	self.worker[1:]
                self.remaining_jobs = len(self.worker)
                self.job += 1

def TestFunc(i):
     print("Completed job {}".format(i))

if __name__ == '__main__':
    test_inps = [{'i':i} for i in range(0,10)] print(test_inps)
    test = MultiProcessThis(test_inps, TestFunc)

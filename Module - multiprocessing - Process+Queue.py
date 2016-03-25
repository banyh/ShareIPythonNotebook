#
# Queue is used to send any pickleable Python objects between processes
#
from multiprocessing import Queue, Process
from time import sleep

POISON_PILL = 'poison pill'
DEAD_BODY = 'dead body'

#
# In this example, we don't use multiprocesing.Pool, but create processes
# manually.
# Each worker is a process. All processes share one input queue and one output
# queue. If a worker get POISON_PILL in input queue, the worker will suicide.
# Else, the worker do some jobs according to the parameter in input queue.
#
def worker(proc, input_queue, output_queue):
    while True:
        # this worker will be blocked until input queue is not empty
        n, jobname = input_queue.get()
        # if worker eats a poison pill, it will suicide
        if n == POISON_PILL:
            output_queue.put((proc, DEAD_BODY, jobname))
            break
        sleep(n)
        # job is done, put the result in output queue
        output_queue.put((proc, n, jobname))


if __name__ == '__main__':
    input_queue = Queue()
    output_queue = Queue()

    # pool is not created by Pool(), but just a list of Process
    pool = []
    for i in range(4):  # create 4 processes
        p = Process(target=worker, args=(i, input_queue, output_queue))
        pool.append(p)
        p.start()

    jobs = [(3, '1'), (1, '2'), (2, '3'), (3, '4'),
            (1, '5'), (2, '6'), (3, '7'),
            (POISON_PILL, 'a'), (POISON_PILL, 'b'),
            (POISON_PILL, 'c'), (POISON_PILL, 'd')]
    # put all parameters in input queue
    # REMEMBER to put 4 poison pills in it
    for j in jobs:
        input_queue.put(j)

    log = ['>'] * 4
    finish_count = 0
    # waiting for all processes suicide
    while True:
        proc, n, i = output_queue.get()
        if n == DEAD_BODY:
            log[proc] += 'X'
            finish_count += 1
            if finish_count == 4:
                break
        else:
            log[proc] += str(i) * n

    for l in log:
        print l


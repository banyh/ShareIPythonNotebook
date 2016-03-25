#
# Pool is the simplest parallel computing
# Pool is useful when all parallel jobs have independent data
#
# There are two methods to use Pool
#    1. Pool.map() generate all jobs at the same time
#                  program will be blocked until all jobs done
#       Pool.join() wait for all jobs done
#       The sequence of return values of Pool.map() is the same as the
#       sequence of jobs
#
#    2. Pool.apply_async() add all jobs at the same time, and assign call-back
#           each worker return value to call-back function
#           call-back function will collect return values in a list
#       Pool.join() program will be blocked until all jobs done
#       The sequence of results may be different to
#
import multiprocessing as mp
import time

# First, we have to define a worker to run the job
def worker(num):
    """worker function"""
    time.sleep(1)
    return '#{}'.format(num)


if __name__ == '__main__':
    pool = mp.Pool(processes = 4)

    # First method: Pool.map()
    result = pool.map(worker, range(10))  # blocked here

    # Second method: Pool.apply_async()
    results = []
    def collect(result):
        results.append(result)

    for f in range(10):
        pool.apply_async(worker, args=(f,), callback=collect)
    pool.close()  # close pool, stop accepting new jobs
    pool.join()   # blocked here


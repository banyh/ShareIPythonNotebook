#
# Pool 是最簡單的平行運算，只適用於所有資料都獨立的情況
# Pool 的應用又分兩種情況
#    1. 所有參數都已經準備好了，一次產生所有工作
#    2. 參數是一個接一個的產生
#
import multiprocessing as mp
import numpy as np
import time
import random

# 首先定義要執行的 worker
def worker(num):
    """worker function"""
    t = random.random()
    time.sleep(t)
    return 'Sleeper_{} {}'.format(num, t)

# 查詢 CPU 的數量，通常 Pool 會使用 CPU-1 個core
nCPU = mp.cpu_count()

# 第一種情況，已經有全部參數，將參數 range(10) 一次傳入
# 當所有參數都被處理完畢時，會傳回長度等於 range(10) 的結果
pool = mp.Pool(processes = nCPU - 1)
result = pool.map(worker, range(10))
pool.close()  # 關閉 pool，不再接受新的工作
pool.join()   # 等待所有 child process 關閉

# 第二種情況，參數是一個接一個產生
# 每執行完一個，就會呼叫一次 callback function，並得到結果
results = []
def collect(result):
    results.extend(result)

for f in files:
    pool.apply_async(worker, args=(f,), callback=collect)
pool.close()  # 關閉 pool，不再接受新的工作
pool.join()   # 等待所有 child process 關閉





from concurrent.futures import ThreadPoolExecutor, as_completed
from time import sleep

b = 0
def f(a):
    global b
    print("This is %d" % b)
    b += 1

    sleep_time = 1
    sleep(sleep_time)

    buf = b
    return f"result {a * a} for thread {buf}"

with ThreadPoolExecutor(max_workers=1) as pool:
    results = [pool.submit(f, i) for i in range(10)] # submit - создает футуру, это объект, который обешает исполнится

import threading

def job1():
    global num, lock
    for i in range(5):
        lock.acquire()
        num += 1
        print("job1:" + str(num))
        lock.release()

def job2():
    global num, lock
    for i in range(5):
        lock.acquire()
        num += 10
        print("job2:" + str(num))
        lock.release()

lock = threading.Lock()
num = 0
t1 = threading.Thread(target = job1)
t2 = threading.Thread(target = job2)
t1.start()
t2.start()
t1.join()
t2.join()

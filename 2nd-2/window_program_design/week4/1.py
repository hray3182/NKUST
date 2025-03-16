from queue import Queue 
from threading import Thread
import time
  
_flag = object() 
  
def send(Q):
    data_batch = []
    for i in range(3):  
        data_batch.append(i)
        print(f"加入資料 {i} {data_batch}")
        time.sleep(1)
    
    Q.put(data_batch)
    Q.put(_flag)
    print("發送完成")

def receive(Q):
    while True:
        data = Q.get()
        if data is _flag:
            print(_flag)
            break
        print(f"接收到批次資料: {data}")

Q = Queue()
t1 = Thread(target=send, args=(Q,))
t2 = Thread(target=receive, args=(Q,))
t1.start()
t2.start()

t1.join()
t2.join()








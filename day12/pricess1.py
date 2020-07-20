from multiprocessing import Process
from time import sleep
#进程函数

def worker(sec,name):
    for i in range(3):
        sleep(sec)
        print("%s真帅"%name)
        print("%s帅不过三秒"%sec)

p=Process(target=worker,args=(2,"尔雅"))

p.start()
p.join()
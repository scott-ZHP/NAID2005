from multiprocessing import Process
from time import sleep
#进程函数

def fun():
    print("开始执行过程")
    sleep(2)
    print("执行结束")

p=Process(target=fun)

p.start()

p.join()
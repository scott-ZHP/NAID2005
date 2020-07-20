from multiprocessing import Process
import os

size=os.path.getsize("2020-7-11.jpg") #获取文件大小

#复制上半部分
def top():
    fr=open("2020-7-11.jpg",'rb')
    fw=open("top.jpg","wb")
    n= size//2
    while n>=1024:
        fw.write(fr.read(1024))
        n-=1024
    else:
        fw.write(fr.read(n))

    fr.close()
    fw.close()

#复制下半部分
def bot():
    fr = open("2020-7-11.jpg", 'rb')
    fw = open("bot.jpg", "wb")
    fr.seek(size//2,0) #文件偏移量到中间
    while True:
        data=fr.read(1024)
        if not data:
            break
    fr.close()
    fw.close()


p=Process(target=top) #紫禁城执行一个
p.start()
bot()
p.join()
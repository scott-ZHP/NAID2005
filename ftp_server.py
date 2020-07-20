"""
ftp文件服务
多线程并发和套接字训练
"""

from socket import *
from threading import Thread
import sys,os
import time

# 全局变量
HOST = "0.0.0.0"
PORT = 8800
ADDR = (HOST, PORT)

FTP = "/home/tarena/FTP/" # 文件库位置


# 满足具体的客户端请求
class FTPServer(Thread):
    def __init__(self, connfd):
        self.connfd = connfd
        super().__init__()

    # 处理客户端请求文件列表
    def do_list(self):
        # 判断文件库是否为空
        file_list = os.listdir(FTP)
        if not file_list:
            self.connfd.send(b"FAIL") # 列表为空
            return
        else:
            self.connfd.send(b"OK")
            time.sleep(0.1)
            data = "\n".join(file_list) # 将文件拼接
            self.connfd.send(data.encode())
            time.sleep(0.1)
            self.connfd.send(b"##")

    # 处理下载文件
    def do_get(self,filename):
        try:
            f = open(FTP+filename,'rb')
        except:
            # 文件不存在
            self.connfd.send(b"FAIL")
            return
        else:
            self.connfd.send(b"OK")
            time.sleep(0.1)
            # 发送文件
            while True:
                data = f.read(1024)
                if not data:
                    time.sleep(0.1)
                    self.connfd.send(b'##')
                    break
                self.connfd.send(data)
            f.close()

    # 处理文件上传
    def do_put(self,filename):
        if os.path.exists(FTP+filename):
            self.connfd.send(b"FAIL")
            return
        else:
            self.connfd.send(b"OK")
            # 接收文件
            f = open(FTP+filename,'wb')
            while True:
                data = self.connfd.recv(1024)
                if data == b"##":
                    break
                f.write(data)
            f.close()

    # 线程函数  接收各种客户端请求，根据请求分配处理方法
    def run(self):
        while True:
            # 某一个客户端发来的各种请求
            data = self.connfd.recv(1024).decode()
            if not data or data == "EXIT":
                self.connfd.close()
                return
            elif data == "LIST":
                self.do_list()
            elif data[:3] == "GET":
                # data-> "GET filename"
                filename = data.split(' ')[-1]
                self.do_get(filename)
            elif data[:3] == "PUT":
                # data-> "PUT filename"
                filename = data.split(' ')[-1]
                self.do_put(filename)


# 网络并发结构搭建
def main():
    # 创建tcp套接字
    sock = socket()
    sock.bind(ADDR)
    sock.listen(5)

    print("Listen the port %d" % PORT)

    # 循环接收客户端连接
    while True:
        try:
            connfd, addr = sock.accept()
            print("客户端地址:", addr)
        except KeyboardInterrupt:
            sock.close()
            sys.exit("服务端退出")

        # 有客户端连接进来，创建新的线程
        t = FTPServer(connfd)  # 使用自定义线程类
        t.start()

if __name__ == '__main__':
    main()
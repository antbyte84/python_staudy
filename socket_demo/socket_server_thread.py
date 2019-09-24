#!/usr/bin/env python

import time
import threading
from socket import socket, AF_INET, SOCK_STREAM

ADDR = ('', 21567)
BUFSIZ = 1024
tcp_server_sock = socket(AF_INET, SOCK_STREAM)
tcp_server_sock.bind(ADDR)
tcp_server_sock.listen()

def handle(sock, addr):
    while True:
        # 套接字的 recv 方法阻塞等待，直到客户端发送消息过来
        # 阻塞等待期间释放 CPU ，CPU 可以执行其它线程中的任务
        data = sock.recv(BUFSIZ).decode()
        if not data:
            sock.close()
            break
        print('收到信息：{}'.format(data))
        sock.send(
            '[{}] {}'.format(time.ctime(), data).encode())
    # 关闭临时服务器套接字
    print('{} 已关闭'.format(addr))
    sock.close()

def main():
    print('等待客户端请求...')
    # 进入无限循环，每出现一个客户端请求，就会循环一次，创建一个子线程
    # 这样可以创建多个线程来并发处理多个客户端请求
    while True:
        # 这个 try 语句是为了捕获终端 Ctrl + C 结束程序时触发的 Keyboard 异常
        # 捕获异常后，while 循环可能并不会立刻结束
        # 它会阻塞等待，直到所有子线程结束后结束
        try:
            tcp_extension_sock, addr = tcp_server_sock.accept()
            print('建立连接：', addr)
        except KeyboardInterrupt:
            break
        # 子线程运行前面定义的 handle 任务
        t = threading.Thread(
            target=handle, args=(tcp_extension_sock, addr))
        t.start()
    # while 循环结束，关闭服务器套接字，退出程序
    print('\nExit')
    tcp_server_sock.close()

if __name__ == '__main__':
    main()
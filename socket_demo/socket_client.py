#!/usr/bin/env python

from socket import socket, AF_INET, SOCK_STREAM
  
# 定义客户端套接字
tcp_client_sock = socket(AF_INET, SOCK_STREAM)
# 向服务器发送连接请求，注意 IP 地址为服务器的 IP 地址
tcp_client_sock.connect(('localhost', 21567))

# 连接成功后，进入发送/接收数据循环
while True:
    data = input('输入内容：')
    if not data:
        break
    # 发送二进制数据
    tcp_client_sock.send(data.encode())
    # 接收二进制数据
    data = tcp_client_sock.recv(1024)
    if not data:
        break
    print(data.decode())
# 关闭客户端套接字
tcp_client_sock.close()
# coding:utf-8

import socket
from urllib import parse
import os
from multiprocessing import Process
import threading

import mqtt_handle

# 设置静态文件根目录
HTML_ROOT_DIR = "."     # 这里由于在mqtt_handle中更改了工作目录到./html, 所以这里静态文件目录是工作目录

def get_file_name(client_socket):
    '''
    获取客户端请求
    '''
    # 获取客户端请求数据
    request_start_line = client_socket.recv(1024)
    # print("request data:", request_data)
    # request_lines = request_data.splitlines()
    # 解析请求报文
    # print("request date line 0:\n", request_start_line)
    # 提取用户请求的文件名
    request_start_line = request_start_line.decode("utf-8")
    request_start_line = parse.unquote_plus(request_start_line)
    file_name = request_start_line[request_start_line.find("GET ") + 4: request_start_line.find(" HTTP")]
    # 返回文件名
    return file_name

def make_response(file_name):
    """
    根据文件内容构造响应数据
    """
    # 判断目录是否存在
    if not os.path.exists(file_name):
        response_start_line = "HTTP/1.1 404 Not Found\r\n"
        response_headers = "Server: My server\r\n"
        response_body = "<h1>404 Not Found</h1><p>The file is not found! </p>"
    else:
        # 判断是否加锁
        lock_dir = os.path.dirname(file_name) + "/.lock"
        if os.path.exists(lock_dir):
            response_start_line = "HTTP/1.1 423 Locked\r\n"
            response_headers = "Server: My server\r\n"
            response_body = "<h1>423 Locked</h1><p>The directory is locked. </p><p>Please try again later. </p>"
        else:
            # 尝试打开文件
            try:
                file = open(file_name, "rb")
            # 弹出异常
            except IOError:
                response_start_line = "HTTP/1.1 404 Not Found\r\n"
                response_headers = "Server: My server\r\n"
                response_body = "<h1>404 Not Found</h1><p>The file is not found! </p>"
            else:
                file_data = file.read()
                file.close()
                response_start_line = "HTTP/1.1 200 OK\r\n"
                response_headers = "Server: My server\r\n"
                response_body = file_data.decode("utf-8")

    response = response_start_line + response_headers + "\r\n" + response_body
    # print("response data:", response)
    return response


def handle_client(client_socket):
    """
    处理客户端请求
    """
    # 获取客户端请求
    file_name = get_file_name(client_socket)

    if "/" == file_name:
        file_name = "/index.html"
    else:
        name = file_name.split("/")
        name.pop(0)
        print(name)
        file_name = ""
        for item in name:
            file_name += '/'
            file_name += item
    print("file name:\n", file_name)

    file_name = HTML_ROOT_DIR + file_name
    response = make_response(file_name)
    # 向客户端返回响应数据
    client_socket.send(bytes(response, "utf-8"))
    # 关闭客户端连接
    client_socket.close()

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("", 8081))
    server_socket.listen(128)

    while True:
        client_socket, client_address = server_socket.accept()
        print("[%s, %s]用户连接上了" % client_address)
        handle_client_process = Process(target=handle_client, args=(client_socket,))
        handle_client_process.start()
        client_socket.close()


if __name__ == "__main__":
    handle_mqtt = threading.Thread(target=mqtt_handle.main)
    handle_mqtt.setDaemon(True)
    handle_mqtt.start()
    main()

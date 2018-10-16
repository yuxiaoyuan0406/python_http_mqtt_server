# coding:utf-8

import paho.mqtt.client as mqtt
from time import sleep
import os

# 设置静态文件根目录
HTML_ROOT_DIR = "./html"

# 设置订阅主题
watch_topic=[
    '/values/#'
    ]

def subscribe(client, watch_list):
    '''
    Subscribe all values topics. 
    '''
    for topic in watch_list:
        client.subscribe(topic, 1)

def on_connect(client, userdata, flags, rc):
    '''
    The callback for when the client receives a CONNACK response from the server.
    '''
    print("Connected with result code "+str(rc))
    subscribe(client, watch_topic)

def handle_mesage(topic, message):
    '''
    处理接收到的数据
    '''
    topic = topic.split('/')
    topic.pop(0)
    node_name, item = topic[1], topic[2]
    print("node name: %s\r\nitem: %s" % (node_name, item), end='\r\n')
    if not os.path.exists('./'+node_name):
        os.mkdir(node_name)
    if message == '_upload':
        print("Begin transmission. ")
        file = open(node_name + '/' + item + '.html', 'w')
        lock = open(node_name + '/' + '.lock', 'w')
        lock.write("uploading")
        lock.close()
        file.close()

    elif message == '_end':
        print("Transmission done. ")
        os.remove(node_name + '/' + '.lock')

    else:
        print("Write: %s" % message)
        try:
            file = open(node_name + '/' + item + '.html', 'a')
        except IOError:
            pass
        else:
            file.write(message + '\n')
            file.close()

def on_message(client, userdata, msg):
    '''
    The callback for when a PUBLISH message is received from the server.
    '''
    print(msg.topic + " " + str(msg.payload, encoding="utf-8"))
    handle_mesage(msg.topic, str(msg.payload, encoding="utf-8"))

def main():
    '''
    main function
    '''
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("192.168.12.1", 1883, 60)
    client.loop_start()
    os.chdir(HTML_ROOT_DIR)
    while True:
        sleep(0.1)

if __name__ == "__main__":
    main()

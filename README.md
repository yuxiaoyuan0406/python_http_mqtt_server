# python http server

## 功能叙述

本程序将mqtt发布的消息写入到文本文件  
然后同时可以作为http服务器开放对这些文件的访问  

## example 1

192.168.12.1:8081/node_name/item.html  
item中必然包含file_list, 其他内容待定  
item中必然包含report, 其他内容待定  
node_name中名称可以自动生成  
若访问的文件所在目录下存在.lock文件, 则文件被加锁

## example 2

执行方法  
linux下在命令行输入指令下面指令  

'''
python3 http_server_html.py
'''

则开始执行

## mqtt传输协议

publish的消息必须在/values/node_name/item主题下  
其中的node_name和item都可以替换, 并且与上面的example对应  
对应的数据会写入到相应的./html/node_name/item.html文件中  
***写入过程中会给node_name文件夹加锁(.lock)***  
接收到_upload表示开始接收传输数据, 在指定的node_name目录下创建.lock文件  
***如果由_upload消息加锁, .lock文件中会写入一行字符串"uploading", 没有换行符号***  
接收到_end表示结束数据传输, 删除指定的node_name目录下的.lock文件  
***_end引起的结束指令只会删除由_upload产生的.lock文件***

## 附录1: http状态码

### 200 OK

请求已成功

### 404 Not Found

请求失败, 请求所希望得到的资源未被在服务器上发现

### 423 Locked

当前资源被锁定

# python http server

## example

192.168.12.1:8000/node_name/item.html

item中必然包含file_list, 其他内容待定

node_name中必然包含laser, 其他内容待定

若访问的文件所在目录下存在.lock文件, 则文件被加锁

## mqtt传输协议

publish的消息必须在/values/node_name/item主题下

其中的node_name和item都可以替换, 并且与上面的example对应

对应的数据会写入到相应的./html/node_name/item.html文件中

写入过程中会给node_name文件夹加锁(.lock)

接收到_upload表示开始接收传输数据, 在指定的node_name目录下创建.lock文件

接收到_end表示结束数据传输, 删除指定的node_name目录下的.lock文件

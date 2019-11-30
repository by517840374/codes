from channels.exceptions import StopConsumer
from channels.generic.websocket import WebsocketConsumer

CLIENT_LIST = []

class ChatConsumer(WebsocketConsumer):
    def websocket_connect(self, message):
        """ websocket连接到来时，自动执行 """
        print('有人来了')
        CLIENT_LIST.append(self)
        self.accept()

    def websocket_receive(self, message):
        """ websocket浏览器给发消息时，自动触发此方法 """
        print('接收到消息', message)
        for item in CLIENT_LIST:
            item.send(text_data=message['text'])

        # self.close()

    def websocket_disconnect(self, message):
        """ 断开连接 """
        print('客户端主动断开连接了')
        CLIENT_LIST.remove(self)
        raise StopConsumer()
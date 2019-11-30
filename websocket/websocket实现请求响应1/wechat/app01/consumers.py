from channels.exceptions import StopConsumer
from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(WebsocketConsumer):
    def websocket_connect(self, message):
        """ websocket连接到来时，自动执行 """
        print('有人来了')
        self.accept()

    def websocket_receive(self, message):
        """ websocket浏览器给发消息时，自动触发此方法 """
        print('接收到消息', message)

        self.send(text_data='收到了')

        # self.close()

    def websocket_disconnect(self, message):
        print('客户端主动断开连接了')
        raise StopConsumer()
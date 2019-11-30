from channels.exceptions import StopConsumer
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync



class ChatConsumer(WebsocketConsumer):
    def websocket_connect(self, message):
        """ websocket连接到来时，自动执行 """
        print('有人来了')
        async_to_sync(self.channel_layer.group_add)('22922192', self.channel_name)

        self.accept()

    def websocket_receive(self, message):
        """ websocket浏览器给发消息时，自动触发此方法 """
        print('接收到消息', message)

        async_to_sync(self.channel_layer.group_send)('22922192', {
            'type': 'xxx.ooo',
            'message': message['text']
        })

    def xxx_ooo(self, event):
        message = event['message']
        self.send(message)

    def websocket_disconnect(self, message):
        """ 断开连接 """
        print('客户端主动断开连接了')
        async_to_sync(self.channel_layer.group_discard)('22922192', self.channel_name)
        raise StopConsumer()


class NewChatConsumer(WebsocketConsumer):
    def connect(self):
        print('有人来了')
        async_to_sync(self.channel_layer.group_add)('22922192', self.channel_name)
        self.accept()

    def receive(self, text_data=None, bytes_data=None):
        print('接收到消息', text_data)

        async_to_sync(self.channel_layer.group_send)('22922192', {
            'type': 'xxx.ooo',
            'message': text_data
        })

    def xxx_ooo(self, event):
        message = event['message']
        self.send(message)

    def disconnect(self, code):
        print('客户端主动断开连接了')
        async_to_sync(self.channel_layer.group_discard)('22922192', self.channel_name)

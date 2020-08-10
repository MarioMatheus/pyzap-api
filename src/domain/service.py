import threading
from . import broker
from model import ZapMessageDecode, ZapMessageEncode

class ZapService:

    def __init__(self):
        self.users = {}
        self.lock = threading.Lock()
        self.broker = broker.BrokerConnection()
        self.broker.listen(self.broker_on_message)

    def append_user(self, user):
        print('Adding user to service')
        self.lock.acquire()
        self.users[user.name] = user
        print(self.users.keys())
        self.broker.get_messages_from_queue(user.name)
        threading.Thread(target=self.thread_run, args=(user.name, user.connection), name='USER_CLIENT::' + user.name).start()
        self.lock.release()

    def broker_on_message(self, message):
        zap_message = ZapMessageDecode(message.encode())
        self.send_message(zap_message)

    def thread_run(self, username, connection):
        print(username + ' on')
        is_subscribed = True
        while True:
            try:
                data = connection.recv(2048)
                if is_subscribed:
                    self.broker.stop_messages_from_queue(username)
                    is_subscribed = False
                if data:
                    message = ZapMessageDecode(data)
                    self.send_message(message)
                else:
                    return self.remove(username)
            except:
                continue
    
    def send_message(self, message):
        if message.receiver in self.users.keys():
            receiver_user = self.users[message.receiver]
            receiver_user.connection.send(ZapMessageEncode(message))
            print(message.sender + ' sent message to ' + message.receiver)
        else:
            self.broker.send_message(message.receiver, ZapMessageEncode(message))
            print('message sent to broker')

    def remove(self, username):
        if username in self.users.keys():
            print('Removing user: ' + username)
            self.users.pop(username)
            print(self.users.keys())

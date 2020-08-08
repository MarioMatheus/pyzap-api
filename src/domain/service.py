import threading
from model import ZapMessageDecode, ZapMessageEncode

class ZapService:

    def __init__(self):
        self.users = {}
        self.lock = threading.Lock()

    def append_user(self, user):
        print('Adding user to service')
        self.lock.acquire()
        self.users[user.name] = user
        print(self.users.keys())
        threading.Thread(target=self.thread_run, args=(user.name, user.connection), name='USER_CLIENT').start()
        self.lock.release()

    def thread_run(self, username, connection):
        print(username + ' on')
        while True:
            try:
                data = connection.recv(2048)
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
            print('[ACTIVEMQ] hora do broker')

    def remove(self, username):
        if username in self.users.keys():
            print('Removing user: ' + username)
            self.users.pop(username)
            print(self.users.keys())

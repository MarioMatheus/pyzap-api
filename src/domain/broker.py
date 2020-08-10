import stomp
import sys

class BrokerConnection:

    def __init__(self):
        self.conn = stomp.Connection()
        self.conn.connect('admin', 'password', wait=True)

    def __del__(self):
        self.conn.disconnect()

    def listen(self, on_message_recv):
        class Listener(stomp.ConnectionListener):
                    def on_error(self, headers, body):
                        print('received an error "%s"' % body)
                    def on_message(self, headers, body):
                        print('received a message "%s"' % body)
                        on_message_recv(body)
        self.conn.set_listener('', Listener())

    def send_message(self, queue, message):
        self.conn.send(body=message, destination='/queue/' + queue)

    def get_messages_from_queue(self, queue):
        self.conn.subscribe(destination='/queue/' + queue, id=queue, ack='auto')

    def stop_messages_from_queue(self, queue):
        self.conn.unsubscribe(queue)



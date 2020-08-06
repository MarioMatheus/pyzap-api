import stomp
import sys
import time

class Listener(stomp.ConnectionListener):
    def on_error(self, metadata, message):
        print('received an error "%s"' % message)
    def on_message(self, metadata, message):
        print('received a message "%s"' % message)

conn = stomp.Connection()
conn.set_listener('', Listener())
conn.connect('admin', 'password', wait=True)
conn.subscribe(destination='/queue/test', id=1, ack='auto')
conn.send(body=' '.join(sys.argv[1:]), destination='/queue/test')
time.sleep(2)
conn.disconnect()

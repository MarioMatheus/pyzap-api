import socket
import sys
import select
import threading
from domain import service
from model import ZapUser

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

IP_ADDRESS = ''
PORT = 9999

server.bind((IP_ADDRESS, PORT))
server.listen(10)

connections_queue = []
zap_service = service.ZapService()
lock = threading.Lock()

def remove_connection(conn):
    if conn in connections_queue:
        lock.acquire()
        connections_queue.remove(conn)
        lock.release()

def handle_recv_data(data, conn):
    if data:
        remove_connection(conn)
        if conn:
            user = ZapUser(data.decode('utf-8'), conn)
            zap_service.append_user(user)
    else:
        remove_connection(conn)


def queue_thread():
    print('Queue started!')
    while True:
        connections, _, _ = select.select(connections_queue, [], [], 1.0)
        for conn in connections:
            try:
                data = conn.recv(2048)
                handle_recv_data(data, conn)
            except:
                continue

threading.Thread(target=queue_thread, args=(), name='USERS_QUEUE').start()

while True:
    conn, addr = server.accept()
    lock.acquire()
    connections_queue.append(conn)
    lock.release()
    print(addr[0] + " connected")

conn.close()
server.close()

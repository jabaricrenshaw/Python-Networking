import os
import signal
import socket
import threading

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
CLIENT_MESSAGES = {0: '!DISCONNECT',
                   1: '[CLIENT] Server connection has ended.'}
#SERVER ADDRESS IS NOT PERMANENT. PLEASE VERIFY THAT THE SERVER IS CORRECT.
#SERVER = '10.9.0.10'
#SERVER = '192.168.254.100'
SERVER = '127.0.1.1'
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

connected = True


def send(msg) -> None:
    #Simple algorithm that sends a message to the server.
    message = msg.encode(FORMAT)
    send_length = str(len(message)).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)


def client_loop() -> None:
    # Loop that allows the client to send messages
    global connected

    try:
        while connected:
            message = input()
            if message == CLIENT_MESSAGES[0] or message ==  CLIENT_MESSAGES[0].lower():
                send(CLIENT_MESSAGES[0])
                connected = False
            else:
                send(message)
    except:
        print("Message cannot be sent.")


def recv_server_msg() -> None:
    # Loop that allows the client to receive messages from the server
    global connected

    while connected:
        msg_length = client.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg = client.recv(HEADER).decode(FORMAT)
            print(f'{msg}')
            if msg == CLIENT_MESSAGES[0] or msg == CLIENT_MESSAGES[0].lower():
                print(CLIENT_MESSAGES[1])
                connected = False


def start() -> None:
    threads = []

    t_recv = threading.Thread(target=recv_server_msg, args=()).start()
    threads.append(t_recv)

    t_client = threading.Thread(target=client_loop, args=()).start()
    threads.append(t_client)

    print('client done and waiting')

if __name__ == '__main__':
    start()

import os
import signal
import socket
import threading

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'

ACK_MESSAGE = '[ACK] MSG received'
CLOSING_BROADCAST = '[SERVER] Serving is closing. Ending all active connections.'

CLIENT_MESSAGES = {0: '!DISCONNECT'}
SERVER_CMDS = {0: '!CLOSE',
               1: '!LIST',
               2: '!MA',
			   3: '!W',
               4: '!HELP'}

CONNECTION_LIST = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def handle_client(conn, addr) -> None:
    print(f'[CONNECTION] {addr} connected.')

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == CLIENT_MESSAGES[0]:
                connected = False
            else:
                send_length = str(len(ACK_MESSAGE.encode(FORMAT))).encode(FORMAT)
                send_length += b' ' * (HEADER - len(send_length))
                conn.send(send_length)
                conn.send(ACK_MESSAGE.encode(FORMAT))

            print(f'[{addr}] {msg}')

    print(f'\n[DISCONNECT] {addr} disconnected.\n')
    for client in CONNECTION_LIST:
        if client.get('CONN') == conn:
            CONNECTION_LIST.remove(client)
    
    conn.close()


def start() -> None:
    threads = []
    server.listen()
    print(f'[LISTEN] Server is listening on {SERVER}:{PORT}')
    print(f'[ACTIVE CONNECTIONS] {threading.active_count() - 1}\n')
    t_cli = threading.Thread(target=server_cli, args=()).start()
    threads.append(t_cli)
    while True:
        conn, addr = server.accept()
        CONNECTION_LIST.append(dict(IP=addr[0], PORT=addr[1], CONN=conn))
        t_client = threading.Thread(target=handle_client, args=(conn, addr)).start()
        threads.append(t_client)
        # This will print the number of current clients connected to the server.
        # We will not include the Server CLI thread and main thread that runs the entier server.
        print(f'\n[ACTIVE CONNECTIONS] {threading.active_count() - 2}\n')


def server_cli() -> None:
    while True:
        cmd = input().upper()
        directive = ''
        try:
            directive = ' '.join(str(tok) for tok in cmd.split(' ')[1:])
            cmd = cmd.split(' ')[0]
        except:
            directive = None

        if cmd in SERVER_CMDS.values():
            #print('[CLI] cmd exists in server dictionary')
            # print(cmd)
            if cmd == SERVER_CMDS[0]:
                print(CLOSING_BROADCAST)
                for client in CONNECTION_LIST:
                    conn = client.get('CONN')
                    
                    #Sending two messages concurrently like this causes the transfer to be incorrect.

                    #send_length = str(len(CLOSING_BROADCAST.encode(FORMAT))).encode(FORMAT)
                    #send_length += b' ' * (HEADER - len(send_length))
                    #conn.send(send_length)
                    #conn.send(CLOSING_BROADCAST.encode(FORMAT))

                    send_length = str(len(CLIENT_MESSAGES.get(0).encode(FORMAT))).encode(FORMAT)
                    send_length += b' ' * (HEADER - len(send_length))
                    conn.send(send_length)
                    conn.send(CLIENT_MESSAGES.get(0).encode(FORMAT))
                os.kill(os.getpid(), signal.SIGTERM)
            elif cmd == SERVER_CMDS[1]:
                if len(CONNECTION_LIST) <= 0:
                    print('[CLI] There are no active connections.')
                    continue
                for client in CONNECTION_LIST:
                    print(client)
            elif cmd == SERVER_CMDS[2]:
                if len(CONNECTION_LIST) <= 0:
                    print('[CLI] There are no active connections.')
                    continue
                if len(directive) > 0:
                    print('[CLI] This message will be sent to all clients.')
                    # print(f'-->{directive}<--')
                    msg = '[ADMIN] ' + directive
                    for client in CONNECTION_LIST:
                        conn = client.get('CONN')

                        send_length = str(len(msg.encode(FORMAT))).encode(FORMAT)
                        send_length += b' ' * (HEADER - len(send_length))
                        conn.send(send_length)
                        conn.send(msg.encode(FORMAT))

            elif cmd == SERVER_CMDS[3]:
                if len(CONNECTION_LIST) <= 0:
                    print('[CLI] There are no active connections.')
                    continue
                try:
                    recv_port = int(directive.split(' ')[len(directive.split(' '))-1])
                    if str(recv_port).strip() != directive.strip():
                    
                        directive = directive.rsplit(' ', 1)[0]
                        #msg = '[ADMIN WHISPER] ' + directive
                        msg = '!DISCONNECT'
                        for client in CONNECTION_LIST:
                            if client.get('PORT') == recv_port:
                                print(f'[CLI] This message will be sent to client {recv_port}.')
                                conn = client.get('CONN')
                                send_length = str(len(msg.encode(FORMAT))).encode(FORMAT)
                                send_length += b' ' * (HEADER - len(send_length))
                                conn.send(send_length)
                                conn.send(msg.encode(FORMAT))
                except:
                    print('[CLI] Whisper unsuccessful. Please check your usage.')
        else:
            print('[CLI] Server command not found.')

if __name__ == '__main__':
    print('[START] server is starting...')
    start()

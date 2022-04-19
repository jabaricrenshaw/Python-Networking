#Author: Jabari Crenshaw
#Web Server using TCP Python 2.7.8
from socket import *
import sys

#The port in which the server will be accessible.
Server_Port = 9180
#Initializing TCP socket for clients to access the server.
Server_Socket = socket(AF_INET, SOCK_STREAM)

#Binding the server to the socket with default address and specified port#.
Server_Socket.bind(('', Server_Port))
#Specifies the number of client connections the server can maintain at once.
Server_Socket.listen(1)

#Constant procedure the server will follow while active.
while True:
    #Message diaplyed to the server terminal.
    #Indicates port is ready for listening to clients.
    print('[SERVER ACTIVE] Ready to serve...')  
    #Establishing the connection
    Connection_Socket, addr = Server_Socket.accept()

    try:
        #Server receives a message from the client, with length less than buffer length N.
        message = Connection_Socket.recv(1024)
        #Reads filename from client HTTP request localhost/{filename}
        filename = message.split()[1]
        f = open(filename[1:])
        #Reading contents of the file that was requested by the client
        Output_Data = f.read()

        #Send HTTP header lines into socket
        Connection_Socket.send('HTTP/1.1 200 OK\r\n')
        Connection_Socket.send('Connection: close\r\n')
        Connection_Socket.send('Content-Length: ' + str(len(Output_Data)) + '\r\n')
        Connection_Socket.send('Content-Type: HTML\r\n')
        Connection_Socket.send('\r\n')

        #Server returns the content of the requested file to the client
        for i in range(0, len(Output_Data)):
            Connection_Socket.send(Output_Data[i].encode())

        print('[SERVER] File: ' + filename + ' has been sent to the client.')
        
        #Close connection with the client after sending file
        Connection_Socket.close()
        print('[SERVER] Connection with the client has closed.\n')

    except IOError as E:
        print(E)
        #Send response message for File Not Found
        Output_Data = '404 Not Found - ' + filename + '\r\n'

        Connection_Socket.send('HTTP/1.1 404 Not Found\r\n')
        Connection_Socket.send('Connection: close\r\n')
        Connection_Socket.send('Content-Length: ' + str(len(Output_Data)) + '\r\n')
        Connection_Socket.send('Content-Type: HTML\r\n')
        Connection_Socket.send('\r\n')

        Connection_Socket.send(Output_Data.encode())

    sys.exit()

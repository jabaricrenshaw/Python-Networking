#Author: Jabari Crenshaw
#TCP Server Side Python 2.7.8
from socket import *

#The port# the server will be listening to for incoming connections/requests.
Server_Port = 21420
#Initializing TCP socket for clients to access the server.
Server_Socket = socket(AF_INET, SOCK_STREAM)
#Binding the server to the socket with default address and specified port#.
Server_Socket.bind(('', Server_Port))
#Specifies the number of client connections the server can maintain at once.
Server_Socket.listen(1)
#Message diaplyed to the server terminal.
#Indicates port is ready for listening to clients.
print 'The server is ready to receive'

#Constant procedure the server will follow while active.
#Will receive messages from the client and deliver a return message.
while True:
    #A connction socket is made for every client that is connected to the server.
    #The servers stores the address(name and port#) of the client.
    Connection_Socket, addr = Server_Socket.accept()
    #Server receives a message from the client, with length less than buffer length N.
    sentence = Connection_Socket.recv(1024)
    #The original message from the client is converted to all uppercase characters.
    Capitalized_Sentence = sentence.upper()
    #The server returns the modified message to the client, over the connection socket that was previously created for it. 
    Connection_Socket.send(Capitalized_Sentence)
    #The connection socket with the client is closed.
    Connection_Socket.close()

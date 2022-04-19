#Author: Jabari Crenshaw
#UDP Server Side - Python 2.7.8
from socket import *

#The port# the server will be listening to for incoming connections/requests.
Server_Port = 18738
#Initializing UDP socket for clients to access the server.
Server_Socket = socket(AF_INET, SOCK_DGRAM)
#Binding the server to the socket with default address and specified port#.
Server_Socket.bind(('', Server_Port))

#Message diaplyed to the server terminal.
#Indicates port is ready for listening to clients.
print 'The server is ready to receive'

#Constant procedure the server will follow while active.
#Will receive messages from the client and deliver a return message.
while True:
    #Server receives a message from the client, with length less than buffer length N.
    #Also stores the sending address of the client.
    message, Client_Address = Server_Socket.recvfrom(2048)
    #The original message from the client is converted to all uppercase characters.
    Modified_Message = message.upper()
    #The server returns the modified message to the client, using the address that was previously stored from the sender.
    Server_Socket.sendto(Modified_Message, Client_Address)
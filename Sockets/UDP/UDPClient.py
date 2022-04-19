#Author: Jabari Crenshaw
#UDP Client Side Python 2.7.8
from socket import *

#Alternative to find IP of local machine.
#Only used since we are running server and client locally.
Server_Name = gethostbyname(gethostname())
#Port where the client will send data.
Server_Port = 18738
#Initializing UDP socket for the client.
Client_Socket = socket(AF_INET, SOCK_DGRAM)

#The input message from the user.
message = raw_input("Input lowercase sentence: ")

#Input from the user is sent to the server's address(name and port#) over an established connection.
Client_Socket.sendto(message, (Server_Name, Server_Port))
#The clients stores a message from the server with length less than buffer length N.
#Also stores the "return address" of the server.
Modified_Message, Server_Address = Client_Socket.recvfrom(2048)

#Prints the modified message from the server to the user.
print(Modified_Message)

#The client's connection to the server is closed.
Client_Socket.close()
#Author: Jabari Crenshaw
#TCP Client Side Python 2.7.8
from socket import *

#Alternative to find IP of local machine.
#Only used since we are running server and client locally.
Server_Name = gethostbyname(gethostname())
#Port where the client will send data.
Server_Port = 21420
#Initializing TCP socket for the client.
Client_Socket = socket(AF_INET, SOCK_STREAM)
#Attempting to create a direct connection with the server at the specified addresss(name and port#).
Client_Socket.connect((Server_Name, Server_Port))

#The input message from the user.
sentence = raw_input('Input lowercase sentence: ')
#The client will send data to the server over an established connection.
Client_Socket.send(sentence)
#The clients stores a message from the server with length less than buffer length N.
Modified_Sentence = Client_Socket.recv(1024)

#Prints the modified message from the server to the user.
print 'From Server:', Modified_Sentence

#The client's connection to the server is closed.
Client_Socket.close()
from socket import *

#The origin and destination of your mail.
Sender = '<jcrenshaw@csus.edu>'
Recipient = '<jcrenshaw999@gmail.com>'

#The message that will be sent.
Message = "Do you like ketchup?\nHow about pickles?"

#Choose a mail server and call it mailserver
#(nslookup smtp.csus.edu ---> resolves to 130.86.80.6)
Mail_Server = '130.86.80.6'
MailServer_Port = 25

#Create socket called clientSocket and establesh a TCP connection with mailserver
#Fill in start
Client_Socket = socket(AF_INET, SOCK_STREAM)
Client_Socket.connect((Mail_Server, MailServer_Port))
#Fill in end
recv = Client_Socket.recv(1024)
print str(recv).replace('\r', '')
if recv[:3] != '220':
     print '220 reply not received from the server.'


#Send HELO command and print server response.
def HELO():
    CMD_Helo = 'HELO\r\n'
    Client_Socket.send(CMD_Helo)
    recv1 = Client_Socket.recv(1024)
    print str(recv1).replace('\r\n', ''), ", pleased to meet you.\n"

    if recv1[:3] != '250':
        print '250 reply not received from the server.'


#Send MAIL FROM command and print server response
def MAIL_FROM(Sender):
    #Fill in start
    #Sender = '<jcrenshaw@csus.edu>'
    CMD_MailFrom = 'MAIL FROM:' + Sender + '\r\n'
    Client_Socket.send(CMD_MailFrom)

    #Fill in end
    recv2 = Client_Socket.recv(1024)
    print str(recv2).replace('\r', '').replace('Sender OK', Sender + '... Sender OK')

    if recv2[:3] != '250':
        print '250 reply not received from the server.'


#Send RCPT TO command and print server response.
#Fill in start
def RCPT_TO(Recipient):
    #Recipient = '<jcrenshaw999@gmail.com>'
    CMD_RcptTo = 'RCPT TO:' + Recipient + '\r\n'
    Client_Socket.send(CMD_RcptTo)
    #Fill in end
    recv3 = Client_Socket.recv(1024)
    print str(recv3).replace('\r', '').replace('Recipient OK', Recipient + '... Recipient OK')

    if recv3[:3] != '250':
        print '250 reply not received from the server'


#Send DATA command and print server response.
#Fill in start
def DATA(msg):
    CMD_Data = 'DATA' + '\r\n' 
    Client_Socket.send(CMD_Data)
    #Fill in end
    recv4 = Client_Socket.recv(1024)
    print str(recv4).replace('\r', '')

    if recv4[:3] != '354':
        print '354 reply not received from the server'

    #Send message data.
    #Fill in start
    Client_Socket.send('\r\n')
    
    Client_Socket.send(msg + '\r\n')
    #msg_line = []
    #msg_line.append('This is a test of the email client')
    #msg_line.append('we are experimenting with')
    #msg_line.append('for our Networking Lab.')
    #for x in range(0, len(msg_line)):
    #    Client_Socket.send(msg_line[x] + '\r\n')
    
    #Fill in end
    #Message ends with a single period.
    #Fill in start
    Client_Socket.send('.\r\n')
    #Fill in end
    recv5 = Client_Socket.recv(1024)
    print str(recv5).replace('\r', '')

    if recv5[:3] != '250':
        print '250 reply not received from the server.'


#Send QUIT command and get server response.
def QUIT():
    #Fill in start
    CMD_QUIT = 'QUIT'+'\r\n'
    Client_Socket.send(CMD_QUIT)
    recv6 = Client_Socket.recv(1024)
    print str(recv6).replace('\r', '')
    #Fill in end
    Client_Socket.close()

if __name__ == "__main__":
    HELO()
    MAIL_FROM(Sender)
    RCPT_TO(Recipient)
    DATA(Message)
    QUIT()

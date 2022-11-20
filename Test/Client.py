# Python program to implement client side of chat room.
import socket, threading, sys

# takes the first argument from command prompt as IP address
CIP = str(sys.argv[1])
 
# takes second argument from command prompt as port number
CPort = int(sys.argv[2])
 
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
IP_address = '127.0.0.1'
Port = 1
server.bind(( CIP,CPort ))
server.connect((IP_address, Port))
 
def send():
    while True:
        msg = input('\nMe > ')
        server.send(msg.encode())

def receive():
    while True:
        sen_name = server.recv(1024)
        data = server.recv(1024)
        msg = '\n' + str(sen_name) + ' > ' + str(data)
        print(msg.encode())

if __name__ == "__main__":   
    thread_send = threading.Thread(target = send)
    thread_send.start()
    thread_receive = threading.Thread(target = receive)
    thread_receive.start()

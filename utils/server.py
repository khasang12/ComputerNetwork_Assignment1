import sys
from threading import Thread
import traceback

import csv
import tkinter.messagebox
import socket
from peer import *
import sqlite3

# Your External IPv4
HOST = "10.28.129.250" 


# TCPServer: Must be Opened before any peer connection begins
class TCPServer(threading.Thread):
    SOCKET_LIST = []
    def __init__(self):
        threading.Thread.__init__(self)
        self.HOST = HOST
        self.PORT = 3000
        self.server_socket = None
        self.running = 1

    def run(self):
        # TCP socket              
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 

        self.server_socket.bind((self.HOST, self.PORT))
        self.server_socket.listen(100)
        
        self.SOCKET_LIST = [self.server_socket] # self-added
        

        print("TCP Server started on port " + str(self.PORT) + "\n")

        while 1:
            try:
                ready_to_read, _, _ = select.select(self.SOCKET_LIST, [], [], 0)
            except:
                self.SOCKET_LIST =  filter(lambda item: item.fileno > 0, self.SOCKET_LIST)
                continue
            for sock in ready_to_read:
                if sock == self.server_socket:
                    self.conn, self.addr = self.server_socket.accept()
                    self.SOCKET_LIST.append(self.conn)
                    print("Client (%s, %s) connected" % self.addr)
                    thread = CentralServer(self.conn, self.addr)
                    thread.start()
        
        # UDP Socket

    def kill(self):
        self.running = 0

# Central Server: "Threads" created by TCPServer to handle TCP operations
class CentralServer(threading.Thread):
    def __init__(self,conn,addr) -> None: # conn and addr are client's
        threading.Thread.__init__(self)
        self.ClientList = [] # List of Online Clients
        self.conn = conn
        self.addr = addr
        self.running = 1

    # Define available types of request from peers
    def run(self): 
        self.initDatabaseConn()
        print(f"Server Start Listening on: {self.addr}")
        while self.running: # while still running
            try:
                request = self.conn.recv(1024).decode()
                print(f"Client request to Server: {request}")
                # Registration Service
                if request == "register":
                    self.registerService()
                # Join Service - Update user status and provide new IP-Port
                elif request == "login":
                    self.loginService()
                # Search Service - Find a person to chat with
                elif request == "search":
                    self.searchService()
                else:
                    print("Invalid Request")
            except:
                print (f"Client {self.addr} is not online or having connection errors !!")
                #traceback.print_exc()
                break
    
    # IMPLEMENTATION OF SERVER'S SERVICES
    
    def registerService(self):
        # we used forloop to ensure registration will always be fulfilled
        while 1:
            user,passwd = self.conn.recv(1024).decode().split(',')
            record = self.getAccountByUsername(user)
            if record != []:
                sendMsg(self.conn, "Account has been used")
                break
            else:
                try:
                    self.insertUser(user,passwd)
                    sendMsg(self.conn, "Account created successfully")
                    break
                except:
                    sendMsg(self.conn, "Error. Try again...")
                    traceback.print_exc()
                    break

    def loginService(self):
        while 1:
            user,passwd,ip,port = self.conn.recv(1024).decode().split(',')
            print(user)
            record = self.getAccountByUsernameAndPassword(user,passwd)
            if record == None:
                sendMsg(self.conn, "Tài khoản hoặc mật khẩu không tồn tại")
                break
            else:
                try:
                    self.updateUser(user,passwd,ip,port)
                    sendMsg(self.conn, "Kết nối thành công")
                    sendMsg(self.conn,user)
                    break
                except:
                    sendMsg(self.conn, "Lỗi truy vấn. Đang thử lại...")
                    traceback.print_exc()
                    break
    
    def searchService(self):
        while 1:
            user = self.conn.recv(1024).decode()
            record = self.getAddressByUsername(user)
            if record == None:
                sendMsg(self.conn, "Tài khoản tìm kiếm không tồn tại")
                break
            else:
                if (record != []):
                    data = str(record[0][0]+","+record[0][1])
                    sendMsg(self.conn,data)
                    break
                else:
                    sendMsg(self.conn, "Tài khoản đang offline")
                    break
    
    def getOnlineUsersService(self):
        records = self.getAccountsOnline()
        sendMsg(self.conn,str([record[1] for record in records]))
        
    # Database-Related Methods
    
    def initDatabaseConn(self):
        self.connector = sqlite3.connect('accounts.db')
        self.cursor = self.connector.cursor()
    
    def closeDatabaseConn(self):
        self.cursor.close()
        
    def getAccountByUsername(self,user):
        self.cursor.execute(f"""SELECT * FROM users WHERE username='{user}'""")
        records = self.cursor.fetchall()
        return records
    
    def getAccountByUsernameAndPassword(self,user,passwd):
        self.cursor.execute(f"""SELECT * FROM users WHERE username='{user}' AND password='{passwd}'""")
        records = self.cursor.fetchall()
        return records
    
    def getAccountsOnline(self):
        self.cursor.execute("SELECT * FROM users WHERE status=1")
        records = self.cursor.fetchall()
        return records

    def getAddressByUsername(self,user):
        self.cursor.execute(f"""SELECT ip,port FROM users WHERE username='{user}' AND status=1""")
        records = self.cursor.fetchall()
        print(records)
        return records
    
    def insertUser(self,user,passwd):
        self.cursor.execute(f"""INSERT INTO users (username,password,status) VALUES ('{user}','{passwd}',0)""")
        self.connector.commit()
    
    def updateUser(self,user,passwd,ip,port):
        self.cursor.execute(f"""UPDATE users SET status={1},ip='{ip}',port='{port}' WHERE username='{user}'""")
        self.connector.commit()

# UDPServer: One Server Thread to handle ALl Client Check-ins.
# Port: 4008
class UDPServer(threading.Thread):
    def __init__(self) -> None: # conn and addr are client's
        threading.Thread.__init__(self)
        self.HOST = HOST
        self.PORT = 3004
        self.server_socket = None
        self.running = 1
        self.ONLINE_LIST = {}

    # Define available types of request from peers
    def run(self): 
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.bind((self.HOST, self.PORT))

        print("UDP server started on port " + str(self.PORT) + "\n")
        
        threading.Thread(target=self.peerStatusCheck).start()

        while self.running == 1:
            try:
                userNameDataAndAddr = self.server_socket.recvfrom(1024)
                userNameData = userNameDataAndAddr[0].decode()

                userName, data = str(userNameData).split(",")
                #print(userNameData)
                if data == "Hello":
                    current = time.time()
                    self.ONLINE_LIST[userName] = current
                    # send a list of friends to the listening client
                    self.server_socket.sendto(str([friend[0] for friend in self.ONLINE_LIST]).encode(),userNameDataAndAddr[1])
                else:
                    print("Wrong UDP data format \n")
            except:
                print("UDP port error \n")
                traceback.print_stack()

    def peerStatusCheck(self):
        while udpThread.running == 1:
            for name in self.ONLINE_LIST.copy().keys(): # create a copy to prevent edit-on-iterate error
                elapsedTime = int(time.time() - self.ONLINE_LIST[name])
                if elapsedTime > 5:  # no response for more than 5 secs
                    print("Peer is offline -> '" + str(name) + "'\n") # print to server console
                    try:
                        self.ONLINE_LIST.pop(name)
                    except:
                        print("Online list update error")
                    # update database
                    self.updatePeerStatus(name)
                    
    def updatePeerStatus(self, userName):
        self.connector = sqlite3.connect('accounts.db')
        self.cursor = self.connector.cursor()  
        self.cursor.execute(f"UPDATE users SET status = 0 WHERE username = '{str(userName)}'")
        self.connector.commit()
        self.connector.close()

# sendMsg: Send message to a given connection
def sendMsg(conn, msg):
    try:
        conn.send(msg.encode())
    except:
        conn.close()
        
#### Client side: SIGNIN - SIGNUP
user_data_csv = "accounts.csv"
def sign_in(user_name, password):
    try:
        # check if appears
        print(user_name,password)
        check = False
        with open(user_data_csv, "rt") as f:
            csvreader = csv.reader(f, delimiter=",")
            for row in csvreader:
                print(row)
                if row == []:
                    break
                elif user_name == row[0]:
                    check = True
                    if password != row[2]:
                        tkinter.messagebox.showerror(title="Lỗi đăng nhập",message="Nhập sai mật khẩu !!")
                        return
                    else:
                        tkinter.messagebox.showinfo(title="Chuyển hướng",message="Đăng nhập thành công !!")
                        
                        # Get your IP Address and Find available socket - picked by OS
                        host_name = socket.gethostname()
                        ip_addr = socket.gethostbyname(host_name)
                        
                        sock = socket.socket()
                        sock.bind(('', 0))
                        free_sock = sock.getsockname()[1]
                        
                        print(f"Login-> IP: {ip_addr}, Port: {free_sock}")
                        Peer_Central(ip_addr,int(free_sock)).run()
                        return
            if not check:
                tkinter.messagebox.showerror(title="Lỗi đăng nhập",message="Tài khoản không tồn tại !!")
    except IOError:
        print("I/O error")

def sign_up(user_name, full_name, password):
    try:
        # check if appears
        with open(user_data_csv, "rt") as f:
            csvreader = csv.reader(f, delimiter=",")
            for row in csvreader:
                if row == []:
                    break
                elif user_name in row[0]:
                    tkinter.messagebox.showerror(title="Lỗi đăng kí",message="Tài khoản đã được đăng kí")
                    return
        # append
        with open(user_data_csv, 'a') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow((user_name, full_name, password))
        tkinter.messagebox.showinfo(title="Chuyển hướng",message="Đăng kí tài khoản thành công !!")
    except IOError:
        print("I/O error")

if __name__ == "__main__":
    tcpThread = TCPServer()
    udpThread = UDPServer()
    udpThread.start()
    tcpThread.start()
import threading, time
import socket, select
from tkinter import *
from tkinter import font
from tkinter import ttk
from tkinter import messagebox
import sys,json
from protocol import Encode
import logging
from protocol import Encode
FORMAT = "utf-8"


# This is Server Side of The Peer
# This will contain an Array of All Client Connection
# This Will Act As A Chat Room
class PeerServer(threading.Thread):
    ClientList = [] # List Of Client Connection IP:Connection 
    peerIP = None
    peerPort = None
    def __init__(self,peerIp,peerPort) -> None:
        threading.Thread.__init__(self)
        self.CliendList = []
        self.peerIP = peerIp
        self.listenPort = 80

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((peerIp, self.listenPort))


    def run(self):
        self.server.listen(100)
        print("Start Listening on Port: {}".format(self.listenPort))
        inputs = [self.server]

        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # Comment This one To act as Client because Server Thread will Take place std in
        while(inputs):
            try:
                readable, writable, exceptional = select.select(inputs, [], [])
                for s in readable:
                    if s is self.server:
                        
                            conn, addr = s.accept()
                            print(conn)
                            """ conn.bind((self.peerIP,0))   """                     
                            self.createClientThread(conn,addr[0],addr[1])
                            self.ClientList.append(conn)
                    else:
                        print("Stuck Here")
            except Exception as e:
                print(e)

    def createClientThread(self,conn,cliIP, cliPort) :
        # Create A Thread For Handle That Connection
        # May be a new window
        PeerClient(self.peerIP,conn,cliIP,cliPort).start()
        self.CliendList.append(conn)
    def sendToAll(self,conn):
        pass
    def closeConn(self,conn):
        pass
    def getConn(self, conn):
        pass

# This is Client Side Of the Peer
# Request and send Message Chat to Other Peer
# This handle Each Connection
# This Class Maybe Handle Transfer
class PeerClient(threading.Thread):
     # constructor method
    def __init__(self, name,conn,ip,port):
        threading.Thread.__init__(self)
        # chat window which is currently hidden
        self.name = name
        self.conn = conn
        self.cip = ip
        self.port = port
        self.Encoder = Encode(ip,port)



    def run(self) :
        self.Window = Tk()
        self.Window.withdraw()
        self.goAhead(self.name)
        self.Window.mainloop()
    
    

    def goAhead(self, name):
        self.layout(name)
        # the thread to receive messages
        rcv = threading.Thread(target=self.receive)
        rcv.start()
 
    # The main layout of the chat 57A1F8
    def layout(self, name):
        self.name = name
        # to show chat window
        self.Window.deiconify()
        self.Window.title("CHATROOM")
        self.Window.resizable(width=True,
                              height=False)
        self.Window.configure(width=470,
                              height=550,
                              bg="#57A1F8")
        # Head of The Chat
        self.labelHead = Label(self.Window,
                               bg="#17202A",
                               fg="#EAECEE",
                               text=self.name,
                               font="Helvetica 13 bold",
                               pady=5)
 
        self.labelHead.place(relwidth=1)
        self.line = Label(self.Window,
                          width=450,
                          bg="#ABB2B9")
 
        self.line.place(relwidth=1,
                        rely=0.07,
                        relheight=0.012)
        # Chat Message
        self.textCons = Text(self.Window,
                             width=20,
                             height=2,
                             bg="#17202A",
                             fg="#EAECEE",
                             font="Helvetica 12",
                             padx=20,
                             pady=5,
                             )
 
        self.textCons.place(relheight=0.745,
                            relwidth=1,
                            rely=0.08)
                            
        self.textCons.tag_config("send",foreground="green"
                                ,justify=RIGHT) # Tag to change color
        

        self.labelBottom = Label(self.Window,
                                 bg="#ABB2B9",
                                 height=80)
 
        self.labelBottom.place(relwidth=1,
                               rely=0.825)
        # Enter Message box
        self.entryMsg = Entry(self.labelBottom,
                              bg="#2C3E50",
                              fg="#EAECEE",
                              font="Helvetica 11")
 
        # place the given widget
        # into the gui window
        self.entryMsg.place(relwidth=0.74,
                            relheight=0.06,
                            rely=0.008,
                            relx=0.011)
 
        self.entryMsg.focus()
 
        # create a Send Button
        self.buttonMsg = Button(self.labelBottom,
                                text="Send",
                                font="Helvetica 10 bold",
                                width=20,
                                bg="#ABB2B9",
                                command=lambda: self.sendButton(self.entryMsg.get()))
 
        self.buttonMsg.place(relx=0.77,
                             rely=0.008,
                             relheight=0.06,
                             relwidth=0.22)

        # create a Send Button
        self.buttonSendFile = Button(self.labelBottom,
                                text="File",
                                font="Helvetica 10 bold",
                                width=20,
                                bg="#ABB2B9",
                                command=lambda: self.sendButton(self.entryMsg.get()))
 
        self.buttonSendFile.place(relx=0.77,
                             rely=0.008,
                             relheight=0.06,
                             relwidth=0.22)
 
        self.textCons.config(cursor="arrow")
 

        self.textCons.config(state=DISABLED)
 
    # function to basically start the thread for sending messages
    def sendButton(self, msg):
        self.textCons.config(state=DISABLED)
        self.msg = msg
        self.entryMsg.delete(0, END)
        snd = threading.Thread(target=self.sendMessage)
        snd.start()
 
    def displayMessage(self,msg, send=False):
        self.textCons.config(state=NORMAL)
        if(send):
            self.textCons.insert(END,
                                    msg+"\n\n","send")
        else:
             self.textCons.insert(END,
                                    msg+"\n\n")

        self.textCons.config(state=DISABLED)
        self.textCons.see(END)
     


    # function to receive messages 
    # This will handle request send from user
    def receive(self):
        while True:
            # try:
            message = self.conn.recv(1024).decode(FORMAT)
            message = json.loads(message)
            # If message is request message
            if message['type'] == 'Request':
                # If it is Start Chat Request
                if message['flag'] == "S":
                    # Call UIn   
                    diaglogResult = messagebox.askokcancel("There is Message Request","{} requested chat. Accept?".format(self.cip))
                    if(diaglogResult):
                        self.conn.send(self.Encoder.acceptChat())
                    else:
                        self.conn.send(self.Encoder.declineChat())
                        self.Window.destroy()
            elif  message['type'] == 'M':
                # insert messages to text box
                self.displayMessage("("+message["time"]+"):"+message['msg'])
            """    except:
                # an error will be printed on the command line or console if there's an error
                print("An error occurred!")
                self.conn.close()
                break
  """
    # function to send messages
    def sendMessage(self):
        self.textCons.config(state=DISABLED)
        while True and self.msg != "":
            #############
            message = (f"{self.msg}")
            self.displayMessage(self.msg, send=True)        
            self.conn.send(self.Encoder.sendMessage(message))
            break



# This is The Peer Main Class act as A routing
# It will contain Server side and Client Side
# This peer will listen request sent from other Peer
START_CHECKING = False
class Peer_Central():
    def __init__(self):
        self.HOST = '192.168.0.125'
        self.PORT_TCP = 3000
        self.PORT_UDP = 3004
        self.central_client_socket = None
        self.userName = None
        self.password = None
        self.ip_addr = None
        self.port = None
        self.CONDITION = True
        self.startTime = 0
        self.endTime = 0
        self.running = 1
        self.friendSatus = [] # Manage User Status
        self.HandleConnection = None # handle Connection
        self.Encoder = None
    
    def run(self):
        # Create central socket - TCP port
        self.central_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.central_client_socket.connect((self.HOST, self.PORT_TCP))
        except:
            print('Unable connection to central server unit')
        
        # Maintain online
        threading.Thread(target=self.checkConn).start()
            
        # Choose
        while self.running == 1:
            while self.CONDITION:
                print ("\n---------------------------------------------------")
                choice = str(input("\rPlease, press '1' for registration, '2' for join: "))
                print ("---------------------------------------------------\n")
                if choice == "1":
                    self.registerClient()
                    break
                elif choice == "2":
                    self.loginClient()
                    self.CONDITION = False
                    #self.kill()
                    break
                else:
                    print("1 or 2 only ! \n ")
            time.sleep(0)
    
    
    def checkConn(self):
        self.checkConn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        while True:
            if(START_CHECKING):
                self.endTime = time.time()
                elapsedTime = int(self.endTime - self.startTime)
                # send to server after 3 secs
                if (elapsedTime % 3) == 0:
                    data = str(self.userName + "," + "Hello")
                    self.checkConn.sendto(data.encode(), (self.HOST, int(self.PORT_UDP)))
            time.sleep(0.1)
    
    def registerClient(self):
        self.central_client_socket.send("register".encode())
        
        # register validation stuff (client side)
        self.userName = str(input("UserName: "))
        self.password = str(input("Password: "))
        data = str(self.userName + "," + self.password)
        
        self.central_client_socket.send(data.encode())
        processStatus = self.central_client_socket.recv(1024).decode()
        print(processStatus)
    
    def loginClient(self):
        hostname = socket.getfqdn()
        ip_addr = socket.gethostbyname_ex(hostname)[2][1]

        sock = socket.socket()
        sock.bind((ip_addr, 0))
        free_sock = sock.getsockname()[1]
        
        # login validation stuff (client side)
        self.central_client_socket.send("login".encode())
        self.userName = str(input("UserName: "))
        self.password = str(input("Password: "))
        self.ip_addr = str(ip_addr)
        self.port = 80
        self.Encoder = Encode(self.ip_addr, self.port) # Initialize Encoder
        # Launch Peer Server to Handle Incomminng Connection
        self.HandleConnection =  PeerServer(self.ip_addr, self.port)
        self.HandleConnection.daemon=True
        self.HandleConnection.start()


        # Send Login Information To Server
        data = str(self.userName + "," + self.password+","+self.ip_addr+","+str(self.port))
        
        self.central_client_socket.send(data.encode())
        processStatus = self.central_client_socket.recv(1024).decode()
        print(processStatus)
    
        # Assume that login is complete
        global START_CHECKING 
        START_CHECKING = True
        self.startTime = time.time()
        
        while True:
            # Greeting...
            print(f"\n Welcome {self.central_client_socket.recv(1024).decode()}")
            
            # Show online users
            self.central_client_socket.send("onlineList".encode())
            time.sleep(0.2)
            data = self.central_client_socket.recv(4096).decode()
            printOnlineUsers(data)
            
            
            while 1:
                user = input("\rType Username you want to chat with: ")
                self.central_client_socket.send("search".encode())
                self.central_client_socket.send(user.encode())
                peer_ip,peer_port = self.central_client_socket.recv(1024).decode().split(",")
                conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                conn.connect((peer_ip, 80))
                # Send Request Chat
                conn.send(self.Encoder.requestChat())

                # Wait Until Receive
                msg = conn.recv(1024).decode(FORMAT)
                msg = json.loads(msg)
                if(msg['code']==1):
                    self.HandleConnection.createClientThread(conn,self.ip_addr,self.port)
                else:
                    print("Peer Decline Chat")
                # Open Box Chat from Peer to Peer
            break


        self.HandleConnection.join()
            
        
def printOnlineUsers(data):
    print ("\t\t<<< ONLINE USER LIST >>>\r")
    print ("\t UserName    IpAddress    Port\n")
    onlineList = data[1:-1].replace("(", "").replace(")", "").replace(",", "").replace("'", "").split(" ")
    iteration = 1
    userAllInfo = ""
    for userInfo in onlineList:
        if (iteration%3) == 0:
            print("\t" + userAllInfo + userInfo + ",   ")
            userAllInfo = ""    
        else:
            userAllInfo = userAllInfo + userInfo + ",   "
        iteration += 1
                
if __name__ == "__main__":
    # [ip,port] = input("IP Port: ").strip().split(" ")
    # Peer(ip,int(port)).run()
    peer_central = Peer_Central()
    peer_central.run()
    
    #[ip,port] = input("IP Port: ").strip().split(" ")
    # ip = socket.gethostbyname(socket.gethostname())
    #Peer(ip,int(port)).run()



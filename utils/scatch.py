# This is The Peer Main Class act as A routing
# It will contain Server side and Client Side
# This peer will listen request sent from other Peer
import socket
from tkinter import *
from threading import *
from protocol import *
# from utils.protocol import *
import peer
import LinkedUI

class Peer:
    def __init__(self, peerName, peerIp, peerPort) -> None:
        self.peerName = peerName
        self.peerIp = peerIp
        self.peerPort = peerPort
        self.Encoder = Encode(self.peerIp, self.peerPort)

        self.HandleConnection=peer.PeerServer(self.peerName, self.peerIp,self.peerPort)
        self.HandleConnection.daemon=True
        self.HandleConnection.start()
    
    def run(self):
        # lúc mới login xong thì đây sẽ chạy cái list user online
        LinkedUI.ListPage()
    # This is for testing purpose
    def runUI(self): 
        self.Window = Tk()
        self.Window.withdraw()
        self.goAhead("Haha")
        self.Window.mainloop()

    def goAhead(self, name):
        self.layout(name)
        # the thread to receive messages
    # The main layout of the chat
    def layout(self, name):
        self.name = name
        # to show chat window
        self.Window.deiconify()
        self.Window.title("Hello User {}".format(self.peerIp))

        self.Window.configure(width=470,
                              height=150,
                              bg="#17202A")
                              
        self.labelBottom = Label(self.Window,
                                 bg="#ABB2B9",
                                 height=80)
        self.labelBottom.place(relwidth=1,
                               rely=0)
        self.entryMsg = Entry(self.labelBottom,
                              bg="#2C3E50",
                              fg="#EAECEE",
                              font="Helvetica 13")

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
        
    # function to basically start the thread for sending messages
    def sendButton(self, msg):
        self.msg = msg
        self.entryMsg.delete(0, END)
        [ip,port] = self.msg.strip().split(" ")
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect((ip, int(port)))
        conn.send(Encode.requestChat())
        conn.recv(1024)
        self.HandleConnection.createClientThread(conn,ip,port)

        conn.send(self.Encoder.requestChat())

        msg = conn.recv(1024).decode(FORMAT)
        msg = json.loads(msg)
        if(msg['code']==1):
            self.HandleConnection.createClientThread(conn,ip,port)
        else:
            print("Peer Decline Chat")


    # This is for testing purpose
    def runUI(self):                                                                # from Khang: Chỗ này bị lặp lại ở trên? 
        self.Window = Tk()
        self.Window.withdraw()
        self.goAhead("Haha")
        self.Window.mainloop()

    def goAhead(self, name):
        self.layout(name)
        # the thread to receive messages
 
    # The main layout of the chat
    def layout(self, name):
 
        self.name = name
        # to show chat window
        self.Window.deiconify()
        self.Window.title("Hello User {}".format(self.peerIp))

        self.Window.configure(width=470,
                              height=150,
                              bg="#17202A")
                              
        self.labelBottom = Label(self.Window,
                                 bg="#ABB2B9",
                                 height=80)
 
        self.labelBottom.place(relwidth=1,
                               rely=0)
 
        self.entryMsg = Entry(self.labelBottom,
                              bg="#2C3E50",
                              fg="#EAECEE",
                              font="Helvetica 13")
 
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
 
    # function to basically start the thread for sending messages
    def sendButton(self, msg):
        self.msg = msg
        self.entryMsg.delete(0, END)
        [ip,port] = self.msg.strip().split(" ")
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect((ip, int(port)))
        conn.send(Encode.requestChat())
        conn.recv(1024)
        self.HandleConnection.createClientThread(conn,ip,port)

import threading
import socket

# This is Server Side of The Peer
# This will contain an Array of All Client Connection
# This Will Act As A Chat Room
class PeerServer(threading.Thread):
    ClientList = [] # List Of Client Connection
    peerIP = None
    peerPort = None

    def __init__(self) -> None:
        threading.Thread.__init__(self)
        self.CliendList = []
    def createClientThread(self,conn) :
        # Create A Thread For Handle That Connection
        # May be a new window
        PeerClient().start()
        self.CliendList.append(conn)
        pass
    def sendMsg(conn):
        pass
    def closeConn(conn):
        pass

# This is Client Side Of the Peer
# Request and send Message Chat to Other Peer
# This handle Each Connection
class PeerClient(threading.Thread):
     # constructor method
    def __init__(self, name,conn):
        threading.Thread.__init__(self)
        # chat window which is currently hidden
        self.name = name
        self.conn = conn


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
 
    # The main layout of the chat
    def layout(self, name):
 
        self.name = name
        # to show chat window
        self.Window.deiconify()
        self.Window.title("CHATROOM")
        self.Window.resizable(width=False,
                              height=False)
        self.Window.configure(width=470,
                              height=550,
                              bg="#17202A")
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
 
        self.textCons = Text(self.Window,
                             width=20,
                             height=2,
                             bg="#17202A",
                             fg="#EAECEE",
                             font="Helvetica 14",
                             padx=5,
                             pady=5)
 
        self.textCons.place(relheight=0.745,
                            relwidth=1,
                            rely=0.08)
 
        self.labelBottom = Label(self.Window,
                                 bg="#ABB2B9",
                                 height=80)
 
        self.labelBottom.place(relwidth=1,
                               rely=0.825)
 
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
 
        self.textCons.config(cursor="arrow")
 
        # create a scroll bar
        scrollbar = Scrollbar(self.textCons)
 
        # place the scroll bar
        # into the gui window
        scrollbar.place(relheight=1,
                        relx=0.974)
 
        scrollbar.config(command=self.textCons.yview)
 
        self.textCons.config(state=DISABLED)
 
    # function to basically start the thread for sending messages
    def sendButton(self, msg):
        self.textCons.config(state=DISABLED)
        self.msg = msg
        self.entryMsg.delete(0, END)
        snd = threading.Thread(target=self.sendMessage)
        snd.start()
 
    # function to receive messages
    def receive(self):
        while True:
            try:
                message = self.conn.recv(1024).decode(FORMAT)
 
                # if the messages from the server is NAME send the conn's name
                if message == 'NAME':
                    self.conn.send(self.name.encode(FORMAT))
                else:
                    # insert messages to text box
                    self.textCons.config(state=NORMAL)
                    self.textCons.insert(END,
                                         message+"\n\n")
 
                    self.textCons.config(state=DISABLED)
                    self.textCons.see(END)
            except:
                # an error will be printed on the command line or console if there's an error
                print("An error occurred!")
                self.conn.close()
                break
 
    # function to send messages
    def sendMessage(self):
        self.textCons.config(state=DISABLED)
        while True:
            message = (f"{self.name}: {self.msg}")
            self.conn.send(message.encode(FORMAT))
            break



# This is The Peer Main Class act as A routing
# It will contain Server side and Client Side
# This peer will listen request sent from other Peer

class Peer:
    HandleConnection = None
    peerIp = None
    peerPort = None
    def __init__(self,peerIp, peerPort) -> None:
        self.peerIp = peerIp
        self.peerPort = peerPort
        self.HandleConnection=PeerServer()
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def run(self):
        pass

if __name__ == "__main__":
    pass



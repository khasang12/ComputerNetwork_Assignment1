from functools import cache
from tkinter import *
import tkinter.messagebox
from PIL import Image, ImageTk
import socket, threading, sys, traceback, os

from RtpPacket import RtpPacket

CACHE_FILE_NAME = "cache-"
CACHE_FILE_EXT = ".jpg"


class Client:
    INIT = 0
    READY = 1
    PLAYING = 2
    state = INIT

    SETUP = 0
    PLAY = 1
    PAUSE = 2
    TEARDOWN = 3

    # Initiation..
    def __init__(self, master, serveraddr, serverport, rtpport, filename):
        self.master = master
        self.master.protocol("WM_DELETE_WINDOW", self.handler)
        self.createWidgets()
        self.serverAddr = serveraddr
        self.serverPort = int(serverport)
        self.rtpPort = int(rtpport)
        self.fileName = filename
        self.rtspSeq = 0
        self.sessionId = 0
        self.requestSent = -1
        self.teardownAcked = 0
        self.rtspSock = None
        self.connectToServer()
        self.frameNbr = 0

    # THIS GUI IS JUST FOR REFERENCE ONLY, STUDENTS HAVE TO CREATE THEIR OWN GUI
    def createWidgets(self):
        """Build GUI."""
        # Create Setup button
        self.setup = Button(self.master, width=20, padx=3, pady=3)
        self.setup["text"] = "Setup"
        self.setup["command"] = self.setupMovie
        self.setup.grid(row=1, column=0, padx=2, pady=2)

        # Create Play button
        self.start = Button(self.master, width=20, padx=3, pady=3)
        self.start["text"] = "Play"
        self.start["command"] = self.playMovie
        self.start.grid(row=1, column=1, padx=2, pady=2)

        # Create Pause button
        self.pause = Button(self.master, width=20, padx=3, pady=3)
        self.pause["text"] = "Pause"
        self.pause["command"] = self.pauseMovie
        self.pause.grid(row=1, column=2, padx=2, pady=2)

        # Create Teardown button
        self.teardown = Button(self.master, width=20, padx=3, pady=3)
        self.teardown["text"] = "Teardown"
        self.teardown["command"] = self.exitClient
        self.teardown.grid(row=1, column=3, padx=2, pady=2)

        # Create a label to display the movie
        self.label = Label(self.master, height=19)
        self.label.grid(
            row=0, column=0, columnspan=4, sticky=W + E + N + S, padx=5, pady=5
        )

    def setupMovie(self):
        """Setup button handler."""
        if self.state == self.INIT:
            self.sendRtspRequest(self.SETUP)


    def exitClient(self):
        """Teardown button handler."""
        self.sendRtspRequest(self.TEARDOWN)
        self.master.destroy()
        cache_name = CACHE_FILE_NAME + self.sessionId + CACHE_FILE_EXT
        os.remove(cache_name)


    def pauseMovie(self):
        """Pause button handler."""
        if self.state == self.PLAYING:
            self.sendRtspRequest(self.PAUSE)


    def playMovie(self):
        """Play button handler."""
        self.sendRtspRequest(self.PLAY)


    def listenRtp(self):
        """Listen for RTP packets."""

    def writeFrame(self, data):
        """Write the received frame to a temp image file. Return the image file."""
        cache_name = CACHE_FILE_NAME + self.sessionId + CACHE_FILE_EXT
        cache_file = open(cache_name, "wb")
        cache_file.write(data)
        cache_file.close()
        return cache_file


    def updateMovie(self, imageFile):
        """Update the image file as video frame in the GUI."""


    def connectToServer(self):
        """Connect to the Server. Start a new RTSP/TCP session."""
        # INIT CONNECTION - Client Side
        self.rtspSock = socket.socket()
        self.rtspSock.connect((self.serverAddr, self.serverPort))

    def sendRtspRequest(self, requestCode):
        """Send RTSP request to the server."""
        # -------------
        # TO COMPLETE
        # -------------

    def recvRtspReply(self):
        """Receive RTSP reply from the server."""
        # TODO

    def parseRtspReply(self, data):
        """Parse the RTSP reply from the server."""
        # TODO
        lines = data.split('\n')
        seqNum = int(lines[1].split(' ')[1])

        if seqNum == self.rtspSeq:
            session = int(lines[2].split(' ')[1])
            # Set RSTP session ID
            self.sessionId == session
            if self.sessionId == session and int(lines[0].split(' ')[1]) == 200:
                if self.requestSent == self.SETUP:
                    # Update RSTP state
                    self.state = self.READY
                    self.openRtpPort()
                elif self.requestSent == self.PLAY:
                    # Update RSTP state
                    self.state = self.PLAYING
                elif self.requestSent == self.PAUSE:
                    # Update RSTP state
                    self.state = self.READY
                    # Create new thread when last play thread is exit
                    self.playEvent.set()
                elif self.requestSent == self.TEARDOWN:
                    # Update RSTP state
                    self.state = self.INIT
                    self.teardownAcked = 1


    def openRtpPort(self):
        """Open RTP socket binded to a specified port."""
        # -------------
        # TO COMPLETE
        # -------------
        # Create a new datagram socket to receive RTP packets from the server
        # self.rtpSocket = ...
        self.rtpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Set the timeout value of the socket to 0.5sec
        # ...
        self.rtpSocket.settimeout(0.5)

    def handler(self):
        """Handler on explicitly closing the GUI window."""
        # TODO
        self.pauseMovie()
        if tkinter.messagebox.askokcancel("Confirmation", "Do you want to exit the client?"):
            self.exitClient() # Exit client
        else:
            self.playMovie() # Continue to play movie
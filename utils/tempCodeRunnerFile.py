while(inputs):
        #     readable, writable, exceptional = select.select(inputs, [], [])
        #     for s in readable:
        #         if s is self.server:
        #                 # accepts the connection, and adds its connection socket to the inputs list
        #                 # so that we can monitor that socket as well
        #                 conn, addr = s.accept()
        #                 self.createClientThread(conn)
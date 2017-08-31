# udp SERVER

import socketserver

count = 0
nOfWins = 0
stored_client = ('null', 0)
connected = []

# Binding the socket to the port
server_address = ('localhost', 9999)

print('Server running on:', server_address)


class MyUDPHandler(socketserver.DatagramRequestHandler):

    def handle(self):

        # global variables are used because the function resets them every time the connection is made otherwise
        global count
        global nOfWins
        global stored_client

        # messages to send to the client
        win = "You win!"
        lose = "You lose!"
        stop = "Game over!"

        # adding TWO clients to the game
        if len(connected) < 1:
            connected.append(self.client_address)
            stored_client = connected[0]
        elif connected[0] == stored_client:
            connected.append(self.client_address)

        # receiving messages
        cid = self.request[0]

        cint = self.request[1].recv(1024)
        print("\nInteger received: ")
        print(cint.decode("utf-8", "ignore"))

        # maths
        cint = int(cint.decode("utf-8", "ignore"))
        count = (cint+count) % 10

        if len(connected) == 2:

            # sending messages to client
            if nOfWins < 3:
                if count == 0:
                    self.request[1].sendto(win.encode("utf-8"), connected[0])
                    print("\nWINNER IS:", stored_client)
                    nOfWins += 1

                    # clearing the cache
                    del connected[:]
                    stored_client = ('null', 0)
                else:
                    self.request[1].sendto(lose.encode("utf-8"), connected[0])
                    print("\n", stored_client, "lost!")

                    # clearing the cache
                    del connected[:]
                    stored_client = ('null', 0)
            else:
                self.request[1].sendto(stop.encode("utf-8"), connected[0])
                self.request[1].sendto(stop.encode("utf-8"), connected[1])
                print("\nTHE GAME IS OVER!")

                # clearing the cache
                del connected[:]
                stored_client = ('null', 0)

# serve forever
if __name__ == "__main__":
    server = socketserver.UDPServer(server_address, MyUDPHandler, bind_and_activate=True)
    server.serve_forever()

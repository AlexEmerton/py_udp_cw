# udp CLIENT
import socket

server_address = ('localhost', 9999)

while True:
    # state variable; 0 means the client is online // 1 means it is offline
    state = 0

    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # prompt an ID from the user
    clientID = input('\nPlease enter your ID (1-100): ')

    while int(clientID) < 1 or int(clientID) > 100:
        print('\nClientID value is unacceptable please try again')
        clientID = input('Please enter your ID (1-100): ')

    # prompt an integer from the user
    clientINT = input('Please enter an integer of your choice: ')

    # sending 2 packets
    sock.sendto(clientID.encode('utf-8'), server_address)
    sock.sendto(clientINT.encode('utf-8'), server_address)

    # receiving packets
    while state == 0:
        print("\nwaiting to receive...")
        received = sock.recv(4096)
        received = received.decode("utf-8", "ignore")
        if received == "You win!" or received == "You lose!":

            # closing the client
            state += 1
            print("\nTHE RESULT IS: ", received)
            sock.close()
        elif received == "Game over!":
            state += 1
            print("\nGAME IS OVER!")
            sock.close()

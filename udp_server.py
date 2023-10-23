import socket, select, time, re, threading

def run(serverSocket, serverPort):
    # The main server function.
    print("\nCHATROOM - UDP\n")
    print("This is the server side.")
    print(f"I am ready to receive connections on port {serverPort}\n")

    # message loop
    while True:
        try:
            msg, clientAddr = serverSocket.recvfrom(2048)
            msg = msg.decode()

            # get the username from the message
            username = re.search(USERNAME_REGEX, msg).group()

            if clientAddr not in clients: #the user is new
                print(f"Message received from {clientAddr}: joining: {username}")
                print(f"User {username} joined from address {clientAddr}")
                clients[clientAddr] = username
            
            if msg:
                if msg[len(username) + 2::] == "exit": #check message without username and ': ' characters
                    print(f"User {username} left the chat from address {clientAddr}!")
                    del clients[clientAddr] 
                else:
                    print(f"Message received from {clientAddr}: {msg}")
                    broadcastMessage(msg, clientAddr) 
        except KeyboardInterrupt:
            print("keyboard interrupt detected. shutting down")
            serverSocket.close()
            break
    print("shut down")

def broadcastMessage(msg, senderAddr):
    for clientAddr, username in clients.items():
        if clientAddr != senderAddr: # do not send message back to the original sender
            serverSocket.sendto(msg.encode(), clientAddr) 

# **Main Code**:  
if __name__ == "__main__":
    USERNAME_REGEX = "^[^:]+\s*"
    clients = {} #client address -> username
    serverPort = 9301 
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Creating a UDP socket.
    serverSocket.bind(('127.0.0.1',serverPort))
    run(serverSocket, serverPort)  # Calling the function to start the server.


    
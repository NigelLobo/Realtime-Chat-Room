import socket, threading, select, time

def run(serverSocket, serverPort):
    # The main server function.
    print("\nCHATROOM - TCP\n")
    print("This is the server side.")
    print(f"I am ready to receive connections on port {serverPort}\n")

    # loop to always accept clients
    while True:
        try:
            clientSocket, clientAddr = serverSocket.accept()
            clients.append((clientSocket, clientAddr))
            clientThread = threading.Thread(target=handleClient, args=(clientSocket, clientAddr,))
            clientThread.start()
        except KeyboardInterrupt:
            print("keyboard interrupt detected: shutting down")
            for client in clients:
                client[0].close()
            serverSocket.close() 
            break
            
    print("shut down")
        
def handleClient(clientSocket, clientAddr):
    # wait for client to send username
    username = clientSocket.recv(1024).decode()
    print(f"Message received from {clientAddr}: joining: {username}")
    print(f"User {username} joined from address {clientAddr}")

    # message loop
    while True:
        try:
            msg = clientSocket.recv(1024).decode()
            if msg: 
                print(f"Message recieved from {clientAddr}: {msg}")
                broadcastMessage(msg, clientSocket)
            else: #blank message sent
                print(f"\n{username} left from address {clientAddr}!")
                clientSocket.close()
                clients.remove((clientSocket, clientAddr))
                broadcastMessage(f"{username} left from address {clientAddr}!", None)
                break
        except KeyboardInterrupt:
            print("keyboard interrupt detected. shutting down")
            clientSocket.close()
            clients.remove((clientSocket, clientAddr))
            print(f"{username} left from address {clientAddr}!")
            broadcastMessage(f"{username} left from address {clientAddr}!", None)
            break
        except Exception:
            clientSocket.close()
            clients.remove((clientSocket, clientAddr))
            print(f"{username} left from address {clientAddr}!")
            broadcastMessage(f"{username} left from address {clientAddr}!", None)
            break

def broadcastMessage(msg, senderSocket):
    for client in clients:
        if client[0] != senderSocket: #do not send the message again to the sender
            client[0].send(msg.encode())


if __name__ == "__main__":
    server_port = 9301
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)# Creating a TCP socket.
    server_socket.bind(('127.0.0.1', server_port))
    server_socket.listen(3) 
    
    clients = [] 
    run(server_socket,server_port)# Calling the function to start the server.

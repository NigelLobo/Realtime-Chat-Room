import sys, socket, argparse, select, threading

def run(clientSocket, clientname):
    # The main client function.
    broadcastThread = threading.Thread(target=handleBroadcastedMessages, args=(clientSocket,clientname))
    broadcastThread.start()

    while True:
        try:
            msg = input(clientname + ": ")
            clientSocket.send(f"{clientname}: {msg}".encode())
        except KeyboardInterrupt:
            print("keyboard interrupt detected: shutting down")
            clientSocket.close()
            break
    print("shut down")

def handleBroadcastedMessages(clientSocket, clientname):
    while True:
        try:
            externalMsg = clientSocket.recv(1024).decode()
            if externalMsg: 
                # print the message at the beginning of the line using a carriage return
                # reprint the username so the input waiting state has the same look
                print(f"\r{externalMsg}\n{clientname}: ", end="")
            else: raise Exception
        except Exception:
            print("There was an exception. Shutting down connection")
            clientSocket.close()
            break

# **Main Code**:  
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Argument Parser')
    parser.add_argument('name')  # to use: python tcp_client.py username
    args = parser.parse_args()
    client_name = args.name
    server_addr = '127.0.0.1'
    server_port = 9301

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TCP
    client_socket.connect((server_addr, server_port))
    client_socket.send(client_name.encode()) #send username upon connecting to server
    run(client_socket, client_name)
 

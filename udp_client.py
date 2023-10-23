import sys, socket, argparse, select, threading

def run(clientSocket, clientname, serverAddr, serverPort):
    # The main client function.
    threadStarted = False

    while True:
        try:
            msg = input(clientname + ": ")
            clientSocket.sendto(f"{clientname}: {msg}".encode(), (serverAddr, serverPort))
            
            if msg == "exit":
                print("client closing.....")
                clientSocket.close()
                break
            if not threadStarted: #there is no persistent connection, so we must use a flag
                broadcastedThread = threading.Thread(target=handleBroadcastedMessages, args=(clientname,clientSocket))
                broadcastedThread.start()
                threadStarted = True

        except KeyboardInterrupt:
            print("keyboard interrupt detected. Shutting down")
            clientSocket.close()
            break
    print("shut down")

def handleBroadcastedMessages(clientname, clientSocket): #clientname refers to the current user's name for the session, not the sender's
    while True:
        try:
            # get the message
            externalMsg, serverAddr = clientSocket.recvfrom(1024)
            if externalMsg: 
                # print the message at the beginning of the line using a carriage return
                # reprint the username so the input waiting state has the same look
                print(f"\r{externalMsg.decode()}\n{clientname}: ", end="")
            else: raise Exception
        except Exception:    
            print("Shutting down connection")
            clientSocket.close()
            break

if __name__ == "__main__":
    
    # Arguments: name address
    parser = argparse.ArgumentParser(description='argument parser')
    parser.add_argument('name')  # to use: python udp_client.py username
    args = parser.parse_args()
    clientname = args.name
    serverAddr = '127.0.0.1'
    serverPort = 9301
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
    run(clientSocket, clientname, serverAddr, serverPort)  # Calling the function to start the client.

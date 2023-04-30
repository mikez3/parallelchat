import threading
import socket
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog


host = '127.0.0.1'
port = 59000
# Creating a server object (address family: IPv4, type of socket: TCP)
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

# Bind the server to the host and the port
server.bind((host, port))

# Activate the listening node for any incoming connections to the server
server.listen()
clients = []
nicknames = []

# Send a message from the server to all the connected clients
def broadcast(message):
      for client in clients:
            client.send(message)

# Handle the connection of each client
def handle_client(client):
      while True:
            try:      
                  # 1024 = max bytes that server can recieve from a client
                  message = client.recv(1024)
                  broadcast(message)
            # errors of connection failures
            except:
                  index = clients.index(client)
                  clients.remove(client)
                  client.close()
                  nickname = nicknames[index]
                  # encode: it must be in form of bytes, not string
                  broadcast(f'{nickname} has left the chat room!'.encode('utf-8'))
                  nicknames.remove(nickname)
                  break
        
# Receive clients connections
def recieve():
      while True:
            print('Server is running and listening for connections...')
            # Ready to accept any incoming connections
            client, address = server.accept()
            print(f'\nconnection is established with address: {str(address)}')
            client.send('nickname?'.encode('utf-8'))
            nickname = client.recv(1024)
            nicknames.append(nickname)
            clients.append(client)
            print(f'The nickname of this client is {nickname}'.encode('utf-8'))
            broadcast(f'{nickname} has just connected to the chat room!'.encode('utf-8'))
            # Msg from Server to Client
            client.send('You are now connected!'.encode('utf-8'))
            # Create a thread
            thread = threading.Thread(target=handle_client, args=(client,))
            thread.start()

if __name__ == "__main__":
      recieve()
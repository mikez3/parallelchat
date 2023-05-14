import threading
import socket

nickname = input('Pick a nickname: ')
# Create a client object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect the client to the localhost and the port
client.connect(('127.0.0.1', 59000))


# Receiving messages from other clients through the server
def client_receive():
    while True:
        try:
            # Decode because the message here is received from another client (and not sent)
            message = client.recv(1024).decode('utf-8')
            if message == "nickname?":
                client.send(nickname.encode('utf-8'))
            else:
                print(message)
        except:
            print('Error!')
            client.close()
            break


# Send messages to other clients through the server
def client_send():
    while True:
        message = f'{nickname}: {input("")}'
        client.send(message.encode('utf-8'))


# Create 2 threads per client: one for receiving messages and one for sending
receive_thread = threading.Thread(target=client_receive)
receive_thread.start()
send_thread = threading.Thread(target=client_send)
send_thread.start()

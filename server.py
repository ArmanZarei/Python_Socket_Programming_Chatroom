import threading
import socket



host = '127.0.0.1' 
port = 4444

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = {}

def broadcast(msg):
    for client in clients:
        client.send(msg)


def handle(client):
    while True:
        try:
            message = client.recv(1024)
            message = nicknames[client] + " : " + message.decode()
            broadcast(message.encode())
        except:
            nickname = nicknames.pop(client)
            clients.remove(client)
            client.close()
            broadcast(f"{nickname} left the chat!".encode())
            break


def receive():
    while True:
        client, address = server.accept()
        print(f"New connection with address: {address}")

        nickname = client.recv(1024).decode()

        clients.append(client)
        nicknames[client] = nickname

        print(f"Connection with address {address} chose \"{nickname}\" as it's nickname")

        broadcast(f"{nickname} joined the chat.".encode())

        client.send("Connected to the server!".encode())

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


print("Server is listening...")
receive()
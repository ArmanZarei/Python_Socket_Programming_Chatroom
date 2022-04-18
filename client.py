import socket
import threading

nickname = input("Nickname: ")

server_host = '127.0.0.1' 
server_port = 4444

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((server_host, server_port))


def receive():
    while True:
        try:
            message = client.recv(1024).decode()
            print(message)
        except:
            print("An error occurred!")
            client.close()
            break


def write():
    while True:
        message = input().encode()
        client.send(message)


client.send(nickname.encode())
threading.Thread(target=receive).start()
threading.Thread(target=write).start()

import socket
import threading

host = '127.0.0.1'
port = 65432
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen()

clients = []
nicknames = []

def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            msg = message = client.recv(1024)
            if msg.decode('ascii').startswith('/kick'):
                if nicknames[clients.index(client)] == "admin":
                    msg_to_kick = msg.decode('ascii')[6:]
                    kick_user(msg_to_kick)
                else:
                    client.send("Commands can only be used by the admin!".encode('ascii'))  
            elif msg.decode('ascii').startswith('/ban'):
                 if nicknames[clients.index(client)] == "admin":
                    msg_to_ban = msg.decode('ascii')[4:]
                    kick_user(msg_to_ban)
                    with open('banned.txt', 'a') as f:       
                        f.write(f'{msg_to_ban}\n')
                    print(f'{msg_to_ban} was banned!')
                    pass
                 else:
                    client.send("Commands can only be used by the admin!".encode('ascii'))
            else:
                broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} left the chat!'.encode('ascii'))
            nicknames.remove(nickname)
            break


def receive():
    while True:
        client, address = server_socket.accept()
        print(f'Connected with {str(address)}')

        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        with open('banned.txt', 'r') as f:
            banned_list = f.readlines()

        if f'{nickname}\n' in banned_list:
            client.send('You are banned from this server!'.encode('ascii'))
            client.close()
            continue

        if nickname == "admin":
            client.send("PASS".encode('ascii'))
            password = client.recv(1024).decode('ascii')
            if password != "adminpass":
                client.send("REFUSE".encode('ascii'))
                client.close()
                continue

        nicknames.append(nickname)
        clients.append(client)

        print(f'Nickname of the client is {nickname}!')
        broadcast(f'{nickname} joined the chat!'.encode('ascii'))
        client.send('Connected to the server!'.encode('ascii'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

def kick_user(nickname):
    if nickname in nicknames:
        index = nicknames.index(nickname)
        client_to_kick = clients[index]
        clients.remove(client_to_kick)
        client_to_kick.send('You were kicked by the admin!'.encode('ascii'))
        client_to_kick.close()
        nicknames.remove(nickname)
        broadcast(f'{nickname} was kicked by the admin!'.encode('ascii'))

print('Server is listening...')
receive()
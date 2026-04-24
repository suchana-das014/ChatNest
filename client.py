import socket
import threading

stop_thread = False
nickname = input("Choose your nickname: ")

if nickname == "admin":
    password = input("Enter the admin password: ")
    if password != "adminpass":
        print("Wrong password!")
        exit()

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('127.0.0.1', 65432))

def receive():
    while True:
        global stop_thread
        if stop_thread:
            break
        try:
            message = client_socket.recv(1024).decode('ascii')
            if message == 'NICK':
                client_socket.send(nickname.encode('ascii'))
                next_message = client_socket.recv(1024).decode('ascii')
                if next_message == 'PASS':
                    client_socket.send(password.encode('ascii'))
                    if client_socket.recv(1024).decode('ascii') == 'REFUSE':
                       print("Connection refused by the server!")
                       stop_thread = True
                elif next_message == 'BAN':
                    print("You are banned from this server!")
                    client_socket.close()
                    stop_thread = True
            else:
                print(message)
        except:
            print("An error occurred!")
            client_socket.close()
            break

def write():
    while True:
        if stop_thread:
            break
        message = f'{nickname}: {input("")}'
        if message[len(nickname)+2:].startswith('/'):
            if nickname == "admin":
                if message[len(nickname)+2:].startswith('/kick'):
                    target_nickname = message[len(nickname)+2+6:]
                    client_socket.send(f'KICK {target_nickname}'.encode('ascii'))
                elif message[len(nickname)+2:].startswith('/ban'):
                    target_nickname = message[len(nickname)+2+5:]
                    client_socket.send(f'BAN {target_nickname}'.encode('ascii'))
            else:
                print("Commands can only be used by the admin!")
        client_socket.send(message.encode('ascii'))

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
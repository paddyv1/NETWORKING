import socket
import sys
HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def message_server(msg):
    message_to_send = msg.encode(FORMAT)
    msg_length = len(message_to_send)
    msg_to_send = str(msg_length).encode(FORMAT)
    msg_to_send += b' ' * (HEADER - len(msg_to_send)) + message_to_send
    client.send(msg_to_send)

def server_reply(temp_client):
    msg_length = temp_client.recv(HEADER).decode(FORMAT)
    length_to_read = int(msg_length)
    actual_message = temp_client.recv(length_to_read).decode(FORMAT)
    return actual_message

#message_server("Hello World!")
#input()
#message_server("Hello Everyone!")
#input()
#message_server("Hello Tim!")

#message_server(DISCONNECT_MESSAGE)
connected = False
authorised = True
while authorised:

    msg = input(">>>>Please enter a username: ")
    message_server(msg)
    server_msg = server_reply(client)
    print(f">>>>{server_msg}")
    if server_msg == "Valid User":
        connected = True
        server_msg = server_reply(client)
        print(f">>>>{server_msg}")
        authorised = False
    elif server_msg == "END":
        print(">>>>Exiting the program.")
        sys.exit()
    else:
        print(">>>>Not a valid user.")


print ("OUT")

while connected:
    msg = input(">>>>")
    message_server(msg)
    server_msg_2 = server_reply(client)
    print(server_msg_2)

    if server_msg_2 == "END":
        sys.exit()
    if server_msg_2 == "DONE":
        print("Order Complete")
        sys.exit()

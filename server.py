


import socket
import threading
import sys

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)



#VERIFIED USERNAMES
USERS = ['Robyn', 'Nirmal', 'Amaar', 'Patrick']


menu = {'Starter': ['Garlic Bread', 'Dough balls', 'Chicken wings'],
        'Main': ['Pizza', 'Burger', 'Pasta'],
        'Side': ['Fries', 'Salad', 'Rice']}

#ALL THE ORDERS OF CURRENT USERS
orders = {}


def ORDR(user_name, order_list):
    if user_name not in orders.keys():
        orders[user_name] = order_list
    elif user_name in orders.keys():
        for x in order_list:
            orders[user_name].append(x)

def PKUP(user_name):
    p = ''
    counter = 0
    for x in orders[user_name]:
        temp = str(counter)
        p += temp + " : " + x + "\n"
        counter += 1
    return p



def client_response(conn):
    msg_length = conn.recv(HEADER).decode(FORMAT)
    if msg_length:
        length_to_read = int(msg_length)
        actual_message = conn.recv(length_to_read).decode(FORMAT)
        return actual_message

def message_client(connection, msg):
    send_message = msg.encode(FORMAT)
    msg_length = len(send_message)
    send_msg = str(msg_length).encode(FORMAT)
    send_msg += b' ' * (HEADER - len(send_msg)) + send_message
    connection.send(send_msg)



def confirm_user(user):
    for i in USERS:
        if user == i:
            return True

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")


    order = False
    connected2 = False
    connected1 = False
    connected = True
    while connected:


        client_message = client_response(conn)
        print(f"[{addr}] {client_message}")

        if confirm_user(client_message):
            print ("Is a user")
            text = "Valid User"
            message_client(conn, text)
            connected1 = True
        elif client_message == "END":
            print ("Exit")
            text = "END"
            message_client(conn, text)
            connected = False

        else:
            text = "Incorrect Username"
            message_client(conn, text)


        while connected1:
            customer = client_message

            msgg = "NEW for new customer, OLD to pick up, and END to terminate"
            message_client(conn, msgg)
            print(f"Waiting for request from the customer")
            new_message = client_response(conn)
            print(f"client sent {new_message}")

            if new_message.upper() == "NEW":
                print ("New order has been chosen")
                #text = "New order has been chosen"
                #message_client(conn, text)
                connected2 = True
            elif new_message.upper() == "OLD":
                print ("Pick up an old order has been selected")
                if customer in orders.keys():
                    to_send = f"{customer} can pick up the order using PKUP command."
                    message_client(conn, to_send)

                    pick_up = True
                    while pick_up:
                        msg = client_response(conn)
                        if msg.upper() == "PKUP":
                            ready_order = PKUP(customer) + "\n Thank you for ordering!"
                            message_client(conn, ready_order)
                            pick_up = False
                            sys.exit()
                        elif msg.upper() == "END" or msg.upper() == "end":
                            conn.send("END".encode(FORMAT))
                            connected = False
                        else:
                            to_send = "You can only use PKUP command"
                            message_client(connection, to_send)

                else:
                    to_send = "You haven't ordered"
                    message_client(connection, to_send)

            elif new_message.upeer() == "END":
                print ("Exiting the program")
                text = "END"
                message_client(conn, text)
                connected=False
                connected1=False


            function1 = False
            while connected2:
                msgg = "Enter either MENU to view the menu or ORDR to create an new order"
                message_client(conn, msgg)
                print(f"Waiting for request from the customer")

                new_message = client_response(conn)
                print(f"client sent {new_message}")

                if new_message.upper() == "MENU" or new_message.upper() == "ORDR":
                    function1 = True


                elif new_message.upper() == "END":
                    text="END"
                    message_client(conn, text)
                    connected2 = False
                    connected1 = False
                    connected = False


                while function1:
                    if new_message.upper() == "MENU":
                        menu_formatted = ''
                        counter = 1
                        for key in menu:
                            menu_formatted += key + "\n"
                            for x in menu[key]:
                                temp = str(counter)
                                menu_formatted += "\t" + temp + " : " + x + "\n"
                                counter += 1
                        print ("The menu has been shown")
                        text = menu_formatted
                        message_client(conn, text)
                        function1 = False
                    else:
                        if new_message.upper() == "ORDR":
                            print(f"{customer} has started a new order")
                            incorrect_starter = True
                            while incorrect_starter:
                                to_send = "Enter your STARTER from the menu or none, please"
                                message_client(conn, to_send)
                                starter = client_response(conn)
                                print(starter)
                                if starter == "none" or starter == "NONE":
                                    incorrect_starter = False
                                elif starter not in menu['starter']:
                                    incorrect_starter = True
                                elif starter in menu['starter']:
                                    incorrect_starter = False

                            incorrect_main = True
                            while incorrect_main:
                                to_send = "Enter your MAIN from the menu or none, please"
                                message_client(conn, to_send)
                                main = client_response(conn)
                                print(main)
                                if main == "none" or main == "NONE":
                                    incorrect_main = False
                                elif main not in menu['main']:
                                    incorrect_main = True
                                elif main in menu['main']:
                                    incorrect_main = False

                            incorrect_side = True
                            while incorrect_side:
                                to_send = "Enter your SIDE from the menu or none, please"
                                message_client(conn, to_send)
                                side = client_response(conn)
                                if side == "none" or side == "NONE":
                                    incorrect_side = False
                                elif side not in menu['side']:
                                    incorrect_side = True
                                elif side in menu['side']:
                                    incorrect_side = False

                            order_list = [starter, main, side]
                            ORDR(customer, order_list)

                            to_send = "DONE"
                            message_client(conn, to_send)
                            connected = False
                            fucntion1 = False
                            print(f"[CLOSED] CONNECTION WITH {customer} CLOSED")
                            sys.exit()

















    conn.close()


def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


print("[STARTING] server is starting...")
start()

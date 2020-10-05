from socket import *


def start_server():
    welcome_socket = socket(AF_INET, SOCK_STREAM)
    welcome_socket.bind(("", 5678))
    welcome_socket.listen(1)
    connection_socket, client_address = welcome_socket.accept()
    #print(client_address)
    communication_continue = True
    while communication_continue:
        response = connection_socket.recv(100).decode()
        if response == "game over":
            communication_continue = False
        else:
            print(response)

    connection_socket.close()
    welcome_socket.close()
    pass


if __name__ == "__main__":
    start_server()

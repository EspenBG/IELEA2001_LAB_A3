from socket import *

HOST = "localhost"
PORT = 5678
client_socket = None    # type: socket


def connect_to_server(host, port):
    connection_established = False
    global client_socket

    try:
        client_socket = socket(AF_INET, SOCK_STREAM)
        client_socket.connect((host, port))
        #client_socket.connect((host, port))
        connection_established = True
    except IOError as e:
        print("Error happened: ", e)
    finally:
        return connection_established


def disconnect_form_server():
    global client_socket
    try:
        client_socket.close()
        pass
    except IOError:
        pass
    except AttributeError as e:
        print('ERROR: ', e)
        pass


if __name__ == '__main__':
    test = connect_to_server(HOST, PORT)
    print(test)
    message = "hellog"
    client_socket.send(message.encode())
    client_socket.send(message.encode())
    client_socket.send(message.encode())
    client_socket.send(message.encode())
    client_socket.send(message.encode())
    client_socket.send(message.encode())
    client_socket.send(message.encode())
    client_socket.send("game over".encode())

    disconnect_form_server()

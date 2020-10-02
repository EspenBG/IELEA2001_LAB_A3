from socket import *

HOST = "datakomm.work"
PORT = 1301
client_socket = None    # type: socket


def connect_to_server(host, port):
    connection_established = False
    global client_socket

    try:
        client_socket = socket(AF_INET, SOCK_STREAM)
        # client_socket.connect((host, port))
        client_socket.connect((host, port))
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
    # test = connect_to_server()
    # print(test)
    # disconnect_form_server()
    test = None
    if test is not None:
        print("tyr")
    else:
        print("MMMMM;")
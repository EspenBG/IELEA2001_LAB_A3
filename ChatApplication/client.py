#################################################################################
# A Chat Client application. Used in the course IELEx2001 Computer networks, NTNU
#################################################################################
import threading
import time
from socket import *
pass

# --------------------
# Constants
# --------------------
# The states that the application can be in
states = [
    "disconnected",  # Connection to a chat server is not established
    "connected",  # Connected to a chat server, but not authorized (not logged in)
    "authorized"  # Connected and authorized (logged in)
]
TCP_PORT = 1300  # TCP port used for communication
SERVER_HOST = "datakomm.work"  # Set this to either hostname (domain) or IP address of the chat server
SYNC_MODE = False   # Set this to true to use synchronous mode
EXTERNAL_VIEWER = True  # Can not be used along with synchronous mode

# --------------------
# State variables
# --------------------
current_state = "disconnected"  # The current state of the system
# When this variable will be set to false, the application will stop
must_run = True
# Use this variable to create socket connection to the chat server
# Note: the "type: socket" is a hint to PyCharm about the type of values we will assign to the variable
client_socket = None  # type: socket
terminal_socket = None  # type: socket
user_socket = None  # type: socket

server_thread = None # type: threading.Thread
messages_thread = None  # type: threading.Thread
users_thread = None  # type: threading.Thread

message_to_terminal = []
message_from_server = []
user_message = []
message_sent = []


def send_to_terminal():
    global terminal_socket
    global must_run
    global message_to_terminal

    terminal_socket = socket(AF_INET, SOCK_STREAM)
    terminal_socket.connect(("localhost", 8001))
    terminal_socket.send("Connected\n".encode())

    while must_run:
        # Array not empty
        if len(message_to_terminal) != 0:
            # print first meassage in array
            message = message_to_terminal[0].__str__() + "\n"
            terminal_socket.send(message.encode())
            message_to_terminal.pop(0)

            #terminal_socket.send("while".encode())
        else:
            time.sleep(0.5)
        pass

def update_users():
    global must_run
    global user_socket

    user_socket = socket(AF_INET, SOCK_STREAM)
    user_socket.connect(("localhost", 8002))
    user_socket.send("Connected\n".encode())

    while must_run:
    # user_socket.send("while".encode())
        time.sleep(1)
        pass
    pass

def continuous_server_response():
    global must_run
    global client_socket
    global current_state
    global message_to_terminal
    global message_sent

    try:
        while must_run and current_state != "disconnected":
            #print("fff")
            server_response = get_servers_response()
            if server_response == "loginok":
                # TODO: Add logged in as: ...
                message_to_terminal.append("Login successful")
            else:
                #print(server_response)
                command, message = server_response.split(maxsplit=1)
                #print(command,message)
                if "msgok" in command:
                    # TODO get the last message sent
                    # TODO: print the correct message...

                    message = "You: " + message_sent[0]
                    message_to_terminal.append(message)
                    message_sent.pop(0)

                elif "msg" in command:
                    username, message = message.split(maxsplit=1)
                    if "privmsg" in command:
                        message = username + " to you: " + message
                        message_to_terminal.append(message)
                    else:
                        message = username + " to all: " + message
                        message_to_terminal.append(message)


                    pass
                pass

                elif "modeok" in command:
                    #TODO: return mode ok to selector in connection
                    message_to_terminal.append("ERROR: mode not switched")

                elif "loginerr" in command:
                    #TODO send an error to terminal 1
                    message_to_terminal.append(message)

                elif "users" in command:
                    all_users = message.split()
                    all_users = all_users[0:]
                    user_message = all_users

                    # print("The following users are online: ")
                    # for user in all_users:
                    #     #TODO: send to terminal 2
                    #     print(user)

                elif "joke" in command:
                    print(message)

    except ConnectionAbortedError:
        pass


def quit_application():
    """ Update the application state so that the main-loop will exit """
    # Make sure we reference the global variable here. Not the best code style,
    # but the easiest to work with without involving object-oriented code
    global must_run
    global EXTERNAL_VIEWER

    must_run = False



def send_command(command, arguments):
    """
    Send one command to the chat server.
    :param command: The command to send (login, sync, msg, ...(
    :param arguments: The arguments for the command as a string, or None if no arguments are needed
        (username, message text, etc)
    :return:
    """
    global client_socket

    # There are some commands that dont have any arguments
    message_to_send = command
    if arguments is not None:
        message_to_send += " "
        message_to_send += arguments

    message_to_send += "\n"     # the "\n" character is used as the end of the statement.
    message_encoded = message_to_send.encode()
    # send the encoded message to the server
    client_socket.send(message_encoded)
    pass


def read_one_line(sock):
    """
    Read one line of text from a socket
    :param sock: The socket to read from.
    :return:
    """
    newline_received = False
    message = ""
    while not newline_received:
        character = sock.recv(1).decode()
        if character == '\n':
            newline_received = True
        elif character == '\r':
            pass
        else:
            message += character
    return message


def get_servers_response():
    """
    Wait until a response command is received from the server
    :return: The response of the server, the whole line as a single string
    """
    # TODO FINAL: Clean up function and refactor code
    global client_socket
    # Hint: reuse read_one_line (copied from the tutorial-code)
    message_from_server = ""
    while message_from_server == "":
        message_from_server = read_one_line(client_socket)

    return message_from_server


def connect_to_server():
    """
    Connects the program to the chat-server specified in the constants at the top
    Also switches the mode of the connection to synchronous mode if SYNC_MODE constant is set
    :return
    """
    # Must have these two lines, otherwise the function will not "see" the global variables that we will change here
    global client_socket
    global current_state
    global terminal_socket
    global EXTERNAL_VIEWER
    global SYNC_MODE
    global server_thread
    global messages_thread
    global users_thread

    # Creates a socket and connects to the sever, prints an error message if it occurs an IO-error.
    try:
        client_socket = socket(AF_INET, SOCK_STREAM)
        client_socket.connect((SERVER_HOST, TCP_PORT))
        connection_established = True

    except IOError as e:
        print('ERROR Connecting to server: ', e)
        connection_established = False

    # Switch to the desired running mode of the communication
    if connection_established:
        current_state = "connected"
        if SYNC_MODE:   # The Server is running async by default
            send_command('sync', None)
            if not EXTERNAL_VIEWER:
                response = get_servers_response()
                if response != "modeok":
                    print("ERROR: mode not switched")
                else:
                    print("Running in synchronous mode")
        else:
            # Uncomment the lines below to have the possibility activate sync mode.
            # send_command('async', None)
            # response = get_servers_response()
            pass

    if EXTERNAL_VIEWER:

        server_thread = threading.Thread(name="server_thread", target=continuous_server_response, args=())
        messages_thread = threading.Thread(name="messages_thread", target=send_to_terminal, args=())
        users_thread = threading.Thread(name="users_thread", target=update_users, args=())

        server_thread.start()
        messages_thread.start()
        users_thread.start()
    pass


def disconnect_from_server():
    """
    Disconnect from the server and change the status if done successfully.
    :return:
    """
    # Must have these two lines, otherwise the function will not "see" the global variables that we will change here
    global client_socket
    global current_state
    global EXTERNAL_VIEWER

    # Close the socket and print the error if one occur
    try:
        client_socket.close()
        client_closed = True

    except IOError as e:
        print('ERROR closing to server: ', e)
        client_closed = False

    except AttributeError as e:
        # AttributeError is when is is not possible to use the close command, i.e. if client_socket == None
        # this means the socket is already closed
        print('ERROR closing to server: ', e)
        client_closed = True

    if client_closed:
        current_state = "disconnected"
    pass


def authorize():
    """
    Allows the user to authorize (login) to the server with a given username,
    and changes the sate of the system to "authorized" if authorization is successful.
    Prints the error message returned from the server, if there is one
    :return:
    """
    global current_state
    global EXTERNAL_VIEWER

    username = input('Enter username: ')
    command = "login"
    send_command(command, username)
    if not EXTERNAL_VIEWER:
        response = get_servers_response()
        if "loginerr" in response:
            print(response)
        else:
            current_state = "authorized"
    pass


def send_public_message():
    """
    Sends a public message to the server.
    :return:
    """
    global EXTERNAL_VIEWER
    global message_sent

    command = "msg"
    message = input("Message: ")
    send_command(command, message)
    message_sent.append(message)

    if not EXTERNAL_VIEWER:
        response = get_servers_response()
        if "msgok" in response:
            print("You: ", message)
        else:
            print(response)
    pass


def send_private_message():
    """
    Sends a private message to a user.
    :return:
    """
    global EXTERNAL_VIEWER
    global message_was_sent

    command = "privmsg"
    username = input("To: ")    # The users specify the user to receive the message
    message = username + " " + input("Message: ")   # The users specify the message to send
    send_command(command, message)

    if not EXTERNAL_VIEWER:
        response = get_servers_response()
        if "msgok" in response:
            print("You to ", username, ": ", message)
        else:
            print(response)
    pass


def get_users():
    """
    Get the list of users from the server, and prints all the users in the console.
    :return:
    """
    global EXTERNAL_VIEWER

    send_command("users", None)
    if not EXTERNAL_VIEWER:
        response = get_servers_response()
        if "users" in response:
            all_users = response.split()
            all_users = all_users[1:]
            print("The following users are online: ")
            for user in all_users:
                print(user)
    pass


def get_inbox():
    """
   Get all the messages from the server. And prints them in order.
   :return:
    """
    send_command("inbox", None)
    # The first response contains "inbox #" there # is the number of messages in the inbox
    if not EXTERNAL_VIEWER:
        first_line = get_servers_response().split(maxsplit=1)
        if "inbox" in first_line:

            for i in range(int(first_line[1])):
                message_type, username, message = get_servers_response().split(maxsplit=2)

                if message_type == "privmsg":
                    print(username, "to you:", message)

                else:
                    print(username, "to all:", message)
    pass


def get_joke():
    """
    Asks the server for a joke to print.
    :return:
    """
    global EXTERNAL_VIEWER

    send_command("joke", None)
    command, joke = get_servers_response().split(maxsplit=1)
    if not EXTERNAL_VIEWER:
        if command == "joke":
            print(joke)
    pass


"""
The list of available actions that the user can perform
Each action is a dictionary with the following fields:
description: a textual description of the action
valid_states: a list specifying in which states this action is available
function: a function to call when the user chooses this particular action. The functions must be defined before
            the definition of this variable
"""
available_actions = [
    {
        "description": "Connect to a chat server",
        "valid_states": ["disconnected"],
        "function": connect_to_server
    },
    {
        "description": "Disconnect from the server",
        "valid_states": ["connected", "authorized"],
        "function": disconnect_from_server
    },
    {
        "description": "Authorize (log in)",
        "valid_states": ["connected", "authorized"],
        "function": authorize
    },
    {
        "description": "Send a public message",
        "valid_states": ["connected", "authorized"],
        # Hint: ask the user to input the message from the keyboard
        # Hint: you can reuse the send_command() function to send the "msg" command
        # Hint: remember to read the server's response: whether the message was successfully sent or not
        "function": send_public_message
    },
    {
        "description": "Send a private message",
        "valid_states": ["authorized"],
        # Hint: ask the user to input the recipient and message from the keyboard
        # Hint: you can reuse the send_command() function to send the "privmsg" command
        # Hint: remember to read the server's response: whether the message was successfully sent or not
        "function": send_private_message
    },
    {
        "description": "Read messages in the inbox",
        "valid_states": ["connected", "authorized"],
        # Hint: send the inbox command, find out how many messages there are. Then parse messages
        # one by one: find if it is a private or public message, who is the sender. Print this
        # information in a user friendly way
        "function": get_inbox
    },
    {
        "description": "See list of users",
        "valid_states": ["connected", "authorized"],
        # Hint: use the provided chat client tools and analyze traffic with Wireshark to find out how
        # the user list is reported. Then implement a function which gets the user list from the server
        # and prints the list of usernames
        "function": get_users
    },
    {
        "description": "Get a joke",
        "valid_states": ["connected", "authorized"],
        # Hint: this part is not described in the protocol. But the command is simple. Try to find
        # out how it works ;)
        "function": get_joke
    },
    {
        "description": "Quit the application",
        "valid_states": ["disconnected", "connected", "authorized"],
        "function": quit_application
    },
]


def run_chat_client():
    """ Run the chat client application loop. When this function exists, the application will stop """

    while must_run:
        print_menu()
        action = select_user_action()
        perform_user_action(action)
    print("Thanks for watching. Like and subscribe! 👍")


def print_menu():
    """ Print the menu showing the available options """
    print("==============================================")
    print("What do you want to do now? ")
    print("==============================================")
    print("Available options:")
    i = 1
    for a in available_actions:
        if current_state in a["valid_states"]:
            # Only hint about the action if the current state allows it
            print("  %i) %s" % (i, a["description"]))
        i += 1
    print()


def select_user_action():
    """
    Ask the user to choose and action by entering the index of the action
    :return: The action as an index in available_actions array or None if the input was invalid
    """
    number_of_actions = len(available_actions)
    hint = "Enter the number of your choice (1..%i):" % number_of_actions
    choice = input(hint)
    # Try to convert the input to an integer
    try:
        choice_int = int(choice)
    except ValueError:
        choice_int = -1

    if 1 <= choice_int <= number_of_actions:
        action = choice_int - 1
    else:
        action = None

    return action


def perform_user_action(action_index):
    """
    Perform the desired user action
    :param action_index: The index in available_actions array - the action to take
    :return: Desired state change as a string, None if no state change is needed
    """
    if action_index is not None:
        print()
        action = available_actions[action_index]
        if current_state in action["valid_states"]:
            function_to_run = available_actions[action_index]["function"]
            if function_to_run is not None:
                function_to_run()
            else:
                print("Internal error: NOT IMPLEMENTED (no function assigned for the action)!")
        else:
            print("This function is not allowed in the current system state (%s)" % current_state)
    else:
        print("Invalid input, please choose a valid action")
    print()
    return None



# Entrypoint for the application. In PyCharm you should see a green arrow on the left side.
# By clicking it you run the application.
if __name__ == '__main__':
    run_chat_client()

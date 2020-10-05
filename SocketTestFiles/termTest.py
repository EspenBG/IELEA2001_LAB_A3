import subprocess
import threading
import socket
import time

def listenproc():
 monitorshell = subprocess.Popen("terminal --command=\"nc -l 8001\"",shell=True)

def printproc():
 print("Local message")
 time.sleep(5) # delay sending of message making sure port is listening
 sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 sock.connect(('localhost', 8001))
 sock.send("Sent message")
 time.sleep(5)
 sock.close()

listenthread = threading.Thread(name="Listen", target=listenproc, args=())
printhread = threading.Thread(name="Print", target=printproc, args=())

listenthread.start()
printhread.start()
listenthread.join()
printhread.join()

import os, socket, sys, threading, time


class Output(threading.Thread):
    def __init__(self, sock):
        threading.Thread.__init__(self)

        self.sock = sock

    def run(self):
        return_msg = self.sock.recv(1024)

        while return_msg:
            sys.stdout.write(return_msg.decode())
            return_msg = self.sock.recv(1024)

        self.sock.shutdown()
        self.sock.close()
        os._exit(0)

def client():
    if len(args) == 5:
        address, messagePort, filePort = 'localhost', args[2], args[4]
    elif len(args) == 7:
        address, messagePort, filePort = args[6], args[2], args[4]

    messageSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    messageSock.connect((address, int(messagePort)))

    messageSock.send(filePort.encode())

    time.sleep(1)

    fileSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    fileSock.connect((address, int(filePort)))

    print(fileSock.recv(1024).decode())

    output = Output(messageSock)
    output.start()

    message = sys.stdin.readline()

    while message:
        messageSock.send(message.encode())
        message = sys.stdin.readline()

    messageSock.shutdown(0)
    messageSock.close()
    os._exit(0)

def server():
    messagePort = args[2]

    messagesocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    messagesocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    messagesocket.bind(('', int(messagePort)))
    messagesocket.listen(5)
    messageSock, addr = messagesocket.accept()

    filePort = messageSock.recv(1024).decode()

    filesocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    filesocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    filesocket.bind(('', int(filePort)))
    filesocket.listen(5)
    fileSock, addr = filesocket.accept()

    print(filePort)
    fileSock.send("test".encode())

    output = Output(messageSock)
    output.start()

    message = sys.stdin.readline()

    while message:
        messageSock.send(message.encode())
        message = sys.stdin.readline()

    messageSock.shutdown(0)
    messageSock.close()
    os._exit(0)

args = sys.argv

if len(args) != 3 and len(args) != 5 and len(args) != 7:
    print("Incorrect Usage\n"
          "Server: python messenger_with_files.py -l <listening port number>\n"
          "Client: python messenger_with_files.py -l <listening port number> -p <connect server port> [-s] [connect server address]")
else:
    if len(args) == 3:
        server()
    elif len(args) == 5 or len(args) == 7:
        client()
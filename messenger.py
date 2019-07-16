import os, socket, sys, threading

class Input(threading.Thread):
    def __init__(self, sock):
        threading.Thread.__init__(self)

        self.sock = sock

    def run(self):
        message = sys.stdin.readline()

        while message:
            self.sock.send(message.encode())
            message = sys.stdin.readline()

        self.sock.shutdown()
        self.sock.close()
        os._exit(0)

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
    address, port = 'localhost', args[1]

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((address, int(port)))

    output = Output(sock)
    output.start()

    message = sys.stdin.readline()

    while message:
        sock.send(message.encode())
        message = sys.stdin.readline()

    sock.close()
    os._exit(0)

def server():
    port = args[2]

    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serversocket.bind(('', int(port)))
    serversocket.listen(5)
    sock, addr = serversocket.accept()

    output = Output(sock)

    output.start()

    serversocket.close()

    message = sys.stdin.readline()

    while message:
        sock.send(message.encode())
        message = sys.stdin.readline()

    sock.close()
    os._exit(0)

args = sys.argv

if len(args) < 2 or len(args) > 4:
    print("Incorrect Usage\n"
          "Server: py messenger.py -l <port number>\n"
          "Client: py messenger.py <port number> [<server address>]")
else:
    if args[1] == "-l":
        server()
    else:
        client()
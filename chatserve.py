import sys
import socket
import re

TEST = True


def serverAddress(argv):
    """
    Checks command line args and assigns IP and Port args to variables
    """
    if len(sys.argv) != 2:
        print >> sys.stderr, "[chatserve] ERROR! Correct format 'chatserve [port]'"
        # exit 2 for command line syntax errors
        sys.exit(2)
    ip = socket.gethostbyname(socket.gethostname())
    port = int(sys.argv[1])
    if TEST:
        print >> sys.stderr, '[DEBUG] %s:%d' % (ip, port)
    return ip, port


def socketInit():
    """
    Initializes Socket
    """
    return socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def socketBind(sock, ip, port):
    """
    Binds IP and Port to Socket
    """
    try:
        sock.bind((ip, port))
    except:
        print >> sys.stderr, '[chatserve] ERROR binding to localhost port'
        sys.exit(1)
    return sock


def socketOpen(argv):
    """
    Initialize and Bind IP and Port to Socket
    """ 
    ip, port = serverAddress(argv)
    sock = socketInit()
    sock = socketBind(sock, ip, port)
    if TEST:
        print >> sys.stderr, '[DEBUG] socket is bound'
    return sock


def socketListen(sock):
    """
    Listens on Socket Port
    """
    sock.listen(1)
    if TEST:
        print >> sys.stderr, '[DEBUG] listening for incoming connections'
    while True:
        client_connection, client_address = sock.accept()
        response = socketConnection(client_connection, client_address)
        if response == -1:
            sock.shutdown(SHUT_RDWR)
            sock.close()
            break
    return


def socketConnection(connection, address):
    """
    Establishes TCP connection with connection data and client address
    """
    try:
        if TEST:
            # print to stderr in case of output redirect
            print >> sys.stderr, 'TCP connection request from %s:%d' % (str(address[0]), address[1])
        while True:
            client_data = connection.recv(32)
            if client_data:
                print("%s" % str(client_data))
                server_data = raw_input('Server reply: ')
                server_data = 'SERVER: ' + server_data
		message_size = len(server_data)
		if TEST:
			print('[DEBUG] message size: %d' % message_size)
			print('[DEBUG] string to send: %s' % server_data)
		connection.send(str(message_size))
                connection.send(server_data)
                if re.match(r'\quit$', client_data) or re.match(r'\quit$', server_data):
                    print >> sys.stderr, 'TCP connection closing'
                    connection.close()
                    return -1
    finally:
        connection.close()
    return 0


def main(argv):
    server_sock = socketOpen(argv)
    socketListen(server_sock)
    sys.exit(0)


if __name__ == "__main__":
    main(sys.argv)


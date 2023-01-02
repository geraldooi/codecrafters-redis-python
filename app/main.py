# Uncomment this to pass the first stage
import socket
import time
from threading import Thread

from .resp_decoder import RESPDecoder

data = {}


def handleConnection(conn):
    while True:
        try:
            command, *args = RESPDecoder(conn).decode()

            if command == b"ping":
                conn.send(b"+PONG\r\n")
            elif command == b'echo':
                conn.send(b"$%d\r\n%b\r\n" % (len(args[0]), args[0]))
            elif command == b'set':
                expiry = None

                # if expiry set, store datetime of expiry
                if len(args) > 2:
                    expiry = int(time.time() * 1000) + int(args[3])

                # Set key value
                data[args[0]] = (args[1], expiry)
                conn.send(b"+OK\r\n")

            elif command == b'get':
                value, expiry = data[args[0]]

                if expiry is not None and expiry <= int(time.time() * 1000):
                    del data[args[0]]
                    conn.send(b"$-1\r\n")
                else:
                    conn.send(b"$%d\r\n%b\r\n" % (len(value), value))
            else:
                conn.send(b"-ERR unknown command\r\n")
        except ConnectionError:
            break  # stop serving if client connection closed


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)

    while True:
        conn, _ = server_socket.accept()  # wait for client
        Thread(target=handleConnection, args=(conn,)).start()


if __name__ == "__main__":
    main()

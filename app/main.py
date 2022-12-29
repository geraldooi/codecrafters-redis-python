# Uncomment this to pass the first stage
import socket
from threading import Thread

from .resp_decoder import RESPDecoder


def handleConnection(conn):
    while True:
        try:
            command, *args = RESPDecoder(conn).decode()

            if command == b"ping":
                conn.send(b"+PONG\r\n")
            elif command == b'echo':
                conn.send(b"$%d\r\n%b\r\n" % (len(args[0]), args[0]))
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

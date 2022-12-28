# Uncomment this to pass the first stage
import socket
from _thread import start_new_thread


def responseCommand(conn):
    while True:
        conn.recv(1024)  # wait for client to send data
        conn.send(b'+PONG\r\n')


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage

    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)

    while True:
        conn, _ = server_socket.accept()  # wait for client

        start_new_thread(responseCommand, (conn,))


if __name__ == "__main__":
    main()

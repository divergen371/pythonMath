# Standard Library
import socket


def telnet_server(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"Listening on {host}:{port}")
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                print(data.decode("utf-8"), end="")
                conn.sendall(data)


if __name__ == "__main__":
    telnet_server("localhost", 2323)

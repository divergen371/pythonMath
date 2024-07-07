# Standard Library
import socket
import threading


def receive_data(sock):
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                break
            print(data.decode("utf-8"), end="")
        except Exception as e:
            print(f"Error receiving data: {e}")
            break


def telnet_client(host, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            print(f"Connected to {host} on port {port}")
            # 受信用のスレッドを開始
            recv_thread = threading.Thread(target=receive_data, args=(s,))
            recv_thread.daemon = True
            recv_thread.start()

            while True:
                user_input = input("Please enter a message to send:")
                if user_input.lower() == "exit":
                    break
                s.sendall(user_input.encode("utf-8") + b"\n")
    except socket.error as e:
        print(f"Socket error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    # ローカル環境でのテストには以下を使用:
    # telnet_client('localhost', 23)
    telnet_client("example.com", 23)

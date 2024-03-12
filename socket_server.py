import socket
import urllib.parse
import logging

from mongo import add_message


def socket_server_run(ip: str, port: int):
    """
    A socket server that listens for incoming connections, receives and processes data, and sends back a response.
    It uses 'add_message' function to send the data into MongoDB
    """
    logging.info("Socket Server: starting")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ip, port))
    server_socket.listen(1)
    logging.info(f"Socket Server: started {server_socket.getsockname()}")

    try:
        while True:

            sock, address = server_socket.accept()
            logging.info(f"Socket Server: Connection established {address}")
            while True:
                received = sock.recv(1024)
                if not received:
                    break

                data_parse = urllib.parse.unquote_plus(received.decode())
                data_dict = {
                    key: value
                    for key, value in [el.split("=") for el in data_parse.split("&")]
                }
                logging.info(f"Socket Server: Data received: {data_dict}")

                add_message(data_dict["username"], data_dict["message"])

                sock.send(received)
            logging.info(f"Socket Server: connection closed {address}")
            sock.close()

    except KeyboardInterrupt:
        logging.info(f"Socket Server: Destroy server")
    finally:
        server_socket.close()


def socket_client_run(ip: str, port: int, data: str):
    """
    A socket client establishes a connection to a Socket server using the provided IP address and port number, and sends it the given data.
    Socket client receives data from HTTP srever.
    """

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        server = ip, port
        sock.connect(server)
        logging.info(f"Socket Client: Connection established {server}")
        sock.send(data)
        logging.info(f"Socket Client: Data sent: {data.decode()}")
        responce = sock.recv(1024)
        logging.info(f"Socket Client: Response data: {responce.decode()}")

    logging.info(f"Socket Client: Data transfer completed")

import multiprocessing
import logging

from socket_server import socket_server_run
from http_server import http_server_run


logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


if __name__ == "__main__":
    """
    Main function
    Runs HTTP server and Socket server
    """

    try:

        http_server = multiprocessing.Process(target=http_server_run)
        http_server.start()

        socket_server = multiprocessing.Process(
            target=socket_server_run, args=("0.0.0.0", 5000)
        )
        socket_server.start()

        http_server.join()
        socket_server.join()

    except KeyboardInterrupt:
        logging.info("HTTP server closed")
        http_server.terminate()
        logging.info("Socket server closed")
        socket_server.terminate()

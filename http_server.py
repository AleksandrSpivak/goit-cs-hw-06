import mimetypes
import pathlib
import urllib.parse
import multiprocessing
import logging

from http.server import HTTPServer, BaseHTTPRequestHandler

from socket_server import socket_client_run, socket_server_run


class HttpHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        """
        Handle the POST request by reading the data.
        Creates a socket client process @port 5000.
        """
        data = self.rfile.read(int(self.headers["Content-Length"]))

        socket_client = multiprocessing.Process(
            target=socket_client_run, args=("0.0.0.0", 5000, data)
        )
        socket_client.start()
        logging.info("HTTP Server: socket client started")

        socket_client.join()
        logging.info("HTTP Server: socket client closed")

        self.send_response(302)
        self.send_header("Location", "/")
        self.end_headers()

    def do_GET(self):
        """
        Handle the GET request.
        No parameters or return types specified.
        """
        pr_url = urllib.parse.urlparse(self.path)
        if pr_url.path == "/":
            self.send_html_file("front-init/index.html")
        elif pr_url.path == "/message":
            self.send_html_file("front-init/message.html")
        else:
            if pathlib.Path("front-init/").joinpath(pr_url.path[1:]).exists():
                self.send_static()
            else:
                self.send_html_file("front-init/error.html", 404)

    def send_html_file(self, filename, status=200):
        """
        Send an HTML file as a response with the specified status code.
        """
        self.send_response(status)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        with open(filename, "rb") as fd:
            self.wfile.write(fd.read())

    def send_static(self):
        """
        Send a static file as response.
        """
        self.send_response(200)
        mt = mimetypes.guess_type(self.path)
        if mt:
            self.send_header("Content-type", mt[0])
        else:
            self.send_header("Content-type", "text/plain")
        self.end_headers()
        with open(f"front-init/{self.path}", "rb") as file:
            self.wfile.write(file.read())


def http_server_run(server_class=HTTPServer, handler_class=HttpHandler):
    """
    Run an HTTP server @port 3000
    :return: None
    """
    server_address = ("", 3000)
    http = server_class(server_address, handler_class)
    try:
        logging.info("HTTP server starting")
        http.serve_forever()

    except KeyboardInterrupt:
        http.server_close()
        logging.info("HTTP server closed")

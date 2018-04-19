#!/usr/bin/env python
from http.server import BaseHTTPRequestHandler, HTTPServer

from job.update_job import update
from scheduler.scheduler import PeriodicScheduler


class AxeServer(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        return


def run():
    print('starting server...')

    server_address = ('127.0.0.1', 8081)
    httpd = HTTPServer(server_address, AxeServer)
    print('running server...')

    scheduler = PeriodicScheduler()
    scheduler.setup(86400, update)
    scheduler.run()

    httpd.serve_forever()


if __name__ == "__main__":
    run()

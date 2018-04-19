#!/usr/bin/env python
from http.server import BaseHTTPRequestHandler, HTTPServer

from axe_selenium_python.axe import Axe
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options

from job.update_job import update
from scheduler.scheduler import PeriodicScheduler

# HTTPRequestHandler class
class AxeServer(BaseHTTPRequestHandler):

  # GET
  def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        return

def run():
  print('starting server...')

  # Server settings
  # Choose port 8080, for port 80, which is normally used for a http server, you need root access
  server_address = ('127.0.0.1', 8081)
  httpd = HTTPServer(server_address, AxeServer)
  print('running server...')

  scheduler = PeriodicScheduler()
  scheduler.setup(86400, update)
  scheduler.run()

  httpd.serve_forever()

if __name__ == "__main__":
    run()

#!/bin/env python3

import http.server
import random
import os
import logging

CRAP_SIZE = 1024 * 1024 * 100  # 100MB
CRAP_INIT = os.urandom(CRAP_SIZE)

open_close = [('''
<SOAP-ENV:Envelope
   xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/"
   SOAP-ENV:encodingStyle=
           "http://schemas.xmlsoap.org/soap/encoding/">
      <SOAP-ENV:Body>
''','''
      </SOAP-ENV:Body>
</SOAP-ENV:Envelope>
''', 'application/soap+xml; charset=UTF-8'), ('''
{
  "status" : "success",
  "data" : {
''','''
  }
}
''', 'application/json'), ('''
<!DOCTYPE html>
<html>
<head>
<title>Page Title</title>
</head>
<body>
''','''
</body>
</html>
''', 'text/html')]

def random_response_builder(wrap_num):
    """Builds a random response with a random size."""
    size = random.randint(1, CRAP_SIZE)  # pick a crap size
    start = int(
        ((CRAP_SIZE) - size) / 2
    )  # set start point on half of the excess crap outside chosen size to slice out the center instead of from beginning
    slice_obj = slice(start, (start + size))  # create the slicer
    crap = CRAP_INIT[slice_obj]  # slice the crap
    craptastic = (
        str.encode(open_close[wrap_num][0]) + crap + str.encode(open_close[wrap_num][1])
    )  # wrap the crap in something nice
    return craptastic  # return the wrapped crap


class Handler(http.server.SimpleHTTPRequestHandler):
    """Handle http requests for the server."""

    def do_GET(self):
        """Respond to a GET request."""
        wrap_num = random.randint(0, 2)
        if self.path == "/":
            # keep load balancer happy
            output = str.encode("OK")
        else:
            output = random_response_builder(wrap_num)
        logging.error(self.headers)

        # Construct a server response.
        self.send_response(200)
        self.send_header("Content-type", open_close[wrap_num][2])
        self.end_headers()
        self.wfile.write(output)
        return

    def do_POST(self):
        """Respond to a POST request"""
        wrap_num = random.randint(0, 2)
        if self.path == "/":
            # keep load balancer happy
            output = str.encode("OK")
        else:
            output = random_response_builder(wrap_num)
        logging.error(self.headers)

        # Construct a server response.
        self.send_response(200)
        self.send_header("Content-type", open_close[wrap_num][2])
        self.end_headers()
        self.wfile.write(output)
        return


def run(server_class=http.server.ThreadingHTTPServer, handler_class=Handler):
    """Run the server."""
    print("Starting server on port 8080...")
    server_address = ("", 8080)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


run()

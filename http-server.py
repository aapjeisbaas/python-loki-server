#!/bin/env python3

import http.server
import socketserver
import random
import os
import logging

crapSize = 1024*1024*100 # 100MB 
crapInit = os.urandom(crapSize)

openClose = [('''
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

def randomResponseBuilder(wrapNum):
    size = random.randint(1,crapSize)        # pick a crap size
    start = int(((crapSize) - size) / 2)     # set start point on half of the excess crap outside chosen size to slice out the center instead of from begining
    sliceObj = slice(start, (start + size))  # create the slicer
    crap = crapInit[sliceObj]                # slice the crap
    craptastic = str.encode(openClose[wrapNum][0]) + crap + str.encode(openClose[wrapNum][1]) # wrap the crap in something nice
    return craptastic                        # return the wrapped crap

class Handler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):
        wrapNum = random.randint(0,2)
        if self.path == "/":
            # keep load balancer happy
            output = str.encode("OK")
        else:
            output = randomResponseBuilder(wrapNum)
        logging.error(self.headers)

        # Construct a server response.
        self.send_response(200)
        self.send_header('Content-type',openClose[wrapNum][2])
        self.end_headers()
        self.wfile.write(output)
        return

    def do_POST(self):
        wrapNum = random.randint(0,2)
        if self.path == "/":
            # keep load balancer happy
            output = str.encode("OK")
        else:
            output = randomResponseBuilder(wrapNum)
        logging.error(self.headers)

        # Construct a server response.
        self.send_response(200)
        self.send_header('Content-type',openClose[wrapNum][2])
        self.end_headers()
        self.wfile.write(output)
        return

def run(server_class=http.server.ThreadingHTTPServer, handler_class=Handler):
    server_address = ('', 8080)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

print('Starting server on port 8080...')
run()
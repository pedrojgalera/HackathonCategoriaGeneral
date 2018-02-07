#!/usr/bin/env python

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from config import functions_map

import json

LINK_HEADER = 'href="data:image/x-icon;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQEAYAAABPYyMiAAAABmJLR0T///////8JWPfcAAAACXBIWXMAAABIAAAASABGyWs+AAAAF0lEQVRIx2NgGAWjYBSMglEwCkbBSAcACBAAAeaR9cIAAAAASUVORK5CYII=" rel="icon" type="image/x-icon"'

class S(BaseHTTPRequestHandler):

    def __instance_api__(self, params):
        print(params)
        return functions_map[params['function'][0]]()

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('link', LINK_HEADER)
        self.send_header('Accept', 'application/json;utf-8')
        self.end_headers()

    def do_GET(self):
        #try:
        bits = urlparse(self.path)
        query=bits.query
        params=parse_qs(query)

        api = self.__instance_api__(params)
        try:
            response_json = api.__call_method__(params) # This is the general case
        except:
            response_json = api.call_method(params) # This is only for timezone google API
        self._set_headers()
        self.wfile.write(json.dumps(response_json).encode("utf-8"))

    def do_HEAD(self):
        self._set_headers()

def run(server_class=HTTPServer, handler_class=S, port=80):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print( 'Starting httpd in port '+ str(port))
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()

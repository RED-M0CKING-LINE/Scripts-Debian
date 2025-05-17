#!/bin/sh
python3 -c 'import http.server, socketserver
socketserver.TCPServer(("", 8080), http.server.SimpleHTTPRequestHandler).serve_forever()
print("port 8080")'


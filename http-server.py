#!/usr/bin/python3
import http.server, socketserver
print('Port 8080')
print('Ctrl-C to exit...')
socketserver.TCPServer(('', 8080), http.server.SimpleHTTPRequestHandler).serve_forever()


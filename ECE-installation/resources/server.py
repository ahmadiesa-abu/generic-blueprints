import sys
import http.server
import base64

from http.server import SimpleHTTPRequestHandler

key = ""

class AuthHandler(SimpleHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_AUTHHEAD(self):
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm=\"Test\"')
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        global key
        auth_header = self.headers.get('Authorization')
        if auth_header is None or not auth_header.startswith('Basic '):
            self.do_AUTHHEAD()
            self.wfile.write(b'no auth header received')
        else:
            encoded_credentials = auth_header.split(' ')[1]
            if encoded_credentials == key:
                SimpleHTTPRequestHandler.do_GET(self)
            else:
                self.do_AUTHHEAD()
                self.wfile.write(auth_header.encode('utf-8'))
                self.wfile.write(b' not authenticated')

def test(HandlerClass=AuthHandler, ServerClass=http.server.HTTPServer):
    server_address = ('', int(sys.argv[1]))
    httpd = ServerClass(server_address, HandlerClass)
    httpd.serve_forever()

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("usage script.py [port] [username:password]")
        sys.exit()

    key = base64.b64encode(sys.argv[2].encode('utf-8')).decode('utf-8')
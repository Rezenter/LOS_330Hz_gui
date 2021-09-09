import http.server
import json
from python.RequestHandler import Handler
import mimetypes

handler = Handler()

mimetypes.init()
mimetypes.add_type('text/javascript', '.js', strict=True)


def __init__():
    return


class ApplicationServer (http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        uri = self.requestline.split(' ')[1]
        if uri != '/api':
            print('Wrong API uri: {0}'.format(uri))
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(bytes(json.dumps({
                'ok': False,
                'description': 'Wrong API uri'
            }), 'utf-8'))
            return

        bodyLength = int(self.headers.get('content-length', 0))
        body = self.rfile.read(bodyLength).decode('utf-8')
        parsedBody = []
        try:
            parsedBody = json.loads(body)
        except:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b'Error 400: Not a JSON request')

        resp = handler.handle_request(parsedBody)

        #print('Sending response: ')
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(bytes(json.dumps(resp), 'utf-8'))

    def do_GET(self):
        filepath = ''
        try:
            if self.path in ("", "/"):
                filepath = "index.html"
            else:
                filepath = self.path.lstrip("/")

            f = open('html/%s' % filepath, "rb")

        except IOError:
            self.send_error(404, 'File Not Found: %s ' % filepath)

        else:
            self.send_response(200)
            #this part handles the mimetypes for you.
            mimetype, _ = mimetypes.guess_type(filepath)
            #print(mimetype)
            self.send_header('Content-type', mimetype)
            self.end_headers()
            for s in f:
                self.wfile.write(s)

if __name__ == '__main__':
    server = http.server.HTTPServer

    httpd = server(('', 8082), ApplicationServer)
    try:
        print('Serving from now. Please, open "http://localhost:8082" in any internet browser.')
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()

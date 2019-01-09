import time
from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi
import urllib

HOST_NAME = 'localhost'
PORT_NUMBER = 8081


class MyHandler(BaseHTTPRequestHandler):
    postvars = {}
    names = []

    def do_GET(self):
        self.respond({'status': 200})
    def do_POST(self):
        ctype, pdict = cgi.parse_header(self.headers['content-type'])
        if ctype == 'multipart/form-data':
            postvars = cgi.parse_multipart(self.rfile, pdict)
        elif ctype == 'application/x-www-form-urlencoded':
            length = int(self.headers['content-length'])
            postvars = urllib.parse.parse_qs(self.rfile.read(length), keep_blank_values=1)


        for key in sorted(postvars):
            self.postvars[key.decode('utf-8')] = postvars[key][0].decode("utf-8")

        if 'first_name' in self.postvars:
            self.names.append(self.postvars['first_name'])

        self.respond({'status': 200})

    def handle_http(self, status_code, path):
        self.send_response(status_code)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()

        hello = ''
        if 'first_name' in self.postvars:
            hello = '<h3>Hello {}</h3>'.format(self.postvars['first_name'])

        content = '''
        <html><head><title>Title goes here.</title></head>
        <body><p>This is a test.</p>
        {}
        <p>You accessed path: {}</p>
        <form method="post">
            <label>Name:</label>
            <input type="text" name="first_name" />
            <input type="submit" value="Send" />
        </form>
        '''.format(hello, path)

        for n in self.names:
            content += n + '<br />'

        content += '''
        </body></html>
        '''
        return bytes(content, 'UTF-8')

    def respond(self, opts):
        response = self.handle_http(opts['status'], self.path)
        self.wfile.write(response)


if __name__ == '__main__':
    server_class = HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print(time.asctime(), 'Server Starts - %s:%s' % (HOST_NAME, PORT_NUMBER))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print(time.asctime(), 'Server Stops - %s:%s' % (HOST_NAME, PORT_NUMBER))

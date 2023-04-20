from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib import parse
from threading import Thread
import json
import os
import uuid

outputFolder = 'results'
restEndpoint = '/asyncservice'
port = 8000

def your_function(input):
    output = 'sample' # replace this line with something like output = yourFunction(input)
    return output 

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

def threaded_function(input, filePath):
    try:
        output = your_function(input) 
        
        with open(filePath, 'w', encoding='utf-8') as f:
            f.write(output)
    except Exception as exc:
        print('Error recorded on ' + filePath + ': ' + str(exc))
        with open(filePath, 'w', encoding='utf-8') as f:
            f.write(json.dumps({"error": str(exc)}))

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            path = parse.urlsplit(self.path).path
            if path == restEndpoint:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                input = post_data.decode('utf-8')
                id = str(uuid.uuid4())
                filePath = os.path.join(__location__, outputFolder + '/' + id + '.data')
                os.makedirs(os.path.dirname(filePath), exist_ok=True)
                open(filePath, 'x').close()
                thread = Thread(target=threaded_function, args = (input, filePath))
                thread.start()
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(bytes(json.dumps({"id": id}), 'utf8'))
            else:
                raise Exception('invalid path: ' + path)
            
        except Exception as exc:
            print(exc)
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(bytes(json.dumps({"error": str(exc)}), 'utf8'))

    def do_GET(self):
        try:
            path = parse.urlsplit(self.path).path
            id = parse.parse_qs(parse.urlsplit(self.path).query).get('id', [])
            if len(id) == 0:
                raise Exception('missing id argument')
            id = id[0]
            if path == restEndpoint:
                filePath = os.path.join(__location__, outputFolder + '/' + id + '.data')
                if not os.path.isfile(filePath) : 
                    raise Exception('The job with id ' + id + ' do not exist')
                with open(filePath, 'r') as file:
                    output = file.read()
                    if output == '': 
                        raise Exception('The job with id ' + id + ' is not yet completed')
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(bytes(output, 'utf8'))
            else:
                raise Exception('invalid path ' + path)
            
        except Exception as exc:
            print(exc)
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(bytes(json.dumps({"error": str(exc)}), 'utf8'))

with HTTPServer(('', port), handler) as server:
    server.serve_forever()
#!/usr/bin/env python3
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

#A good commands are:
# python3 httpclient.py GET http://httpbin.org/get
# python3 httpclient.py GET http://google.com/hello


import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib.parse 

def help():
    print("httpclient.py [GET/POST] [URL]\n")

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    def get_host_port_path(self,url):
        #get the host and port from a given url
        parsed_url = urllib.parse.urlsplit(url)
        host = parsed_url.hostname
        port = parsed_url.port
        path = parsed_url.path
        if port is None: port = 80
        if (not path) or path == None: path = "/"

        return host, port, path


    #done
    def connect(self, host, port):
        print(f"Connecting to: Host: {host} Port: {port}")
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        return None

    def get_code(self, data):
        return None

    def get_headers(self,data):
        return None

    def get_body(self, data):
        return None
    
    #done
    def sendall(self, data):
        self.socket.sendall(data.encode('utf-8'))
        
    #done
    def close(self):
        self.socket.close()

    # read everything from the socket
    #done
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return buffer.decode('utf-8')

    def GET(self, url, args=None):
        code = 500
        body = ""
        host, port, path = self.get_host_port_path(url)
        self.connect(host, port)

        request = f"GET {path} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
        print(f"Request: {repr(request)}")
        self.sendall(request)

        response = self.recvall(self.socket)
        print(f"Response: {response}")

        self.close()
        return HTTPResponse(code, body)

    def POST(self, url, args=None):
        code = 500
        body = ""
        return HTTPResponse(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        print("opt1")
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print("opt2")
        print(client.command( sys.argv[2], sys.argv[1] ))
    else:
        print("opt3")
        print(client.command( sys.argv[1] ))

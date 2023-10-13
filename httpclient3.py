#!/usr/bin/env python3
# coding: utf-8
# Copyright 2016 Abram Hindle, Gabriel Giang, https://github.com/tywtyw2002, and https://github.com/treedust
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

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib.parse

# http://127.0.0.1:27618/abcdef/gjkd/dsadas
# curl -v -X GET http://127.0.0.1:8080/wiki?CommonLispHyperSpec

def help():
    print("httpclient.py [GET/POST] [URL]\n")

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    #def get_host_port(self,url):

    def connect(self, host, port):
        # print("\nCONNECTING")
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.socket.connect((host, port))

        # return self.socket
        # print("\nFINISHED CONNECTING")
        return None

    def get_code(self, data):
        # print("\nget_code")
        # print(data)
        data_lines = data.split("\r\n")
   
        code = (data_lines[0].split()[1])
        # print("Code is:", code)
        return int(code)

    def get_headers(self,data):
        # data_lines = data.split("\r\n")
        # print("\nget_headers")

        # data_lines = data.split('\r\n')
        # print(data_lines)

        # index = data_lines.index("")

        # header_array = []
        # for i in range(0, index):
        #     header_array.append(data_lines[i])

        # print(header_array)
        # print("Header")
        # print("\r\n".join(header_array))
        # header = "\r\n".join(header_array)

        data_lines = data.split('\r\n\r\n')
        header = data_lines[0]
        # return data_lines[0]
        return header

    def get_body(self, data):
        # print("\nget_body")

        # data_lines = data.split('\r\n')
        # print(data_lines)

        # index = data_lines.index("")

        # body_array = []
        # for i in range(index+1, len(data_lines)):
        #     body_array.append(data_lines[i])

        # print(body_array)

        # print("Body")
        # print("\r\n".join(body_array))

        # body = "\r\n".join(body_array)

        data_lines = data.split('\r\n\r\n')
        body = data_lines[1]
        return body
    
    def sendall(self, data):
        # print("SENT DATA")
        self.socket.sendall(data.encode('utf-8'))
        
    def close(self):
        self.socket.close()

    # read everything from the socket
    def recvall(self, sock):
        # print("READING THE DATA")
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        
        # print("FINISHED READING DATA")
        return buffer.decode('utf-8')

    def GET(self, url, args=None):
        code = 500
        body = ""
        # URL contains host, port as well as path
        # print("GET METHOD", url)
        # print("ARGUMENT", args)
        url_parsed = urllib.parse.urlparse(url)

        host = url_parsed.hostname
        port = url_parsed.port 
        path = url_parsed.path

        if (url_parsed.port):
            pass
        else:
            port = 80

        query_params = url_parsed.query
        # print(query_params)
        # print(urllib.parse.urlencode(query_params))

        # print(host, url)

        # if host == None:
        #     host = url

        if path == "":
            path = "/"

        # print("HOST:", host, "PORT:", port, "PATH:", path, "QUERY PARAMS", query_params)
    

        # query_params = "" # Could be a potential test.
        # args = "$#&%(#&%@(#$&%(I*&$@"
        if args:
            # print("ARGUMENTS FOUND")
            query_params = urllib.parse.urlencode(args)
            path = path + "?" + query_params # To keep or not
            print(path)

        
        # print("HOST:", host, "PORT:", port, "PATH:", path, "QUERY PARAMS", query_params)

        self.connect(host,port)

        # request = f"GET {path} HTTP/1.1\r\nHost: {host}\r\nContent-type: application/x-www-form-urlencoded\r\nContent-Length: {len(query_params)}\r\nConnection: close\r\n\r\n" + query_params
        request = f"GET {path} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n" + query_params
        
        self.sendall(request)

        response_data = self.recvall(self.socket) # HTTP Response Header

        self.close() # Close the socket

        code = self.get_code(response_data)

        # header = self.get_headers(response_data)

        body = self.get_body(response_data)
        print(body + "\n")
        return HTTPResponse(code, body)

    def POST(self, url, args=None):
        code = 500
        body = ""
        

        url_parsed = urllib.parse.urlparse(url)

        host = url_parsed.hostname
        port = url_parsed.port
        path = url_parsed.path 

        if (url_parsed.port):
            pass
        else:
            port = 80

        # print(host, port, path)
    
        if path == "":
            path = "/"

        # if host == None:
        #     host = url

        self.connect(host,port)

        post_content = ""
        if args:
            post_content = urllib.parse.urlencode(args)
            # print("POST CONTENT:", post_content)
        
        # print("ARG TEST", args)

        request = f"POST {path} HTTP/1.1\r\nHost: {host}\r\nContent-Type: application/x-www-form-urlencoded\r\nContent-Length: {len(post_content)}\r\nConnection: close\r\n\r\n" + post_content

        # request = request + post_content
        
        # print("\nREQUEST")
        # print(request)

        self.sendall(request)
        
        response_data = self.recvall(self.socket)

        self.close()

        code = self.get_code(response_data)
        body = self.get_body(response_data)
        

        # print("HEADER \n")
        # print(self.get_headers(response_data))

        # print("BODY starts here")

        # print(body + "  \n")

        return HTTPResponse(code, body)

    def command(self, url, command="GET", args=None):
        # print("URL:", url, "Command:", command)
        if (command == "POST"):
            # print("POST REQ")
            return self.POST( url, args )
        else:
            # print("GET REQ")
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        # print("TEST1: sys.argv[2] =", sys.argv[2], "sys.argv[1] =", sys.argv[1])
        print(client.command( sys.argv[2], sys.argv[1] ))
    else:
        # print("TEST2: sys.argv[1] =", sys.argv[1])
        print(client.command( sys.argv[1] ))
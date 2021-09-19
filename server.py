#  coding: utf-8 
import socketserver
import os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
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
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):

    def successful_send(self, res, format):
        self.request.send("HTTP/1.1 200 OK \n".encode())
        self.request.send(("Content-type: text/%s \n"%format).encode())
        self.request.sendall(res.encode())

    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        #print ("Got a request of: %s\n" % self.data)

        '''
        The data string is:  GET / HTTP/1.1
        Accept-Encoding: identity
        Host: 127.0.0.1:8080
        User-Agent: Python-urllib/3.8
        Connection: close
        '''

        data_string = self.data.decode()
        #print("###################")
        #print("The data string is: ", data_string)
        #print("###################")

        assert (data_string != None), ("HTTP/1.1 400 Bad Request \n".encode())
        http_method, path = (data_string.split()[0], data_string.split()[1])
        print(http_method, 'and', path)

        real_path = os.getcwd() + "/www"
        if http_method == "GET":
            if os.path.realpath(real_path + path).startswith(real_path):
                if os.path.exists(real_path) and path.endswith("/"):
                    resource = open(real_path + "/index.html").read()
                    format = "html"
                    self.successful_send(resource, format)

                elif os.path.exists(real_path + path) and path.endswith(".html"):
                    resource = open(real_path + path).read()
                    self.successful_send(resource, format="html")

                elif os.path.exists(real_path + path) and path.endswith(".css"):
                    resource = open(real_path + path).read()
                    self.successful_send(resource, format="css")

                else:
                    try:
                        resource = open(real_path + path + "/index.html")

                        self.request.send("HTTP/1.1 301 Moved Permanently \n".encode())
                        self.request.sendall(("HTTP://127.0.0.1:8080" + path + "\n").encode())
                    except:
                        self.request.send("HTTP/1.1 404 Not Found \n".encode())
                
            else:
                self.request.send("HTTP/1.1 404 Not Found \n".encode())

        else:
            self.request.send("HTTP/1.1 405 Method Not Allowed \n".encode())

        self.request.sendall(bytearray("OK",'utf-8'))

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()

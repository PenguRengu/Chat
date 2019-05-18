"""
server.py
created on 5/17/2019
"""
### Imports
from socketserver import BaseRequestHandler, TCPServer

### Variable
messages = []

### Classes
class ChatHandler(BaseRequestHandler):
    def handle(self):
        print("Got connection from:", self.client_address)
        data = str(self.request.recv(7766))[2:-1]
        print(data)
        if data == "msg":
            print("Get Messages")
            self.request.send("|".join(messages).encode("utf-8"))
        else:
            messages.append(data)
            print(messages)

### Main
if __name__ == "__main__":
    print("Starting server...")
    print("Press Ctrl+C to stop")
    server = TCPServer(("", 9897), ChatHandler)
    server.serve_forever()
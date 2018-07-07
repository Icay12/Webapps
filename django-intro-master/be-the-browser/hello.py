from socket import socket

s = socket()
s.connect(('localhost', 8000))
s.send("""GET /greet?name=Farnam HTTP/1.1
Host: localhost:8000

""")

data = s.recv(8192)
while len(data) > 0:
    print(data)
    data = s.recv(8192)

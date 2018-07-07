from socket import socket

s = socket()
s.connect(('www.jeffeppinger.com', 80))
s.send("""GET /jle/ HTTP/1.1
Host: www.jeffeppinger.com

""")

print(s.recv(8192))

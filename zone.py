#!/usr/bin/env python
import socket
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = socket.gethostname()

port = 9999

s.connect((host, port))

zone = sys.argv[2]
status = sys.argv[1]

sendString = "ZONE:" + status + ":" + zone
s.send(sendString.encode('ascii'))

s.close()

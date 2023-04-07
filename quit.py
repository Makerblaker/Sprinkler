#!/usr/bin/env python3
import socket
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = socket.gethostname()

port = 9999

s.connect((host, port))

sendString = "QUIT"
s.send(sendString.encode('ascii'))

s.close()

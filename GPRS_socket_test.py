#!/usr/bin/env python
import socket
import sys
import time
host='202.120.188.59';
port=80;
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host = sys.argv[1]
port = int(sys.argv[2])
s.connect((host,port))
if len(sys.argv)>=4 and sys.argv[4]=='c':
    for i in range(0,10):
        s.send(sys.argv[3]+str(i)+'\n')
        time.sleep(10)
else :
    s.send(sys.argv[3]+'\n')

#s.close();


#!user/bin/env python
import socket, sys
from thread import *


listening_port = 6666
max_conn = 5
buffer_size = 4096

def start():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('', listening_port))
        s.listen(max_conn)
    except Exception, e:
        print "Unable to initialize Socket"
        print
        sys.exit(2)

    while 1:
        try:
            conn,addr = s.accept();
            data = conn.recv(buffer_size)
            start_new_thread(resend, (conn,data,addr))
        except KeyboardInterrupt:
            s.close()
            print "Proxy Server Shutting Down ..."
            sys.exit(1)

    s.close()

def resend(conn, data, addr):
    serverIp = "192.168.25.49"
    serverPort = 80
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((serverIp,serverPort))
        s.send(data)

        while 1:
            reply = s.recv(buffer_size)

            if(len(reply)>0):
                conn.send(reply)
                dar = float((len(reply)/1024))

                print "Request done :%s => %.3f " %(str(addr[0]),dar)
            else:
                break
        s.close()
        conn.close()
    except socket.error,(value,message):
        s.close()
        conn.close()
        sys.exit(1)

start()

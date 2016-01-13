import socket,select
import asyncore
import time
import os
from GPRS_data_operator import GPRS_data_operator
class GPRS_handler(asyncore.dispatcher_with_send):
    current_data = ''
    current_flag = time.strftime('%Y-%m-%d:%H:%M%S')
    def handle_read(self):
        data =self.recv(1024)
        if data :
            print data
        GPRS_handler.current_data = data
        GPRS_handler.current_flag = time.strftime('%Y-%m-%d:%H:%M%S')
        data_config = GPRS_data_operator.read_config()
        data_time = time.strftime('%Y-%m-%d')
        data_operator = GPRS_data_operator(os.path.join(data_config['data_dir'],data_time+'.txt'))
        data_operator.write_data(data)

def get_current_info():
    return GPRS_handler.current_data,GPRS_handler.current_flag

class GPRS_socket(asyncore.dispatcher):
    def __init__(self,ip='localhost',port=7080):
       asyncore.dispatcher.__init__(self)
       #self.server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
       #self.server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
       self.create_socket(socket.AF_INET,socket.SOCK_STREAM)
       self.set_reuse_addr()
       self.bind((ip,port))
       self.listen(5)
       #self.inputs = [self.server]

    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            sock,addr = pair
            print 'Incomming connection from %s' %repr(addr)
            handler = GPRS_handler(sock)

    def listening(self):
        asyncore.loop()

    #def listen(self):
    #    rs,ws,es = select.select(self.inputs,[],[],1)
    #    for r in rs :
    #        if r is server :
    #            client_sockt,client_addr = r.accept();
    #            self.inputs.append(client_sockt)
    #        else :
    #            data = r.recv(1024)
    #            if not data:
    #                self.inputs.remove(r)
    #            else :
    #                print data

if __name__ == '__main__':
    test = GPRS_socket()
    #test.listen()
    asyncore.loop()

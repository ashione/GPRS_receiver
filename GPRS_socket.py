import socket,select
import time
import os
from GPRS_data_operator import GPRS_data_operator
import Queue

class GPRS_socket(object):
    def __init__(self,ip='localhost',port=7080):
       self.server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
       #self.server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,75)
       self.server.bind((ip,port))
       socket.setdefaulttimeout(600)
       self.server.listen(5)
       #self.inputs = [self.server]

    def listening(self,queue):
        assert isinstance(queue,Queue.Queue)
        inputs = [self.server]
        while inputs:
            rs,ws,es = select.select(inputs,[],[],5)
            for r in rs:
                if r is self.server:
                    clientsock,clientaddr = r.accept() 
                    inputs.append(clientsock)
                else :
                    data = r.recv(2048)
                    #if not data:
                        #inputs.remove(r)
                    if data :
                        print data,'Incomming from ',clientaddr
                        queue.put(data)
                        data_config = GPRS_data_operator.read_config()
                        data_time = time.strftime('%Y%m%d')
                        #data_operator = GPRS_data_operator(os.path.join(data_config['data_dir'],data_time+'.txt'))
                        data_operator = GPRS_data_operator(os.path.join(data_config['data_dir'],data_time+'.dat'))
                        data_operator.write_data(data)
                    else :
                        print 'no data comming, closing'
                        inputs.remove(r)

            #print 'before'
            #conn,addr = self.server.accept()
            #print addr,'is connected!'
            #try :
            #    data = conn.recv(2048)
            #    if len(data)>0:
            #        print data,'Incomming from ',addr
            #        data_config = GPRS_data_operator.read_config()
            #        data_time = time.strftime('%Y%m%d')
            #        data_operator = GPRS_data_operator(os.path.join(data_config['data_dir'],data_time+'.dat'))
            #        data_operator.write_data(data)
            #        queue.put(data)
            #    else :
            #        conn.shutdown(socket.SHUT_RDWR)
            #        conn.close()
            #except Exception as msg:
            #    conn.shutdown(socket.SHUT_RDWR)
            #    conn.close()
            #    print msg
            #print 'after'

    def recv(self,queue):
        while True:
            try :
                data = self.server.recv(0xfff)
                print time.strftime('%Y-%m-%d %h:%M:%s'),data,'Incomming from '#,clientaddr
                queue.put(data)
                data_config = GPRS_data_operator.read_config()
                data_time = time.strftime('%Y-%m-%d')
                data_operator = GPRS_data_operator(os.path.join(data_config['data_dir'],data_time+'.dat'))
                data_operator.write_data(data)
            except Exception,e:
                print e

    def close(self):
        self.server.close()

if __name__ == '__main__':
    test = GPRS_socket()
    test.listening()

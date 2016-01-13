from Tkinter import *
import time
import asyncore
from datetime import datetime
from GPRS_socket import GPRS_socket
import thread
from GPRS_thread import GPRS_thread
from GPRS_data_operator import GPRS_data_operator
import os
import Queue
from GPRS_sendEmail import send_mail as GPRS_SendEmail
class Swither(object):
    def __init__(self,master):
        #self.main_window = Toplevel(master)
        self.main_window = (master)
        self.main_window.title('GPRS Receiver')
        self.ip_hint_string = StringVar()
        self.ip_hint_label = Label(self.main_window,textvariable=self.ip_hint_string,relief=RAISED)
        self.ip_hint_string.set('IP')
        self.ip_hint_label.grid(row=0,column=0,sticky=W,padx=10,pady=10)

        self.hint_string = StringVar()
        self.hint_label = Label(self.main_window,textvariable=self.hint_string,relief=RAISED)
        self.hint_string.set('Port')
        self.hint_label.grid(row=1,column=0,sticky=W,padx=10,pady=10)

        self.port_var = StringVar()
        self.port_entry = Entry(self.main_window,textvariable=self.port_var)
        self.port_entry.grid(row=1,column=1,sticky=W)
        #self.hint_label.pack()
        self.ip_var = StringVar()
        self.ip_entry = Entry(self.main_window,textvariable=self.ip_var)
        self.ip_entry.grid(row=0,column=1,sticky=W)

        self.bt_start = Button(self.main_window,text='Start',command=self.listen)
        self.bt_start.grid(row=0,column=2,padx=5,pady=5)

        self.bt_halt = Button(self.main_window,text='Halt',command=self.stop)
        self.bt_halt.grid(row=1,column=2,padx=5,pady=5)

        self.bt_set_directory = Button(self.main_window,text='Directory')
        self.bt_set_directory.grid(row=2,column=2,padx=5,pady=5)

        self.directory_var = StringVar()
        self.directory_entry = Entry(self.main_window,textvariable=self.directory_var)
        self.directory_entry.grid(row=2,column=1,columnspan=2,sticky=W)

        self.receiver_data = Text(self.main_window)
        self.receiver_data.grid(row=3,column=0,columnspan=3,padx=3,pady=3)
        self.scroll = Scrollbar(self.main_window, command=self.receiver_data.yview)
        self.receiver_data.configure(yscrollcommand=self.scroll.set)
        #self.scroll.pack(side=RIGHT,fill=Y)

        self.clock = Label(self.main_window,bg='green',font=('times',20,'bold'))
        self.clock.grid(row=2,column=0)
        self.clock.after(1000,self.tick)
        #self.socket = GPRS_socket()
        self.queue_data = Queue.Queue()
        #self.thread = GPRS_thread(1,self.socket.listening,self.queue_data)

        self.read_text()
        self.main_window.protocol('WM_DELETE_WINDOW',self.on_close)
    def read_text(self):
        data_config = GPRS_data_operator.read_config()
        data_time = time.strftime('%Y%m%d')
        data_operator = GPRS_data_operator(os.path.join(data_config['data_dir'],data_time+'.txt'))
        self.ip_var.set(data_config['ip'])
        self.port_var.set(data_config['port'])
        self.directory_var.set(data_config['data_dir'])
        data = data_operator.read_data()
        #print data
        self.receiver_data.insert(END,''.join(data))
        #data_operator.write_data(data)
        self.pre_date = datetime.now()

    def tick(self):
        tick_time = time.strftime('%Y-%m-%d %H-%M:%S')
        self.clock.config(text=tick_time)

        if (datetime.now().day != self.pre_date.day):
            self.send_mail()
            self.pre_date = datetime.now()
            self.receiver_data.delete('1.0',END)

        if self.queue_data.empty() is not True :
            current_data = self.queue_data.get()
            print 'in queue: ',current_data
            self.receiver_data.insert('1.0',tick_time+' '+current_data+os.linesep)

        self.clock.after(1000,self.tick)

    def send_mail(self):
        send_date = self.pre_date.strftime('%Y%m%d')
        temp_config = GPRS_data_operator.read_config()
        try :
            GPRS_SendEmail(sub='Data of '+send_date,
                        content='There is auto-sender of GPRS_receiver',
                        att=os.path.join(temp_config['data_dir'],send_date+'.txt'))
            print send_mail,': send email ok!'
        except Exception as msg:
            print 'send email faild,',msg

    def listen(self):
        if hasattr(self,'socket'):
            self.stop()
            #self.socket.close()
            #print self.ip_var.get()

        self.socket = GPRS_socket(ip=self.ip_var.get(),port=int(self.port_var.get()))
        self.thread = GPRS_thread(1,self.socket.listening,self.queue_data)
        #self.thread_recive = GPRS_thread(1,self.socket.recv,self.queue_data)
        #self.listener_thread = thread.start_new_thread(self.socket.listening,(1,))
        self.thread.start()
        #self.thread_recive.start()
        #self.thread.run(self.socket.listening)

    def stop(self):
        if hasattr(self,'socket'):
            self.thread.stop()
            #self.thread_recive.stop()

    #ensure this thread stop before window destroy
    def on_close(self):
        self.stop();
        self.main_window.destroy()


if __name__ == '__main__':
    window = Tk()
    test = Swither(window)
    mainloop()

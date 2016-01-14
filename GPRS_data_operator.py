import os
import json
class GPRS_data_operator(object):
    def __init__(self,absfile):
        self.file = absfile
        #self.file.replace('.txt','.dat')

    @staticmethod
    def read_config():
        with open('GPRS_config.json') as config_file:
            data = json.load(config_file)
            config_file.close()
        return data

    @staticmethod
    def read_email_receiver():
        data = GPRS_data_operator.read_config()
        return data['email_receiver']

    @staticmethod
    def read_email_sender():
        data = GPRS_data_operator.read_config()
        return data['email_sender']

    @staticmethod
    def alter_atrribute(key,value):
        with open('GPRS_config.json','r+') as config_file:
            try :
                data = json.load(config_file)
                data[key] = value
            except Exception as msg:
                print msg
                return

        with open('GPRS_config.json','w') as config_file:
            json.dump(data,config_file,indent=4)
            config_file.close()

    @staticmethod
    def alter_directory(directory_str):
        GPRS_data_operator.alter_atrribute('data_dir',directory_str)

    @staticmethod
    def alter_ip(ip):
        GPRS_data_operator.alter_atrribute('ip',ip)

    @staticmethod
    def alter_port(port):
        GPRS_data_operator.alter_atrribute('port',int(port))

    @staticmethod
    def alter_email_receiver(receiver):
        GPRS_data_operator.alter_atrribute('email_receiver',receiver)

    def read_data(self):
        try :
            with open(self.file,'r') as fp:
                lines = fp.readlines()
                fp.close()
            lines.reverse()
            return lines
        except Exception,e:
            print e
        return ''
    def write_data(self,line):
        if not os.path.isfile(self.file):
            print '%s is no exist,now touch it!' %self.file
            open(self.file,'a').close()
            os.utime(self.file,None)

        try :
            fp = open(self.file,'a')
            fp.write(line+os.linesep)
            fp.close()
        except Exception as error:
            print error

        print 'write %s in %s ok.' %(line,self.file)



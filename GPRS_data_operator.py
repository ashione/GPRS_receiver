import os
import json
class GPRS_data_operator(object):
    def __init__(self,absfile):
        self.file = absfile

    @staticmethod
    def read_config():
        with open('GPRS_config.json') as config_file:
            data = json.load(config_file)
        return data

    @staticmethod
    def read_email_receiver():
        data = GPRS_data_operator.read_config()
        return data['email_receiver']

    @staticmethod
    def read_email_sender():
        data = GPRS_data_operator.read_config()
        return data['email_sender']

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



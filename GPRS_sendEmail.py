# -*- coding: UTF-8 -*-
import smtplib
from email.mime.text import MIMEText
from email import Encoders
from email.header import Header
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from GPRS_data_operator import GPRS_data_operator
import os
#mailto_str = ['zlx<14zlx@tongji.edu.cn',
#              '1004354917@qq.com',
#              'zhouxytj@tongji.edu.cn',
#              '1410242@tongji.edu.cn']

#mail_host="smtp.tongji.edu.cn"  #设置服务器
#mail_user="14zlx"    #用户名
#mail_pass="xxxxxxxx"   #口令
#mail_postfix="tongji.edu.cn"  #发件箱的后缀
email_sender = GPRS_data_operator.read_email_sender()
mail_host = email_sender['host']
mail_user = email_sender['user']
mail_pass = email_sender['pass']
mail_postfix = email_sender['postfix']

def send_mail(sub,content,to_str=None,att='window.py'):
    if to_str is None :
        to_str = GPRS_data_operator.read_email_receiver()
    me="snowobservation"+"<"+mail_user+"@"+mail_postfix+">"
    #msg = MIMEText(content,_subtype='plain',_charset='utf-8')
    msg = MIMEMultipart()
    msg['Subject'] = Header(sub,'utf-8').encode()
    msg['From'] = me
    msg['To'] = ";".join(to_str)

    if att is not None :
        part = MIMEBase('application','octet-stream')
        part.set_payload(open(att,'rb').read())
        Encoders.encode_base64(part)
        part.add_header('Content-Disposition','attachment; filename="%s"' %os.path.basename(att))
        part.add_header('Content-ID', '<0>')
        part.add_header('X-Attachment-Id', '0')
        msg.attach(part)

    #msg['To'] = to_str
    try:
        server = smtplib.SMTP()
        #server.set_debuglevel(1)
        server.connect(mail_host)
        server.login(mail_user,mail_pass)
        server.sendmail(me, to_str, msg.as_string())
        server.close()

        return True
    except Exception, e:
        print str(e)
        return False

if __name__ == '__main__':
    if send_mail("data of text","don't reply",att='./data/2015-12-29.txt'):
        print "发送成功"
    else:
        print "发送失败"

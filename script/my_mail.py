#!/usr/bin/env python
# -*- coding: utf-8 -*-

import smtplib
from email.mime.text import MIMEText  
from email.header import Header
from netmon_env import envi
from my_log import logger

 
####
def send_mail(sub,content,receiver):
    if receiver == ['']:
       logger.warn('mail[' + sub + '] fail, empty receive list!')
       return False

    if not send_mail_int(sub,content,receiver):
       send_mail_int_nologin(sub,content,receiver)

def send_mail_int(sub,content,receiver):
    sender = "netmon<%s>" % envi['smtp_usr']
    msg = MIMEText(content,'plain','gbk')
    msg['Subject'] = Header(sub, 'gbk')
    msg['From'] = sender
    
    try:
        smtp = smtplib.SMTP()
        smtp.connect(envi['smtp_server'])
        smtp.login(envi['smtp_usr'], envi['smtp_pwd'])
        smtp.sendmail(sender, receiver, msg.as_string())
        smtp.quit()
    except Exception, e:
        logger.error(str(e))
        return False
    else:
        logger.info('mail [' + sub + '] to ' + str(receiver))
        return True

def send_mail_int_nologin(sub,content,receiver):
    sender = "netmon<%s>" % envi['smtp_usr']
    msg = MIMEText(content,'plain','gbk')
    msg['Subject'] = Header(sub, 'gbk')
    msg['From'] = sender
    
    try:
        smtp = smtplib.SMTP(envi['smtp_server'])
        smtp.sendmail(sender, receiver, msg.as_string())
        smtp.quit()
    except Exception, e:
        logger.error(str(e))
        return False
    else:
        logger.info('mail [' + sub + '] to ' + str(receiver))
        return True

def send_mail_ext(sub,content,receiver):
    if receiver == ['']:
       logger.warn('mail[' + sub + '] fail, empty receive list!')
       return False

    if(envi['smtp_server2'] == ''):
       return send_mail(sub,content,receiver)

    sender = "netmon<%s>" % envi['smtp_usr2']
    msg = MIMEText(content,'plain','gbk')
    msg['Subject'] = Header(sub, 'gbk')
    msg['From'] = sender
   
    try:
        smtp = smtplib.SMTP()
        smtp.connect(envi['smtp_server2'])
        smtp.login(envi['smtp_usr2'], envi['smtp_pwd2'])
        smtp.sendmail(sender, receiver, msg.as_string())  
        smtp.quit()
    except Exception, e:
        logger.error(str(e))
        return False
    else:
        logger.info('mail [' + sub + '] to ' + str(receiver))
        return True


if __name__ == '__main__':

    list1=['gaojianming.zj@139.com','16015@etransfar.com']
    list3=['gaojianming.zj@ccb.com']
    list2 = []
    send_mail(u'这是python测试邮件22',u'python发送邮件',list1)

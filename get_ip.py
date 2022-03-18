#!/usr/bin/python3
import os
import requests
import smtplib
from email.mime.text import MIMEText
from email.header import Header

LOCAL_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ip.txt')


mail_host="smtp.163.com"
# user name
mail_user=""
# email password
mail_pass="" 
# 发件邮箱地址
sender = ""
# 收件箱，可以用[]填写多个收件人
rece = ["",""]

def send_mail(msg):
    message = MIMEText(msg,'plain', 'utf-8')
    message['From'] = Header('wyls','utf-8')
    message['To'] = Header('myself','utf-8')

    subject =  'IP Changed'
    message['Subject'] = Header(subject,'utf-8')

    try:
        smtpObj = smtplib.SMTP_SSL(mail_host)
        smtpObj.connect(mail_host, 465)
        smtpObj.login(mail_user,mail_pass)
        smtpObj.sendmail(sender, rece, message.as_string())
        print ("邮件发送成功")
    except smtplib.SMTPException:
        print ("Error: 无法发送邮件")


def get_curr_ip():
	headers = {
		'content-type': 'text/html',
		'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'
	}
	resp_v4 = requests.get('https://ipv4.ipw.cn', headers=headers)
	return resp_v4.content

def get_lastest_local_ip():
    try:
        with open(LOCAL_FILE, 'r') as f:
            data = f.read()
            return data
    except:
        return ''

if __name__ == '__main__':
    ip_data = get_curr_ip()
    print(ip_data)
    last_ip_data = get_lastest_local_ip().encode()
    print(last_ip_data)
    need_write = False
    if ip_data != last_ip_data:
        need_write = True
        send_mail(ip_data)
        
    if need_write:
        print('save ip to {}...'.format(LOCAL_FILE))
        with open(LOCAL_FILE, 'wb') as f:
            f.write(ip_data)

    

#-*-coding:utf-8-*-

from app import app
from itsdangerous import URLSafeTimedSerializer
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
from email import encoders
from email.header import Header
import smtplib

ts = URLSafeTimedSerializer(app.config["SECRET_KEY"])

myEmailAddresss = "ouertouru@163.com"
password = "1638096@weiyi"
smtpServer = "smtp.163.com"

#393129389

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr(( \
        Header(name, 'utf-8').encode(), \
        addr.encode('utf-8') if isinstance(addr, unicode) else addr))

def sendmail(html,to_email,subject):
	msg = MIMEText(html,_subtype='html',_charset='utf-8')
	msg['Subject'] = Header(subject,'utf-8').encode()
	msg['From'] = _format_addr(u'geixyw.cc验证邮件<%s>'%myEmailAddresss)
	msg['To'] = _format_addr(u'验证账户<%s>'%to_email)
	server = smtplib.SMTP(smtpServer,25)
	server.set_debuglevel(1)
	server.login(myEmailAddresss,password)
	server.sendmail(myEmailAddresss,[to_email],msg.as_string())
	server.quit()
#! /usr/bin/python
# coding=utf-8
import sys
import smtplib

from email.mime.text import MIMEText
from email.header import Header
from email.MIMEMultipart import MIMEMultipart
from email.MIMEImage import MIMEImage


to_addr = sys.argv[1]
subject = sys.argv[2]
msg = sys.argv[3]

smtp_conf = {'host': 'smtp.office365.com',
             'user': 'support@gti.com.cn',
             'password': 'supp@1234',
             'port': 587,
             'tls': True}



message = MIMEMultipart('related')

msg_html = MIMEText("""

    <table width="750"  align="center" cellpadding="0" cellspacing="0"
        border="0">
    <tbody>
    <tr>
        <table width="750" align="center" cellpadding="0" cellspacing="0"
            border="0">
            <tbody>
            <tr >
                <td width = "8" height = "41" bgcolor="#fa4a1a"></td>
                <td width = "15" style="border: 1px solid #eee;
                    border-right: none;border-left: none" >
                </td>
                <td  style="border: 1px solid #eee; border-left: none">
                    告警通知
                </td>
            </tr>
        </table>
    </tr>
    <tr>
        <table style="border: 1px solid #eee; border-top: none;
            border-bottom: none"
            width="750" align="center" cellpadding="0" cellspacing="0" >
            <tbody>
            <tr >
                <td style="padding: 40px 50px">
                    %s
                </td>
            </tr>
            </tbody>
        </table>
    </tr>

    </tbody>
   <tbody>

    <table style="border: 1px solid #eee; border-top: none;border-bottom: none"
        width="750" align="center" cellpadding="0" cellspacing="0" >
    <td  style="border: 1px solid #eee; border-left: none" align="center">
        <img src="cid:footer_img" alt="footer_img" width="750px" height="auto">
    </td>
    </table>

   </tbody>

</table>
<br>
<br>
<br>
<br>

    """ % msg.replace("\r\n", "<br>"), "HTML", "uft-8")
message.attach(msg_html)

fp = open('/usr/lib/zabbix/alertscripts/email-banner.png', 'rb')
msg_img = MIMEImage(fp.read())
msg_img.add_header('Content-ID', 'footer_img')
message.attach(msg_img)

message['From'] = 'GTI 技术运维团队 <%s>' % smtp_conf['user']
message['To'] = to_addr
message['Subject'] = Header(subject, 'utf-8').encode()

server = smtplib.SMTP(smtp_conf['host'],smtp_conf['port'])
server.set_debuglevel(1)
server.ehlo()
server.starttls()
server.login(smtp_conf['user'],smtp_conf['password'])
server.sendmail(smtp_conf['user'],[to_addr], message.as_string())
server.quit()


from __future__ import print_function
from PIL import Image
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from google.oauth2 import service_account
from operator import itemgetter
import random
import string
import sys
import googleapiclient.discovery
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email import encoders
import barcode
import datetime
from barcode.writer import ImageWriter
import imghdr
import os

def mail(to, subject, text=None, html=None, attach=None):
   msg = MIMEMultipart()
   msg['From'] = "cayenne<do-not-reply@srvusd-lunch.com>" #gmail_user
   msg['To'] = to
#','.split(to)
   msg['Subject'] = subject

   if (html != None and text != None):
       msgAlternative = MIMEMultipart('alternative')
       msg.attach(msgAlternative)
       msgAlternative.attach(MIMEText(html, 'html'))
       msgAlternative.attach(MIMEText(text, 'plain'))
   elif (html != None):
       msg.attach(MIMEText(html, 'html'))
   elif (text != None):
       msg.attach(MIMEText(text, 'plain'))

   # if (attach != None):
   #     fp = open(attach, 'rb')
   #     msgImage = MIMEImage(fp.read())
   #     fp.close()

       # msgImage.add_header('Content-ID', '<image1>')
       # msg.attach(msgImage)
           # part = MIMEBase('application', 'octet-stream')
           # part.set_payload(open(attach, 'rb').read())
           # encoders.encode_base64(part)
           # part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(attach))
           # msg.attach(part)

   mailServer = smtplib.SMTP("localhost", 587)
   mailServer.ehlo()
   mailServer.starttls()
   #mailServer.ehlo()
#   mailServer.login(gmail_user, gmail_password)
   mailServer.sendmail(from_user, to, msg.as_string())
   # Should be mailServer.quit(), but that crashes...
   mailServer.close()

def generate_email():
    #i = vals
    to = "9259646667@txt.att.net"
    #name = i[COL_NAME]

    subject = "Fire Detected"

     # The embedded image doesn't show up in gmail so use inline attachment
     # '<br>\n<img src="data:image/png;base64,{0}" alt="">'.format(data_uri) + \
    htmlbody = "Fire detected at (37.77042000, -121.90381000) with temperature 55 C heading for San Ramon"
#    textbody=strip_html( htmlbody)

    try:
        mail(to, subject, text=htmlbody, html=None)

    except Exception as e:
        print("ERROR: Failed to send email to: "+to+": "+str(e))

generate_email()

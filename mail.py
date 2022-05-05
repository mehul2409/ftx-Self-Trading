import os
import smtplib
import os
from email.message import EmailMessage
EMAIL_ADDRESS= os.getenv("Email_Address")
EMAIL_PASSWORD=os.getenv("Email_Password")
msg=EmailMessage()
msg['From']=EMAIL_ADDRESS
msg['Subject']='Trading working Stop'
msg['To']='mehul.dev24@gmail.com'
def send(e):
    msg.set_content("The program stop working due to following reason")
    with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp:
        smtp.login(EMAIL_ADDRESS,EMAIL_PASSWORD)
        smtp.send_message(msg)
import smtplib
from dotenv import load_dotenv
from os import getenv
from email.message import EmailMessage
import random

server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
load_dotenv()
server.login("meet.and.hack.project@gmail.com", getenv("PASSWORD"))

def send_verification_email(email):
    msg = EmailMessage()
    msg["subject"] = "Verify your email"
    msg["to"] = email
    msg["from"] = "meet.and.hack.project@gmail.com"
    code = ""
    for i in range(6):
        code += str(random.randint(0, 9))
    msg.set_content(
        f"""
        Please enter this code into the form 
        {code} 
        to verify your email.
    """)
    server.send_message(msg)
    return code

if __name__ == "__main__":
    send_verification_email("evanclough99@gmail.com")
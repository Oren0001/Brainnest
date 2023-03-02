"""
The goal of this project is to automate the process of sending daily reports via email
to different clients.
"""

import smtplib
import os
import schedule
from time import sleep
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

USERNAME = "Enter username here"
PASSWORD = "Enter password here"


def get_recipients_list():
    if not os.path.exists("recipients.txt"):
        raise FileNotFoundError("Add Recipients File.")
    with open("recipients.txt") as f:
        return [recipient.strip() for recipient in f]


def new_mail(recipients):
    mail = MIMEMultipart()
    if not os.path.exists("reports.pdf"):
        raise FileNotFoundError("Add Reports File.")
    with open("reports.pdf", "rb") as reports:
        att = MIMEApplication(reports.read(), _subtype='pdf')
        att.add_header('Content-Disposition', 'attachment', filename="reports.pdf")
        mail.attach(att)

    mail['From'] = USERNAME
    mail['To'] = ",".join(recipients)
    mail['Subject'] = "Daily Reports"
    mail.attach(MIMEText("Daily reports are attached to this mail", "plain"))

    return mail


def send_email(mail, recipients):
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(mail["From"], PASSWORD)
        server.sendmail(mail["From"], recipients, mail.as_string())


def update_log_file(msg):
    with open("logs.txt", 'w') as logs:
        log = datetime.now().strftime("%m/%d/%Y, %H:%M") + f": {msg}\n"
        logs.writelines(log)


def main():
    try:
        recipients = get_recipients_list()
        mail = new_mail(recipients)
        send_email(mail, recipients)
    except FileNotFoundError as e:
        print(e)
        exit()
    except Exception as e:
        update_log_file(e)
    else:
        update_log_file("Emails Sent.")


if __name__ == "__main__":
    schedule.every().day.at("21:00").do(main)
    while True:
        schedule.run_pending()
        sleep(60)

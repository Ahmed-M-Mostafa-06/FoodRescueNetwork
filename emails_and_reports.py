import json
import os
import smtplib
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DONATIONS_FILE = os.path.join(BASE_DIR, "donations.json")
USERS_FILE = os.path.join(BASE_DIR, "users.json")
REPORT_FILE = os.path.join(BASE_DIR, "report.csv")


class EmailService:
    def __init__(self, sender_email, sender_password):
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587

    def load_users(self):
        with open(USERS_FILE) as file:
            data = json.load(file)
        return data

    def find_user_email(self, name):
        for user in self.load_users():
            if user["name"] == name:
                return user["email"]
        return None

    def send_email(self, to_email, subject, body):
        if to_email is None:
            print("Email address not found, notification skipped")
            return
        message = f"Subject: {subject}\n\n{body}"
        server = smtplib.SMTP(self.smtp_server, self.smtp_port)
        server.starttls()
        server.login(self.sender_email, self.sender_password)
        server.sendmail(self.sender_email, to_email, message)
        server.quit()
        print(f"Email sent to {to_email}")

    def notify_reservation(self, donation):
        donor_email = self.find_user_email(donation["donor_name"])
        subject = "Your Donation Has Been Reserved"
        body = f"Hello {donation['donor_name']}, your donation '{donation['food_name']}' has been reserved."
        self.send_email(donor_email, subject, body)

    def notify_receipt_confirmation(self, donation):
        donor_email = self.find_user_email(donation["donor_name"])
        subject = "Your Donation Has Been Delivered"
        body = f"Hello {donation['donor_name']}, your donation '{donation['food_name']}' has been delivered."
        self.send_email(donor_email, subject, body)

    def notify_new_donation(self, donation):
        donor_email = self.find_user_email(donation["donor_name"])
        subject = "Donation Added Successfully"
        body = f"Hello {donation['donor_name']}, your donation '{donation['food_name']}' has been added."
        self.send_email(donor_email, subject, body)


def generate_report():
    with open(DONATIONS_FILE) as file:
        data = json.load(file)

    total_donations = len(data["donations"])
    status_counts = {}
    for donation in data["donations"]:
        status = donation["status"]
        status_counts[status] = status_counts.get(status, 0) + 1

    report_data = {
        "Metric": ["Total Donations", "Available", "Reserved", "Delivered"],
        "Count": [total_donations, status_counts.get("Available", 0),
                  status_counts.get("Reserved", 0), status_counts.get("Delivered", 0)]
    }
    df = pd.DataFrame(report_data)
    df.to_csv(REPORT_FILE, index=False)
    return df

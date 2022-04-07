import csv
from pprint import pprint
import smtplib
import sys
from decouple import config
from email.message import EmailMessage
sender_email = config('EMAIL')
sender_password = config('PASSWORD')
sender_name = config("NAME")
receivers = []
# Reading from csv
def write_emails_csv(row):
    file = open('./files/users_emails.csv',"a",newline="")
    fieldnames=["NAME","EMAIL"]
    dictwriter = csv.DictWriter(file,delimiter=',', lineterminator='\n',fieldnames=fieldnames)
    if file.tell() == 0:
        dictwriter.writeheader()
    dictwriter.writerow(row)
    file.close()
def read_emails_csv():
    print("\n-----------------------------")
    print("Reading Data from CSV file...")
    print("-----------------------------\n")
    file = open('./files/users_emails.csv',"r",newline="")
    dictreader = csv.DictReader(file,)
    for row in dictreader:
        receivers.append(row)
    print("\n-----------------------------")
    print("Reading Data from CSV file Completed...")
    print("-----------------------------\n")

def add_recievers():
    n = int(input("How many users you want to add? "))
    if n == 1:
        name = input("Enter name: ")
        email = input("Enter email: ")
        write_emails_csv({"NAME":name,"EMAIL":email})
        print("Written Successfully")
    else:
        while n >= 1:
            name = input("Enter name: ")
            email = input("Enter email: ")
            write_emails_csv({"NAME":name,"EMAIL":email})
            print("Written Successfully")
            n -= 1
def create_and_send_mail(name, receiver, subject, message):
    email = EmailMessage()

    email["To"] = receiver
    email["From"] = sender_email
    email["Subject"] = subject
    email.set_content(f"Dear {name},\n\n\t"+message+f"\n\n\nRegards,\n{sender_name}\n{sender_email}")

    # Starting TLS
    smtp = smtplib.SMTP('smtp.gmail.com',587)
    smtp.starttls()
    smtp.login(sender_email,sender_password)
    smtp.send_message(email)
    smtp.close()

def send_email(subject, message):
    read_emails_csv()
    if len(receivers) <= 1:
        print("\n-----------------------------")
        print("Sending Mail")
        print("-----------------------------\n")
        create_and_send_mail(receivers[0]["NAME"],receivers[0]["EMAIL"],subject,message)
        print("\n-----------------------------")
        print(f"{len(receivers)} Mail Sent.")
        print("-----------------------------\n")
    else:
        print("\n-----------------------------")
        print("Sending Mails")
        print("-----------------------------\n")
        for receiver in receivers:
            create_and_send_mail(receiver["NAME"],receiver["EMAIL"],subject,message)
        print("\n-----------------------------")
        print(f"{len(receivers)} Mails Sent.")
        print("-----------------------------\n")
def menu():
    print("\n1. Add Data to CSV file")
    print("2. See CSV file data")
    print("3. Send Mail.")
    print("4. Exit\n")
    return int(input("Enter Choice : "))
if __name__ == "__main__":
    choice = menu()
    if choice == 1:
        add_recievers()
        sys.exit(0)
    elif choice == 2:
        read_emails_csv()
        pprint(receivers)
        sys.exit(0)
    elif choice == 3:
        subject = input("Enter Subject: ")
        message = input("Enter Message: ")
        send_email(subject,message)
        sys.exit(0)
    elif choice == 4:
        sys.exit(0)
    sys.exit(0)


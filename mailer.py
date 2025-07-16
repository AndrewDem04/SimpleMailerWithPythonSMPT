import csv
from datetime import datetime, timedelta
import smtplib
from email.message import EmailMessage

def read_and_process_csv(filename):
    updated_rows = []
    today = datetime.now().date()
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = list(csv.DictReader(csvfile))
        for row in reader:
            if row['Notification Status'].strip() == "Ειδοποίηση - Στάλθηκε":
                updated_rows.append(row)
                continue

            due_date = datetime.strptime(row['Account Due Date'], '%Y-%m-%d').date()
            if today + timedelta(days=3) >= due_date:
                send_email(row)
                row['Notification Status'] = 'Ειδοποίηση - Στάλθηκε'
            updated_rows.append(row)
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = updated_rows[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(updated_rows)

def send_email(row):
    msg = EmailMessage()
    msg['Subject'] = f"Υπενθύμιση Πληρωμής: {row['Account Type']}"
    msg['From'] = "YOUR EMAIL"
    msg['To'] = row['User Email']
    print(f"Email sent to {row['User Email']}")
    msg.set_content(f"""
Αγαπητέ/ή {row['Name']},

Υπενθυμίζουμε ότι ο λογαριασμός σας για {row['Account Type']} ποσού {row['Payment Amount']}€ λήγει στις {row['Account Due Date']}.

Παρακαλούμε όπως μεριμνήσετε εγκαίρως.

Με εκτίμηση,
Η ομάδα Υπενθυμίσεων
""")

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login('YOUR EMAIL', 'YOUR PASSWORD OR APP PASSWORD')
        smtp.send_message(msg)

read_and_process_csv(input("Enter the path to your CSV file: "))

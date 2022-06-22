import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart

ctx = ssl.create_default_context()
password = "qojxkexwarkaubtm"
sender = "birefringenceprogram@gmail.com"
receiver = "alexadam418@gmail.com"
message = MIMEMultipart("mixed")
message["Subject"] = "Birefringence Scan Finished"
message["From"] = sender
message["To"] = receiver

message.attach(MIMEText("Birefringence Scan Finished", "plain"))
filename = r"C:\Users\jadam\PycharmProjects\pythonProject\testdata.png"
with open(filename, "rb") as f:
    file = MIMEApplication(f.read())
disposition = f"attachment; filename={filename}"
file.add_header("Content-Disposition", disposition)
message.attach(file)

with smtplib.SMTP_SSL("smtp.gmail.com", port=465, context=ctx) as server:
    server.login(sender, password)
    server.sendmail(sender, receiver, message.as_string())

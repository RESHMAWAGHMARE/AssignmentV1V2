import pandas as pd
import io
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# read csv using pandas and then convert the csv to html string ....this code later will add into body
str_io = io.StringIO()
df = pd.read_csv('Sample.csv')
df.to_html(buf=str_io)
table_html = str_io.getvalue()
print(table_html)


sender_email = "mymail@gmail.com"
receiver_email = "anothermail@gmail.com"
password = "mypass"

message = MIMEMultipart("alternative")
message["Subject"] = "Subject: Your Title"
message["From"] = sender_email
message["To"] = receiver_email

text = """\
Subject: Your Title"""

html = """\
<html>
  <body>
    <p>{table_html}</p>
  </body>
</html>
""".format(table_html=table_html)

part1 = MIMEText(text, "plain")
part2 = MIMEText(html, "html")
message.attach(part1)
message.attach(part2)

# Send email
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(
        sender_email, receiver_email, message.as_string()
    )
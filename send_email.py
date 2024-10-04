import os
import smtplib
from email.mime.text import MIMEText

# Set environment variables
Mail_password = os.getenv('MAIL_PASSWORD') # declare the app password as an environment variable. or you can hardcode the password

From_email = "your-gmail@gmail.com"
recipients = ["recipient1@gmail.com", "recipient2@gmail.com"] # you can add multiple recipients or adjust for the single recipient


# Create email content
msg = MIMEText("""
Attention!!
Drift has been Detected in your recent Terraform architecture.
Jenkins pipeline has been triggered.
Immediate action recommended.
""") # enter the message
msg["Subject"] = "Warning!! Drift detected!"
msg["From"] = From_email # enter your gmail address
msg["To"] = ",".join(recipients)  # enter recipient's gmail address

# Connect to Gmail SMTP server using TLS
server = smtplib.SMTP("smtp.gmail.com", 587) # enter the smtp server address and the port
server.starttls() # use TLS

# Log in using app password
server.login(From_email, Mail_password)

# Send email
server.sendmail(From_email, recipients, msg.as_string())

# Close the connection
server.quit()


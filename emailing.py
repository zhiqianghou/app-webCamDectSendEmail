# Don't use email.py as file name as python has email library.
import smtplib, ssl
import imghdr
from email.message import EmailMessage


PASSWORD = "pwoojjssywjkpply"
SENDER = "houzh.py@gmail.com"
RECEIVER = "houzh.py@gmail.com"

def send_email(image_object):
	email_message = EmailMessage()
	email_message["Subject"] = "New customer showed up"
	email_message.set_content("Hi, We just saw a new customer")

	with open(image_object, "rb") as file:
		content = file.read()

	email_message.add_attachment(content, maintype="image", subtype=imghdr.what(None, content))

	gmail = smtplib.SMTP("smtp.gmail.com", 587)
	gmail.ehlo()
	gmail.starttls()
	gmail.login(SENDER, PASSWORD)
	gmail.sendmail(SENDER, RECEIVER, email_message.as_string())
	gmail.quit()


if __name__ == "__main__":
	send_email(image_object="images_test/16.png")
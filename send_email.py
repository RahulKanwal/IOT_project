import os
import smtplib
import config

def send_email(subject, msg, reciever):
	try:
		server = smtplib.SMTP('smtp.gmail.com:587')
		server.ehlo()
		server.starttls()
		server.login(config.EMAIL_ADDRESS, config.PASSWORD)
		messsage = 'Subject: {}\n\n{}'.format(subject, msg)
		server.sendmail(config.EMAIL_ADDRESS, reciever, messsage)
		server.quit()
		print('Mail sent to ' + reciever)
	except:
		print('Email fail.')

subject = 'Python test'
msg = 'This is sent using Python!!!'

recievers = ["2017.rahul.kanwal@ves.ac.in", "2017.mahesh.keswani@ves.ac.in", "2017.sanket.mahale@ves.ac.in"]

for reciever in recievers:
	send_email(subject, msg, reciever)

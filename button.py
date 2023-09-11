import RPi.GPIO as GPIO
import picamera
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
import time

# Set up GPIO
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)

# Set up the camera
camera = picamera.PiCamera()

# Email parameters
toaddr = "teddy.michael.sannan@gmail.com"
me = "teddy.michael.sannan@gmail.com"
my_password = "anvdjmcwwurpykyv"

def send_email(image_path):
    msg = MIMEMultipart()
    msg['Subject'] = 'Someone Is At Your Door'
    msg['From'] = me
    msg['To'] = toaddr

    # Attach the image
    part = MIMEBase('application', "octet-stream")
    part.set_payload(open(image_path, "rb").read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment', filename=image_path)  # or
    msg.attach(part)

    s = smtplib.SMTP_SSL('smtp.gmail.com')
    s.login(me, my_password)
    
    s.sendmail(me, toaddr, msg.as_string())
    s.quit()

while True:
    if GPIO.input(10) == GPIO.HIGH:
        print("Button was pushed!")
        image_path = "door_image.jpg"
        camera.capture(image_path)
        send_email(image_path)
        time.sleep(1)

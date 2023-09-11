# import necessary packages
from imutils.video import VideoStream
from imutils.video import FPS
import face_recognition
import imutils
import pickle
import time
import cv2
import serial  # to communicate with the Arduino
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
import time

def send_email(image_path):
    msg = MIMEMultipart()
    msg['Subject'] = 'Someone Unlocked the Door'
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

# Email parameters
toaddr = "teddy.michael.sannan@gmail.com"
me = "teddy.michael.sannan@gmail.com"
my_password = "anvdjmcwwurpykyv"

# initialize the HC-05 connection
bluetoothSerial = serial.Serial("/dev/rfcomm0", baudrate=9600)

# Initialize 'currentname' to trigger only when a new person is identified.
currentname = "unknown"

# Determine faces from encodings.pickle file model created from train_model.py
encodingsP = "encodings.pickle"

# load the known faces and embeddings
print("[INFO] loading encodings + face detector...")
data = pickle.loads(open(encodingsP, "rb").read())

# initialize the video stream
vs = VideoStream(usePiCamera=True).start()
time.sleep(2.0)

# start the FPS counter
fps = FPS().start()

while True:
    # grab the frame from the video stream and resize it
    frame = vs.read()
    frame = imutils.resize(frame, width=500)
    
    # Detect the face boxes
    boxes = face_recognition.face_locations(frame)
    encodings = face_recognition.face_encodings(frame, boxes)
    names = []

    # loop over the facial embeddings
    for encoding in encodings:
        # attempt to match each face in the input image to our known encodings
        matches = face_recognition.compare_faces(data["encodings"], encoding)
        name = "Unknown"  # if face is not recognized, then print Unknown

        # check to see if we have found a match
        if True in matches:
            matchedIdxs = [i for (i, b) in enumerate(matches) if b]
            counts = {}
            for i in matchedIdxs:
                name = data["names"][i]
                counts[name] = counts.get(name, 0) + 1
            name = max(counts, key=counts.get)
            if currentname != name:
                currentname = name
                print(currentname)
                if currentname != "Unknown":
                    image_path = "door_image.jpg"
                    cv2.imwrite(image_path, frame)  # save the current frame
                    send_email(image_path)
                    time.sleep(1)
                    bluetoothSerial.write(b'1')  # send '1' to the Arduino to unlock the door

        # update the list of names
        names.append(name)
    
    # check for incoming data from Arduino
    if bluetoothSerial.inWaiting() > 0:
        command = bluetoothSerial.read().decode("utf-8") 
        if command == '2':  # check if the signal from Arduino is '2'
            currentname = "unknown"  # reset the currentname variable

    # loop over the recognized faces
    for ((top, right, bottom, left), name) in zip(boxes, names):
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 225), 2)
        y = top - 15 if top - 15 > 15 else top + 15
        cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

    # display the image to our screen
    cv2.imshow("Facial Recognition is Running", frame)
    key = cv2.waitKey(1) & 0xFF

    # quit when 'q' key is pressed
    if key == ord("q"):
        break

    # update the FPS counter
    fps.update()

# stop the timer and display FPS information
fps.stop()
print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()

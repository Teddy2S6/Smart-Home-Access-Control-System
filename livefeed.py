from flask import Flask, render_template, Response
import cv2
from imutils.video import VideoStream
import time

app = Flask(__name__)

camera = VideoStream(usePiCamera=True, resolution=(640, 480), framerate=30).start()
time.sleep(2)

@app.route('/')
def index():
    return render_template('index.html')

def gen_frames():
    while True:
        frame = camera.read()
        ret, buffer = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)
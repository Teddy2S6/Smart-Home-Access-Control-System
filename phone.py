from flask import Flask
import serial

app = Flask(__name__)
arduino = serial.Serial("/dev/rfcomm0", baudrate=9600)

@app.route('/unlock', methods=['POST'])
def unlock_door():
    arduino.write(b'1')  # Send '1' to the Arduino to unlock the door
    return 'Door unlocked'
    
@app.route('/lock', methods=['POST'])
def lock_door():
    arduino.write(b'0')  # Send '0' to the Arduino to unlock the door
    return 'Door locked'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

print('model test starting')
import numpy as np
import socketio
import eventlet
from flask import Flask
import tensorflow as tf
import base64
from io import BytesIO
from PIL import Image
import cv2


sio = socketio.Server()
app = Flask(__name__) #'__main__'
max_speed = 10


def preprocessing_img(img):
    img = img[60:135,:,:]
    img = cv2.cvtColor(img,cv2.COLOR_BGR2YUV)
    img = cv2.GaussianBlur(img,(3,3),0)
    img = cv2.resize(img,(200,66))
    img = img/255
    return img


@sio.on('telemetry')
def telemetry(sid,data):
    speed = float(data['speed'])
    image = Image.open(BytesIO(base64.b64decode(data['image'])))
    image = np.asarray(image)
    image = preprocessing_img(image)
    image = np.array([image])
    steering = float(model.predict(image))
    throttle = 1.0 - speed/max_speed
    print(f"Steering:{steering}\nThrottle{throttle}\nSpeed{speed}")
    sendControl(steering,throttle)



@sio.on('connect')
def connect(sid,environ):
    print('connected')
    sendControl(0,0)



def sendControl(steering,throttle):
    sio.emit('steer', data={
        'steering_angle': steering.__str__(),
        'throttle': throttle.__str__()
    })


if __name__ == '__main__':
    model = tf.keras.models.load_model('Alastor.h5')
    app = socketio.Middleware(sio, app)
    eventlet.wsgi.server(eventlet.listen(('',4567)),app)

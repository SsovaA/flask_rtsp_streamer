from flask import Flask, Response, request, abort
import cv2

# Для камеры Geovision: rtsp://admin:admin@192.168.10.110:8554/CH001.sdp 
CAMERA_URL = ''

class VideoCamera(object):
    def __init__(self, address):
        self.video = cv2.VideoCapture(address)
    
    def __del__(self):
        self.video.release()
    
    def get_frame(self):
        _, frame = self.video.read()
        _, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()

app = Flask(__name__)

def gen_frame(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame)

@app.route('/live/')
def live():
    camera = VideoCamera(f'{CAMERA_URL}')
    return Response(gen_frame(camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port = '8000',  debug=True)

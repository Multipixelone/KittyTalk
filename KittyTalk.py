from flask import Flask, render_template, Response
import datetime
from Camera import VideoCamera
app = Flask(__name__)

@app.route("/")
def index():
   now = datetime.datetime.now()
   timeString = now.strftime('%I:%M:%S')
   templateData = {
      'title' : 'KittyTalk',
      'time': timeString,
      }
   return render_template('KittyTalk.html', **templateData)

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

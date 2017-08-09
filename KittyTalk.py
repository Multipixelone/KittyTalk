from flask import Flask, render_template, Response
import datetime
from Camera import VideoCamera
import flask_uwsgi_websocket as GeventWebSocket
app = Flask(__name__)
ws = GeventWebSocket(app)

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

@ws.route('/websocket')
def audio(ws):
   first_message = True
   total_msg = ""
   sample_rate = 0

   while True:
      msg = ws.receive()

      if first_message and msg is not None: # the first message should be the sample rate
         sample_rate = getSampleRate(msg)
         first_message = False
         continue
      elif msg is not None:
         audio_as_int_array = numpy.frombuffer(msg, 'i2')
         doSomething(audio_as_int_array)
      else:
         break

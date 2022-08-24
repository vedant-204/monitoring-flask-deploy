from flask import Flask
from datetime import datetime
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from prometheus_client import make_wsgi_app
from flask_prom import Prometheus
import  pytz
import os

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
Prometheus(app)


@app.route("/")
def hello():
    try:
        return "Hello World!"
    except:
        return "error occurred"


@app.route('/time')
def time():
    try:
        tz = pytz.timezone('Asia/Kolkata')
        time = datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')
        return time
    except:
        return "error occurred"


app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/metrics': make_wsgi_app()
})

# main driver function
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

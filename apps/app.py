from flask import Flask

app = Flask(__name__)
app.secret_key = 'supersecretkey'

from routes import *

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)

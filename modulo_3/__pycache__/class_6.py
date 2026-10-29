from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "<p>大家，今天去打羽毛球吗？不去就是不够意思啦!</p>"

<img src="images/"
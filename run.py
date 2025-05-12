from flask import Flask, render_template
from apis.url_shortener import url_api

app = Flask(__name__)
app.register_blueprint(url_api)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

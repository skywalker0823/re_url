from flask import Flask, request, redirect
import redis
import string
import random
import os

app = Flask(__name__)
r = redis.Redis(host='redis', port=6379, db=0)

def generate_short_id(length=6):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        long_url = request.form.get('url')
        if not long_url:
            return '請輸入URL'
        
        short_id = generate_short_id()
        r.set(short_id, long_url)
        domain = os.getenv('DOMAIN_NAME', 'localhost')
        protocol = 'https' if os.getenv('USE_HTTPS', 'true').lower() == 'true' else 'http'
        return f'短網址: {protocol}://{domain}/{short_id}'
    
    return '''
        <form method="POST">
            <input type="url" name="url" placeholder="請輸入網址">
            <input type="submit" value="縮短">
        </form>
    '''

@app.route('/<short_id>')
def redirect_to_url(short_id):
    long_url = r.get(short_id)
    if long_url:
        return redirect(long_url.decode('utf-8'))
    return '網址不存在'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

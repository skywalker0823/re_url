from flask import Blueprint, request, redirect, jsonify
import string
import random
import os
import redis

url_api = Blueprint('url_api', __name__)
r = redis.Redis(host='redis', port=6379, db=0)

def generate_short_id(length=6):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

@url_api.route('/', methods=['POST'])
def create_short_url():
    long_url = request.form.get('url')
    if not long_url:
        return jsonify({'error': '請輸入URL'})
    
    short_id = generate_short_id()
    r.set(short_id, long_url)
    domain = os.getenv('DOMAIN_NAME', 'localhost:5000')
    return jsonify({'short_url': f'http://{domain}/{short_id}'})

@url_api.route('/<short_id>')
def redirect_to_url(short_id):
    long_url = r.get(short_id)
    if long_url:
        return redirect(long_url.decode('utf-8'))
    return '網址不存在'

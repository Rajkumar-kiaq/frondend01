import os
import random
import string
from flask import Flask, Response, abort

app = Flask(__name__)

# This function automatically creates a fresh unique CloudFront Distribution ID for you
def generate_fresh_id():
    uppercase_elements = ''.join(random.choices(string.ascii_uppercase + string.digits, k=13))
    return f"E{uppercase_elements}"

DISTRIBUTION_ID = generate_fresh_id()
DIST_DIR = "./dist"

@app.route('/', defaults={'path': 'index.html'})
@app.route('/<path:path>')
def serve_cloudfront_native(path):
    # Dynamically tracking request using your freshly generated ID
    print(f"[Floci CloudFront Engine] Distribution ID: {DISTRIBUTION_ID} -> Requesting: {path}")
    
    file_path = os.path.join(DIST_DIR, path)
    
    if not os.path.exists(file_path) or os.path.isdir(file_path):
        file_path = os.path.join(DIST_DIR, 'index.html')
        
    try:
        if path.endswith('.html'): content_type = 'text/html'
        elif path.endswith('.css'): content_type = 'text/css'
        elif path.endswith('.js'): content_type = 'application/javascript'
        elif path.endswith('.svg'): content_type = 'image/svg+xml'
        else: content_type = 'text/html'
            
        with open(file_path, 'rb') as f:
            file_content = f.read()
            
        response = Response(file_content, mimetype=content_type)
        response.headers['X-Cache'] = 'Hit from CloudFront Local Emulator'
        response.headers['X-Amz-Cf-Id'] = DISTRIBUTION_ID
        response.headers['Server'] = 'CloudFront'
        return response
    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == '__main__':
    print(f"🚀 Floci CloudFront Engine Activated Successfully on Port 4566!")
    print(f"🎯 YOUR FRESH LOGICAL DISTRIBUTION ID: {DISTRIBUTION_ID}")
    print(f"👉 Open Browser Link: http://localhost:4566")
    app.run(host='0.0.0.0', port=4566, debug=True)

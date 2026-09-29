import boto3
from flask import Flask, Response, abort
from botocore.exceptions import ClientError

app = Flask(__name__)

BUCKET_NAME = "floci-bucket-1"
# Floci-la auto-generate aagadha naala, namma custom distribution ID configure panrom
DISTRIBUTION_ID = "ED7UQZ3MQM0H0" 

# Local Floci server connection mapping
s3_client = boto3.client(
    's3',
    endpoint_url='http://localhost:4566',
    region_name='ap-south-1',
    aws_access_key_id='mock_key',
    aws_secret_access_key='mock_secret'
)

@app.route('/', defaults={'path': 'index.html'})
@app.route('/<path:path>')
def serve_static_assets(path):
    print(f"[Floci CloudFront Routing] Using Dist ID: {DISTRIBUTION_ID} -> Requesting asset: {path}")
    try:
        s3_object = s3_client.get_object(Bucket=BUCKET_NAME, Key=path)
        
        # Proper web standard MIME target identification
        if path.endswith('.html'): content_type = 'text/html'
        elif path.endswith('.css'): content_type = 'text/css'
        elif path.endswith('.js'): content_type = 'application/javascript'
        elif path.endswith('.svg'): content_type = 'image/svg+xml'
        else: content_type = s3_object.get('ContentType', 'text/html')
            
        file_content = s3_object['Body'].read()
        response = Response(file_content, mimetype=content_type)
        
        # Real CloudFront headers simulation setup
        response.headers['X-Cache'] = 'Hit from local Floci Distribution Edge'
        response.headers['X-Amz-Cf-Id'] = DISTRIBUTION_ID
        return response
        
    except ClientError as e:
        if e.response['Error']['Code'] == "404":
            # Vite / React standard frontend app client router router fallback fallback config
            try:
                fallback_file = s3_client.get_object(Bucket=BUCKET_NAME, Key='index.html')
                return Response(fallback_file['Body'].read(), mimetype='text/html')
            except:
                abort(404)
        return f"Floci S3 service error context: {str(e)}", 500

if __name__ == '__main__':
    print(f"🌍 Local CloudFront Server listening on port 8080...")
    app.run(host='0.0.0.0', port=8080, debug=True)

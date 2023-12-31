from flask import Flask, render_template, jsonify
import boto3
import os

app = Flask(__name__)

# Access AWS credentials from environment variables
aws_access_key_id = os.environ.get('AKIAU3SMU4N4FLANWSAQ')
aws_secret_access_key = os.environ.get('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')
aws_region = os.environ.get('ap-south-1')

# Initialize S3 client
s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id,
                  aws_secret_access_key=aws_secret_access_key,
                  region_name=aws_region)

@app.route('/')
def index():
    try:
        # Replace 'your-bucket-name' with your actual bucket name and 'your-file-name.json' with your JSON file name
        bucket_name = 'productsfetch'
        file_name = 'productsfetch.json'

        # Fetch JSON file from S3 bucket
        obj = s3.get_object(Bucket=bucket_name, Key=file_name)
        data = obj['Body'].read().decode('utf-8')

        # Parse the JSON data
        parsed_data = json.loads(data)
        
        # Sort data by descending popularity
        sorted_data = sorted(parsed_data, key=lambda x: x['Popularity'], reverse=True)

        return render_template('index.html', products=sorted_data)
    
    except Exception as e:
        return f'Failed to fetch data: {str(e)}'

if __name__ == '__main__':
    app.run(debug=True)

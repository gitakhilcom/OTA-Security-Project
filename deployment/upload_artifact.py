# deployment/upload_artifact.py
import boto3

def upload_to_s3(file_path, bucket, key):
    s3 = boto3.client('s3')
    s3.upload_file(file_path, bucket, key)
    print(f"✅ Uploaded {file_path} to s3://{bucket}/{key}")

upload_to_s3("firmware.bin", "your-bucket-name", "releases/firmware.bin")

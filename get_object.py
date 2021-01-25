# Usage: python3 get_object.py copy_object new_key.dat
import sys
import urllib3
import os
import base64
from minio import Minio
from minio.sse import SseCustomerKey
from minio.error import S3Error

MINIO_URL = "10.7.2.207:9000"
BUCKET_NAME = "photos"
        
def sse_encryption(key):

    f = open(key, "r")

    key_str = f.read()
    key_str = key_str.replace('\n', '')
    key = key_str.encode('ascii')
    
    SSE = SseCustomerKey(key)

    return (SSE)

def main():
    
    # Get input file path from command line
    file_name = sys.argv[1]

    # Get Symmetric Decryption key path
    key_path = sys.argv[2]

    httpClient = urllib3.PoolManager(
                timeout=urllib3.Timeout.DEFAULT_TIMEOUT,
                        cert_reqs='CERT_REQUIRED',
                        ca_certs='/home/edimoulis/.minio/certs/public.crt',
                        retries=urllib3.Retry(
                            total=5,
                            backoff_factor=0.2,
                            status_forcelist=[500, 502, 503, 504]
                        )
            )

    client = Minio(MINIO_URL,
                    access_key='minio',
                    secret_key='minio123',
                    secure=True,
                    http_client=httpClient)


    # Make 'asiatrip' bucket if not exist.
    found = client.bucket_exists(BUCKET_NAME)
    if not found:
        client.make_bucket(BUCKET_NAME)
    else:
        print("Bucket " + BUCKET_NAME + " already exists.")

    # SSE Customer provided key encryption
    SSE = sse_encryption(key_path)

    output_filename = input("Save downloaded object as: ")
    
    # Download object
    client.fget_object(BUCKET_NAME, file_name, output_filename, ssec=SSE)



if __name__ == "__main__":
    try:
        main()
    except S3Error as exc:
        print("error occurred.", exc)

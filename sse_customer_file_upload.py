# Usage: python3 file_uploader.py /home/edimoulis/Master/Semester3/Security-of-Computer-Systems/Project/test.txt
import sys
import urllib3
import os
import base64
from minio import Minio
from minio.sse import SseCustomerKey
from minio.error import S3Error

MINIO_URL = "10.7.2.207:9000"
BUCKET_NAME = "photos"
AES_KEY = "/home/edimoulis/Master/Semester3/Security-of-Computer-Systems/Project/key.dat"
        

def sse_encryption():

    #key = base64.encode()
    key_str = 'MzJieXRlc2xvbmdzZWNyZXRrZXltdXN0'
    key = key_str.encode('ascii')
    SSE = SseCustomerKey(key)

    return (SSE)

def main():
    
    # Get input file path from command line
    file_name = sys.argv[1]

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
    SSE = sse_encryption()

    client.fput_object(
        BUCKET_NAME, file_name, file_name, sse=SSE
    )
    print(
        file_name + " is successfully uploaded as object " + str(file_name) + " to bucket: " + BUCKET_NAME
    )

    # Download the object again with SSE configuration
    client.fget_object(BUCKET_NAME, "README.md", "readmetest.txt", ssec=SSE)


if __name__ == "__main__":
    try:
        main()
    except S3Error as exc:
        print("error occurred.", exc)

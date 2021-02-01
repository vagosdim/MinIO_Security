# Usage: python3 list_objects.py

import sys
import base64
import urllib3
from minio import Minio
from minio.sse import SseCustomerKey
from minio.commonconfig import REPLACE, CopySource
from minio.error import S3Error

MINIO_URL = "10.7.2.207:9000"
BUCKET_NAME = "encrypted"
PUBLIC_CERTIFICATE = '/home/edimoulis/.minio/certs/public.crt'

def sse_encryption(key):

    key = key.encode('ascii')
    SSE = SseCustomerKey(key)

    return (SSE)

def main():

    httpClient = urllib3.PoolManager(
                timeout=urllib3.Timeout.DEFAULT_TIMEOUT,
                        cert_reqs='CERT_REQUIRED',
                        ca_certs=PUBLIC_CERTIFICATE,
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
    
    buckets = client.list_buckets()
    for bucket in buckets:
        print(bucket.name, bucket.creation_date)
    

if __name__ == "__main__":
    try:
        main()
    except S3Error as exc:
        print("error occurred.", exc)

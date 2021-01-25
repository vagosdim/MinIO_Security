# Usage: python3 object_re_encryption.py test.txt

import sys
import base64
import urllib3
from minio import Minio
from minio.sse import SseCustomerKey
from minio.commonconfig import REPLACE, CopySource
from minio.error import S3Error

MINIO_URL = "10.7.2.207:9000"
BUCKET_NAME = "photos"

OLD_AES_KEY = '638b7a2cd0748b7f395501b657bcb858'
NEW_AES_KEY = 'f7ff22264f628a669b1650270ee5672d'


def sse_encryption(key):

    key = key.encode('ascii')
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

    # Source object customer provided key
    SSE_SRC = sse_encryption(OLD_AES_KEY)
    
    # Deestination Object SSE Customer provided key encryption
    SSE_DST = sse_encryption(NEW_AES_KEY)

    # Copy the object to the same bucket using a different key
    # Object does not leave the server this way
    result = client.copy_object(
        BUCKET_NAME,
        file_name,
        CopySource(BUCKET_NAME, file_name, ssec=SSE_SRC),
        sse=SSE_DST,

    )
    print(result.object_name, result.version_id)


if __name__ == "__main__":
    try:
        main()
    except S3Error as exc:
        print("error occurred.", exc)
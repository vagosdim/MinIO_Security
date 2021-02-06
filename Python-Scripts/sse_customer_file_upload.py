# Usage: python3 sse_customer_file_upload.py /home/edimoulis/Master/Semester3/Security-of-Computer-Systems/Input/1KB.bin Keys/test_key.dat
import sys
import urllib3
import os
import base64
import time
import psutil
from minio import Minio
from minio.sse import SseCustomerKey
from minio.error import S3Error
from encryption_stats import *

MINIO_URL = "10.7.2.207:9000"
BUCKET_NAME = "encrypted"
PUBLIC_CERTIFICATE = '/home/edimoulis/.minio/certs/public.crt'

def sse_encryption(key):

    f = open(key, "r")

    key_str = f.read()
    key_str = key_str.replace('\n', '')
    key = key_str.encode('ascii')
    
    SSE = SseCustomerKey(key)

    return (SSE)

def measure_execution_time(client, BUCKET_NAME, file_name, file_path, SSE):

    samples = []
    cpu_usage = []
    ram_usage = []

    for i in range(100):
        start = time.time()
        client.fput_object(
            BUCKET_NAME, file_name, file_path, sse=SSE
        )
        cpu_usage.append(((psutil.cpu_percent(interval=None))))
        ram_usage.append(psutil.virtual_memory().percent)
        end = time.time()
        samples.append(end-start)
    
    export_system_stats(cpu_usage, ram_usage, file_name, 'cpu_percent_usage.csv')
    #export_stats_to_csv(samples, file_name, 'sse_encryption.csv')
    breakpoint()

    return

def main():
    
    # Get input file path from command line
    file_path = sys.argv[1]
    file_name = (file_path.split('/')[-1]).split(".")[0] + ".bin"

    # Get Symmetric Decryption key path
    key_path = sys.argv[2]

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


    # Make 'BUCKET_NAME' bucket if not exist.
    found = client.bucket_exists(BUCKET_NAME)
    if not found:
        client.make_bucket(BUCKET_NAME)
    else:
        print("Bucket " + BUCKET_NAME + " already exists.")

    # SSE Customer provided key encryption
    SSE = sse_encryption(key_path)
    
    measure_execution_time(client, BUCKET_NAME, file_name, file_path, SSE)
    result = client.fput_object(
        BUCKET_NAME, file_name, file_path, sse=SSE
    )

    print(
        file_name + " is successfully uploaded as object " + str(file_name) + " to bucket: " + BUCKET_NAME
    )

    # Download the object again with SSE configuration
    # output_filename = input("Save downloaded object as: ")
    # client.fget_object(BUCKET_NAME, file_name, output_filename, ssec=SSE)


if __name__ == "__main__":
    try:
        main()
    except S3Error as exc:
        print("error occurred.", exc)

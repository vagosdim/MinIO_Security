# Usage: python3 file_uploader.py /home/edimoulis/Master/Semester3/Security-of-Computer-Systems/Project/test.txt
import sys
import urllib3
import ctypes
import os
from minio import Minio
from minio.error import S3Error
from ctypes import *

MINIO_URL = "10.7.2.207:9000"
BUCKET_NAME = "photos"
AES_KEY = "/home/edimoulis/Master/Semester3/Security-of-Computer-Systems/Project/key.dat"

class go_string(Structure):
    _fields_ = [
        ("p", c_char_p),
        ("n", c_int)]
        

def encrypt(file_path, file_name, AES_KEY):

    lib = cdll.LoadLibrary('./libencrypt.so')
    lib.encrypt.restype = c_char_p
    
    fp = go_string(c_char_p(file_path.encode('utf-8')), len(file_path))
    key = go_string(c_char_p(AES_KEY.encode('utf-8')), len(AES_KEY))
    file_name = go_string(c_char_p(file_name.encode('utf-8')), len(file_name))

    encrypted_file_name = lib.encrypt(fp, file_name, key)

    return encrypted_file_name

def main():
    
    # Get input file path from command line
    file_path = sys.argv[1]

    # Extract only the name of the file without the ending ex/ "test.txt" --> "test"
    file_name = (file_path.split("/")[-1]).split(".")[0]
    file_name = encrypt(file_path, file_name, AES_KEY)

    # Create a client with the MinIO server playground, its access key
    # and secret key.
    #client = Minio(
    #    MINIO_URL,
    #    access_key="minio",
    #    secret_key="minio123",
    #    secure=False,
    #)

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

    client.fput_object(
        BUCKET_NAME, file_name, file_name,
    )
    print(
        file_path + " is successfully uploaded as object " + str(file_name) + " to bucket: " + BUCKET_NAME
    )


if __name__ == "__main__":
    try:
        main()
    except S3Error as exc:
        print("error occurred.", exc)

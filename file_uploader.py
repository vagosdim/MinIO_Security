# Usage: python3 file_uploader.py ~/Pictures/dd.png
import sys
import urllib3
from minio import Minio
from minio.error import S3Error

MINIO_URL = "10.7.2.207:9000"
BUCKET_NAME = "photos"

def main():
    
    # Get input file path from command line
    file_path = sys.argv[1]
    file_name = file_path.split("/")[-1]

    # Create a client with the MinIO server playground, its access key
    # and secret key.
    #client = Minio(
    #    MINIO_URL,
    #    access_key="minio",
    #    secret_key="minio123",
    #    secure=True,
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

    # Upload '/home/user/Photos/asiaphotos.zip' as object name
    # 'asiaphotos-2015.zip' to bucket 'asiatrip'.
    client.fput_object(
        BUCKET_NAME, file_name, file_path,
    )
    print(
        file_path + " is successfully uploaded as object " + str(file_name) + " to bucket: " + BUCKET_NAME
    )


if __name__ == "__main__":
    try:
        main()
    except S3Error as exc:
        print("error occurred.", exc)

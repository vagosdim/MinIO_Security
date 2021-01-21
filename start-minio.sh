#!/bin/bash

# States if we want to build minio
BUILD_FLAG=$1

# Go to minio folder
cd "minio-master"

if [ "$BUILD_FLAG" = "build" ]; then
	# Build minio for changes, only several seconds
	make;
fi

# Export credentials
export MINIO_ROOT_USER=minio
export MINIO_ROOT_PASSWORD=minio123

# Start the server
./minio server /mnt/data

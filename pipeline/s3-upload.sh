#!/bin/bash

# Set the S3 bucket name
S3_BUCKET_NAME="alex-choi-ucl-test-1"

# Loop through all .json files in the current directory
for file in *.json
do
  # Copy the file to the S3 bucket using the AWS CLI
  aws s3 cp "$file" "s3://$S3_BUCKET_NAME/"
done

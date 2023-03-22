#!/bin/bash

# Set the S3 bucket name
S3_BUCKET_NAME="***REMOVED***"

# Create the archive directory if it does not exist
if [ ! -d "archive" ]
then
  mkdir archive
  echo "Archive directory created."
fi

# Loop every hour
while true
do
  # Loop through all .json files in the output directory
  for file in output/*.json
  do
    # Copy the file to the S3 bucket using the AWS CLI
    aws s3 cp "$file" "s3://$S3_BUCKET_NAME/"

    # Move the file to the archive folder
    mv "$file" archive/
    echo "Moved $file to archive/"
  done
  
  echo "All files moved to S3 and archive."
  
  # Sleep for an hour before looping again
  sleep 3600
done

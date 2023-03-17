import os
import json
import boto3
from pymongo import MongoClient

def lambda_handler(event, context):
    # AWS S3 configuration
    s3 = boto3.client('s3')
    bucket_name = '***REMOVED***'
    file_keys = {
        'hotels.json': 'hotels',
        'train.json': 'train',
        'tweets.json': 'tweets',
        'uber.json': 'uber',
        'weather.json': 'weather',
        'routes.json': 'routes'
    }

    # MongoDB configuration
    mongodb_uri = "***REMOVED***"

    # Connect to MongoDB
    try:
        client = MongoClient(mongodb_uri)
        db = client.group_db
    except Exception as e:
        print(f"Error connecting to MongoDB: {str(e)}")
        return {"statusCode": 500, "body": json.dumps({"message": "Error connecting to MongoDB"})}

    for file_key, collection_name in file_keys.items():
        # Check if collection exists
        if collection_name not in db.list_collection_names():
            print(f"Skipping non-existent collection: {collection_name}")
            continue

        collection = db[collection_name]

        # Download the JSON file from S3
        try:
            s3_object = s3.get_object(Bucket=bucket_name, Key=file_key)
            json_data = json.loads(s3_object['Body'].read().decode('utf-8'))
        except Exception as e:
            print(f"Error downloading file from S3: {str(e)}, skipping file: {file_key}")
            continue

        # Insert JSON data into MongoDB collection
        try:
            collection.insert_many(json_data)
            print(f"Data successfully inserted into MongoDB collection: {collection_name}")
        except Exception as e:
            print(f"Error inserting data into MongoDB: {str(e)}, skipping file: {file_key}")

    client.close()
    return {"statusCode": 200, "body": json.dumps({"message": "Processing completed"})}

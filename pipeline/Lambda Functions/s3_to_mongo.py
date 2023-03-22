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
        'routes.json': 'routes',
        'coordinates_hotel.json': 'coordinates_hotel',
        'coordinates_train.json': 'coordinates_train'
    }

    # MongoDB configuration
    mongodb_uri = "***REMOVED***"

    # Connect to MongoDB
    try:
        client = MongoClient(mongodb_uri)
        db = client.group_db
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"message": f"Error connecting to MongoDB: {str(e)}"})}

    logs = []
    available_files = []
    for file_key, collection_name in file_keys.items():
        # Check if collection exists
        if collection_name not in db.list_collection_names():
            logs.append(f"Skipping non-existent collection: {collection_name}")
            continue

        collection = db[collection_name]

        # Download the JSON file from S3
        try:
            s3_object = s3.get_object(Bucket=bucket_name, Key=file_key)
            raw_json_data = json.loads(s3_object['Body'].read().decode('utf-8'))

            if file_key == 'routes.json':
                json_data = [{'route_id': k, **v} for k, v in raw_json_data.items()]
            elif file_key == 'tweets.json':
                json_data = raw_json_data['data'] if 'data' in raw_json_data else raw_json_data
            else:
                json_data = raw_json_data

            available_files.append(file_key)
        except Exception as e:
            logs.append(f"No file found for collection '{collection_name}' on S3, skipping file: {file_key}")
            continue

        # Insert JSON data into MongoDB collection
        successful_inserts = 0
        for document in json_data:
            try:
                collection.insert_one(document)
                successful_inserts += 1
            except Exception as e:
                logs.append(f"Error inserting document into MongoDB: {str(e)}, document: {document}")

        logs.append(f"{successful_inserts} documents successfully inserted into MongoDB collection: {collection_name}")

    logs.append("Available files on S3:")
    for file in available_files:
        logs.append(f" - {file}")

    client.close()
    return {"statusCode": 200, "body": json.dumps({"message": "Processing completed", "logs": logs})}

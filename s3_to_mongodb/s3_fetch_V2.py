
#set up the environment
import subprocess
import os
import json
import pandas as pd
import boto3

os.environ['SPARK_VERSION'] = 'spark-3.2.3'
os.environ['HADOOP_VERSION'] = '3.3.1'

print(os.environ['SPARK_VERSION'])

#install libtinfo6

subprocess.call(["sudo", "apt-get", "install", "libtinfo6"])

#update package list and to make sure that the system is up-to-date
subprocess.call(["sudo", "apt-get", "update"])


#install OpenJDK 8

subprocess.call(["sudo", "apt-get", "install", "-y", "openjdk-8-jdk-headless", "-qq", ">", "/dev/null"])

#download spark
url = "https://downloads.apache.org/spark/{}/{}-bin-hadoop{}.tgz".format(os.environ['SPARK_VERSION'], os.environ['SPARK_VERSION'], os.environ['HADOOP_VERSION'])
subprocess.call(["wget", "-q", url])

#extract the contents of the downloaded spark file to the current directory. This will make spark binaries and libraries available

subprocess.call(["tar", "xf", "{}-bin-hadoop{}.tgz".format(os.environ['SPARK_VERSION'], os.environ['HADOOP_VERSION'])])

#install awscli and s3fs

subprocess.call(["pip", "install", "awscli"])

subprocess.call(["pip", "install", "s3fs"])

#display the path to java 
#java_path = os.path.join(os.environ["JAVA_HOME"], "bin", "java")
#check the version of java
#subprocess.call([java_path, "-version"])

java_home = "/usr/lib/jvm/java-8-openjdk-amd64"
subprocess.Popen(["export", "JAVA_HOME={}".format(java_home)], shell=True)

java_home = "/usr/lib/jvm/java-8-openjdk-amd64"
os.environ["JAVA_HOME"] = java_home

#update the system path environment variable to include the location of java
os.environ["PATH"] += os.pathsep + os.path.join(os.environ["JAVA_HOME"], "bin")

#display the new path environment variable
subprocess.call(["echo", "$PATH"])

#display the spark version
subprocess.call(["echo", "$SPARK_VERSION"])

#install findspark and pyspark
subprocess.call(["pip", "install", "-q", "findspark"])
subprocess.call(["pip", "install", "pyspark"])

#check the version of python
subprocess.call(["python", "--version"])

#set JAVA_HOME path
os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-8-openjdk-amd64"


#update the path so it includes the location of the spark binaries and libraries
os.environ["PATH"] += os.pathsep + "/project/AWS/spark-3.3.2-bin-hadoop3/bin"

#initialize findspark

import findspark
findspark.init()

#get the spark mongo connector
subprocess.call(["wget", "https://repo1.maven.org/maven2/org/mongodb/spark/mongo-spark-connector_2.13/10.1.1/mongo-spark-connector_2.13-10.1.1-all.jar"])

#install a mongodb database if one is needed
subprocess.call(["sudo", "apt-get", "install", "-y", "mongodb"])


#check mongo version
subprocess.call(["mongod", "--version"])

#move hadoop-aws-3.3.1.jar  to the jars directory of the spark installation

source_path = "hadoop-aws-3.3.1.jar"
destination_path = os.path.join(os.environ["SPARK_HOME"], "jars", "hadoop-aws-3.3.1.jar")
subprocess.call(["mv", source_path, destination_path])

#download hadoop-aws-3.3.1.jar from the maven repository

subprocess.call(["wget", "https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.3.1/hadoop-aws-3.3.1.jar"])

#define a function to fetch data from S3


def load_s3_files(bucket_name, prefix='', delimiter='/', aws_access_key_id=None, aws_secret_access_key=None):
    #create S3 client
    s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

    #list objects in the S3 bucket with the prefix and delimiter
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix, Delimiter=delimiter)

    #create an empty dictionary to store the dataframes
    dataframes = {}

    #for each file in the bucket, load it into a Pandas DataFrame and add it to the dictionary
    for obj in response.get('Contents', []):
        file_key = obj.get('Key')
        if file_key.endswith('.json'):
            df_name = file_key.split('/')[-1].split('.')[0]
            file_obj = s3.get_object(Bucket=bucket_name, Key=file_key)
            file_content = file_obj['Body'].read().decode('utf-8')
            try:
                df = pd.read_json(file_content, lines=True)
                #check if the object is a dataframe and convert it to a dictionary if necessary
                if isinstance(df, pd.DataFrame):
                    dataframes[df_name] = df.to_dict()
            except ValueError:
                continue

    #write the dictionary to a JSON file
    with open('dataframes.json', 'w') as f:
        json.dump(dataframes, f, indent=4)

    return dataframes


#load files 

***REMOVED***

#create a spark session

from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("ReadJSON")\
        .config("spark.jars", "/project/AWS/mongo-spark-connector_2.13-10.1.1-all.jar") \
        .getOrCreate()

#read the file with spark and create a spark dataframe
df = spark.read.json('/project/AWS/dataframes.json')


#make sure that the mongo-spark-connector JAR file is included in the spark application

os.environ['PYSPARK_SUBMIT_ARGS'] = '--jars /project/AWS/mongo-spark-connector_2.13-10.1.1-all.jar'

#install pymongo

subprocess.call(["pip", "install", "pymongo"])

#check if the server is reachable

from pymongo import MongoClient
client = MongoClient('***REMOVED***')


try:
    client.server_info()
    print("Connection successful!")
except Exception as e:
    print("Connection failed:", e)


# Connect to the database
db = client['group_db']

# Load the contents of the JSON file as a Python dict
with open('dataframes.json', 'r') as f:
    data = json.load(f)

# Insert a document into a collection
collection = db['collection_1']
collection.insert_one(data)
















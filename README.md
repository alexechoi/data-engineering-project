# Data Engineering Project
This is the group project for Data Engineering

There are several systems within this repository to build a data pipeline that revolves around Uber rides and pricing in London.

These include Uber, Weather, Hotels, Trains and Twitter which are scheduled to call these APIs or webscrape. We use a shell script to upload this data to S3 periodically. Then we use Lambda functions to integrate this into a MongoDB database. From that we used Lambda again to transform the data to Postgres before converting to Parquet and Pandas. You can view the entire process in the DemoPipeline.ipynb file.

To replicate this project you could deploy the Lambda functions by zipping the contents of each folder and uploading to AWS and set a trigger such as CloudWatch.
To replicate postgres you could upload the schema file in this repo to a service such as RDS.

In this project we use the schedule.py script to automate the calling of all our functions.

You can demo this pipeline using the demo notebook in this repository
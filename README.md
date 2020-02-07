# migrat
Migration to S3Bucket
Script is used to migrate files from tilda to s3 bucket, copying js, css files with html pages and images.
Several variables should br changed for script to work: public and secret keys for tilda API, project ID of your website and bucket name on AWS.
Plus, there is an YAML configuration file for CloudFormation.

The whole process is next: 
1. One S3Bucket is created in advance for migration script with its dependecies.
2. YAML file is given to CloudFormation to create all other services: roles, S3Bucket, REST API, Lambda Functions and CloudFront.
3. One Lambda is for script itself, another is used to call the migration process.
4. Migration is triggered by REST API POST request, all files are checked on tilda and if there is any difference - new files are uploaded to S3Bucket.

## Implementing bulk CSV ingestion to Amazon DynamoDB

References / sources:
  https://aws.amazon.com/blogs/database/implementing-bulk-csv-ingestion-to-amazon-dynamodb/
  https://github.com/aws-samples/csv-to-dynamodb

To ingest the data, complete the following steps:

1.  On the AWS CloudFormation console, choose Create stack.
2.  Choose With new resources (standard).
3.  In the Specify template section, for Template source, choose Upload a template file.
4.  Choose Choose File.
5.  Choose the CloudFormation template file you downloaded previously.
6.  Choose Next.

7.  In the Specify stack details section, for Stack name, enter a name for your stack.
8.  For Parameters, enter parameter names for the following resources:
      BucketName – S3 bucket name where you upload your CSV file.
      The bucket name must be a lowercase, unique value, or the stack creation fails.
      DynamoDBTableName – DynamoDB table name destination for imported data.
      FileName – CSV file name ending in .csv that you upload to the S3 bucket for insertion into the DynamoDB table.
9.  Choose Next

10.  Choose Next again.
11.  Select I acknowledge that AWS CloudFormation might create IAM resources.
12.  Choose Create Stack.
13.  When the stack is complete, navigate to your newly created S3 bucket and upload your CSV file.
      The upload triggers the import of your data into DynamoDB. However, you must make sure that your CSV file adheres to the following requirements:
      Structure your input data so that the partition key is located in the first column of the CSV file. Make sure that the first column of your CSV file is named uuid. For more information about selecting a partition key according to best practices, see Choosing the Right DynamoDB Partition Key.
      Confirm that your CSV file name matches the exact file name, which ends in .csv suffix, that you entered previously.
      For a 100,000 row-long file, this execution should take approximately 80 seconds. The Lambda function timeout can accommodate about 1 million rows of data; however, you should break up the CSV file into smaller chunks. Additionally, this solution does not guarantee the order of data imported into the DynamoDB table. If the execution fails, make sure that you have created and set your environment variables correctly, as specified earlier. You can also check the error handling messages in the Lambda function console.

14.  On the DynamoDB console, choose Tables.
15.  Choose the table you entered in your CloudFormation template for DynamoDBTableName.
      You can now view your imported data and associated table details.

-------------------------------------------------------------------------------------------------------------------------------------------------

This repository is used in conjunction with the following blog post:

You can use your own CSV file or download the test file we provided in this repo.

Steps to Download CloudFormation template:
1. Navigate to CloudFormation folder in this repo.
2. Click on CSVToDynamo.template.
3. Click on the Raw button.
4. Save Page As > Remove any file extensions so that the file reads like "CSVToDynamo.template". Click save.


## License

This library is licensed under the MIT-0 License. See the LICENSE file.

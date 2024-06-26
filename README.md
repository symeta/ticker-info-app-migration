# ticker-info-app-migration

## Migration Diagram

   <img width="730" alt="image" src="https://github.com/symeta/ticker-info-app-migration/assets/97269758/2226b996-fbb7-4ad1-80b0-29d45bb32ea9">



## Data Pre-processing Module Development & Ticker Info Application Upgrade

Both Data Pre-processing Module Development (**Task1**) and Ticker Info Application Upgrade (**Task2**) need to deal with read/write Docdb instance via Java.

DocumentDB Connection via Java is per link below:
 - [DocumentDB Connection for Java](https://github.com/aws-samples/amazon-documentdb-samples/blob/master/samples/app-config/src/main/java/com/example/app/DocumentDBConnection.java)

DocumentDB Client via Java Sample Code is per link below:
 - [DocumentDB Client for Java](https://github.com/aws-samples/amazon-documentdb-samples/blob/master/samples/app-config/src/main/java/com/example/app/DocumentDBClient.java)

DocumentDB Java SDK is per link below:
 - [DocumentDB Java SDK](https://sdk.amazonaws.com/java/api/latest/software/amazon/awssdk/services/docdb/package-summary.html)

Ticker Info Application Upgrade (**Task2**) also needs to deal with read/write ElastiCache for Redis instance via Java

ElastiCache for Redis Client via Java is per link below:
 - [ElastiCache for Redis Client for Java](https://docs.aws.amazon.com/AmazonElastiCache/latest/mem-ug/AutoDiscovery.Using.ModifyApp.Java.html)

ElastiCache for Redis Client via Java Sample Code is per link below:
 - [ElastiCache for Redis Client for Java](https://github.com/aws-samples/amazon-ElastiCache-redis-and-memcached-java-client-examples)

ElastiCache for Redis Java SDK is per link below:
 - [ElastiCache for Redis Java SDK](https://sdk.amazonaws.com/java/api/latest/software/amazon/awssdk/services/ElastiCache/package-summary.html)

## Migrate Existing Data from Self-built Redis to ElastiCache for Redis Instance

There are two ways to achieve **Task3**-Migrate Existing Data from Self-built Redis to ElastiCache for Redis Instance.
**Do Implement Migration durign Migration Window**

- **Method1:** via Elastiche for Redis built-in Data Migration Job
  - Create ElastiCache for Redis cluster via AWS console or CLI
  - Choose Migrate Data from Endpoint via Cluster Console
     <img width="570" alt="image" src="https://github.com/symeta/ticker-info-app-migration/assets/97269758/f058fbd1-415d-4f48-a9a3-aed414566763">
    
  - Configure Source Redis Endpoint Information and Star Migration
     <img width="570" alt="image" src="https://github.com/symeta/ticker-info-app-migration/assets/97269758/1f4b6532-95aa-4083-9a8e-bcf696e22b80">


- **Method2:** via File Dumpling and Upload
  - Create an S3 Bucket
  - Create Redis Backup via BGSAVE or SAVE, and upload the Backup to S3 bucket
  - Make sure ElastiCache Cluster has the permission to read the RDB file. If not, give the right permission to ElastiCache Cluster
  - Restore RDB file data to the ElastiCache Cluster
  
     <img width="512" alt="image" src="https://github.com/symeta/ticker-info-app-migration/assets/97269758/88bea460-73f6-43dc-ba84-ab2b00f6f39c">


  The detailed implementation guidance could be referred per [Seeding a Self-designed Cluster with a Backup](https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/backups-seeding-redis.html)



## Migrate Existing Data from Self-built Mysql to DocDB via DMS
**Task4.1**-Migrate Existing Data from Self-built Mysql to DocDB via DMS

could refer to [this blog](https://aws.amazon.com/cn/blogs/database/migrating-relational-databases-to-amazon-documentdb-with-mongodb-compatibility/) for Detailed Implementation Guide.

Besides the guidance, there are **3 points** that need to highlight:

**1st:**
 - as a preparation job for the latter **Task4.2**-Merge Multiple Ticker Data Table into One DocDB Table, you must alter all target mysql table by adding a NULL field named '_id'. The specific SQL command is shown below:
 
```sql
ALTER TABLE <target table name> ADD COLUMN _id varchar(20) NULL;
```

The field _id will be the primary key. During DMS task, _id will be fulfilled with global unique values. Index does not migrate, index needs to be re-built on the merged table (operatoin guidance could be referred per 'Create Index on the merged table' section)

**2nd:**
 - do not use 'rds-combined-ca-bundle.pem' mentioned in the blog (as shown in the first snapshot below). Instead, use 'global-bundle.pem' appeared in [ec2 connect docdb manually](https://docs.aws.amazon.com/documentdb/latest/developerguide/connect-ec2-manual.html)(as shown in the second snapshot below)
 

   <img width="639" alt="image" src="https://github.com/symeta/ticker-info-app-migration/assets/97269758/e9763b45-9a4c-4ad6-9b01-673f05f07c8a">



   <img width="639" alt="image" src="https://github.com/symeta/ticker-info-app-migration/assets/97269758/95deca29-9ead-4285-81cc-3b28e2586201">



 - command to get global-bundle.pem

 ```cmd
 wget https://truststore.pki.rds.amazonaws.com/global/global-bundle.pem
 ```


**3rd:**
 - when try to connect the docdb instance via ec2 console, make sure the ec2 is provisioned using Amazon Linux2 AMI. Because Amazon Linux2 has pre-installed relevant packages/libraries used for mongo shell

   <img width="639" alt="Screenshot 2024-06-23 at 18 42 53" src="https://github.com/symeta/ticker-info-app-migration/assets/97269758/c7d2d737-7ab9-4b7b-8625-29c7d013b1e7">


- the detailed implementation guide of how to connect to docdb instance via ec2 console is shown in [ec2 connect docdb manually](https://docs.aws.amazon.com/documentdb/latest/developerguide/connect-ec2-manual.html)

After successfully accomplishing DMS task, use the below command to check whether the original data in Mysql has been migrated to Docdb.

```mongosh
#show all the schema in the docdb instance
show dbs

#switch schema to the target schema
use <target schema name>

#show all tables under target schema
db.getCollectionNames()

#show one record of a table
db.<specific collection name>.find()

#count the records numer of a table
db.<specific collection name>.count()
```


## Merge Multiple Ticker Data Table into One DocDB Table
**Task4.2**-Merge Multiple Ticker Data Table into One DocDB Table. The steps are as follows:
 - Extract the data in the target docdb schema collections (mongodb table) into json file via [export.py](https://github.com/symeta/ticker-info-app-migration/blob/main/export.py)
 - Create a new collection using the extracted files generated in the 1st step via python [import.py](https://github.com/symeta/ticker-info-app-migration/blob/main/import.py)
 - Create Index on the merged table
 ```mongosh
 db.timetrend_merged.createIndex( { "instrumentId": 1, "EndTime": 1 },{ unique: true } )

 db.timetrend_merged.getIndexes()
 ```

**One point needs to lighlight:**
mongoexport/mongoimport install command:

```sh
sudo yum install mongodb-org-tools
```






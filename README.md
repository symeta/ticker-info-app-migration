# ticker-info-app-migration

## Migration Diagram

<img width="639" alt="image" src="https://github.com/symeta/ticker-info-app-migration/assets/97269758/58faace9-0712-4ce0-8c8d-7d7149ec9589">


## Data Pre-processing Module Development & Ticker Info Application Upgrade

Both Data Pre-processing Module Development (Task1) and Ticker Info Application Upgrade (Task2) need to deal with read/write Docdb instance via Java.

DocumentDB Connection via Java is per link below:
 - [DocumentDB Connection for Java](https://github.com/aws-samples/amazon-documentdb-samples/blob/master/samples/app-config/src/main/java/com/example/app/DocumentDBConnection.java)

DocumentDB Client via Java Sample Code is per link below:
 - [DocumentDB Client for Java](https://github.com/aws-samples/amazon-documentdb-samples/blob/master/samples/app-config/src/main/java/com/example/app/DocumentDBClient.java)

DocumentDB Java SDK is per link below:
 - [DocumentDB Java SDK](https://sdk.amazonaws.com/java/api/latest/software/amazon/awssdk/services/docdb/DocDbClient.html)


## Migrate Existing Data from Self-built Redis to Elasticache for Redis Instance

There are two ways to achieve Task3-Migrate Existing Data from Self-built Redis to Elasticache for Redis Instance.

- via Elastiche for Redis built-in Data Migration Job
  - Create Elasticache for Redis cluster via AWS console or CLI
  - Choose Migrate Data from Endpoint via Cluster Console
  - Configure Source Redis Endpoint Information and Star Migration

  ![redis0](https://github.com/symeta/ticker-info-app-migration/assets/97269758/f058fbd1-415d-4f48-a9a3-aed414566763)

  ![redis1](https://github.com/symeta/ticker-info-app-migration/assets/97269758/1f4b6532-95aa-4083-9a8e-bcf696e22b80)

- via File Dumpling and Upload
  - Implement Migration durign Migration Window
  - Create an S3 Bucket
  - Create Redis Backup via BGSAVE or SAVE, and upload the Backup to S3 bucket
  - Make sure Elasticache Cluster has the permission to read the RDB file. If not, give the right permission to Elasticache Cluster
  - Restore RDB file data to the Elasticache Cluster
  ![redis2](https://github.com/symeta/ticker-info-app-migration/assets/97269758/52735123-16b6-4158-9c1c-c00b5242aca5)



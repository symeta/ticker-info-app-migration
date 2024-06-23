# ticker-info-app-migration

## Migration Diagram



## Data Pre-processing Module Development & Ticker Info Application Upgrade

Both Data Pre-processing Module Development (Task1) and Ticker Info Application Upgrade (Task2) need to deal with read/write Docdb instance via Java.

DocumentDB Connection via Java is per link below:
 - [DocumentDB Connection for Java](https://github.com/aws-samples/amazon-documentdb-samples/blob/master/samples/app-config/src/main/java/com/example/app/DocumentDBConnection.java)

DocumentDB Client via Java Sample Code is per link below:
 - [DocumentDB Client for Java](https://github.com/aws-samples/amazon-documentdb-samples/blob/master/samples/app-config/src/main/java/com/example/app/DocumentDBClient.java)

DocumentDB Java SDK is per link below:
 - [DocumentDB Java SDK](https://sdk.amazonaws.com/java/api/latest/software/amazon/awssdk/services/docdb/DocDbClient.html)


## Migrate Existing Data from Self-built Redis to Elasticache for Redis Instance

There are two ways to achieve Task3:Migrate Existing Data from Self-built Redis to Elasticache for Redis Instance.

- via Elastiche for Redis built-in Data Migration Job
  - Create Elasticache for Redis cluster via AWS console or CLI
  - Choose Migrate Data from Endpoint via Cluster Console
  - Configure Source Redis Endpoint Information and Star Migration
  
  
- via File Dumpling and Upload


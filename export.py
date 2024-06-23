import os
from pymongo import MongoClient

#MongoDB Connection Info 
host = "docdb-bbae-ticker.cluster-ckijl4cofaxc.us-east-1.docdb.amazonaws.com"
username = "bbaeadmin"
password = "Huawei12#$"
database_name = "docdb-bbae"

#Create MongoDB Client
client = MongoClient(f"mongodb://{username}:{password}@{host}/{database_name}?tls=true&tlsCAFile=global-bundle.pem")


#Get Database Object
db = client[database_name]

#Get Collections List
collections = db.list_collection_names()

#for each collection execute mongoexport
for collection in collections:
    output_file = f"{collection}.json"
    command = f"mongoexport --ssl \
    --host=docdb-bbae-ticker.cluster-ckijl4cofaxc.us-east-1.docdb.amazonaws.com:27017 \
    --collection={collection} \
    --db=docdb-bbae \
    --out={output_file} \
    --username=bbaeadmin \
    --password=Huawei12#$ \
    --sslCAFile global-bundle.pem"
    os.system(command)
    print(f"Exported collection {collection} to {output_file}")

client.close()
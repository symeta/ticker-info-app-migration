import os
import subprocess

host = "docdb-bbae-ticker.cluster-ckijl4cofaxc.us-east-1.docdb.amazonaws.com"
username = "bbaeadmin"
password = "Huawei12#$"
database_name = "docdb-bbae"
collection_name = "tickdata_new"

json_dir = "/root/export_file"

for filename in os.listdir(json_dir):
    if filename.endswith(".json"):
        file_path = os.path.join(json_dir, filename)
        command = f"mongoimport --ssl \
        --host={host} \
        --collection={collection_name} \
        --file={file_path} \
        --db={database_name} \
        --username={username} \
        --password={password} \
        --sslCAFile global-bundle.pem"

        try:
            subprocess.run(command, shell=True, check=True)
            print(f"Imported data from {filename}")
        except subprocess.CalledProcessError as e:
            print(f"Error importing {filename}: {e}")
import os
from azure.storage.blob import BlobServiceClient

with open("resources.txt") as f:
    resource_list = f.readlines()
    resource_list = [x.strip() for x in resource_list]

def upload_blob(connect_str, file_name):
    # Create the BlobServiceClient object
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    container_name = "data"
    # Create a blob client
    blob_client = blob_service_client.get_blob_client(
        container=container_name, blob=file_name
    )
    # Upload the created file
    with open(file=file_name, mode="rb") as data:
        blob_client.upload_blob(data, overwrite=True)
    return 0

def upload_to_azure(connect_str):
    for resource in resource_list:
        if os.path.isfile(resource):
            upload_blob(connect_str, resource)
        else:
            print(f"File {resource} not found.")

if __name__ == "__main__":
    connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
    upload_to_azure(connect_str)
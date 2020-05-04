from google.cloud import storage
from google.oauth2 import service_account

KEY='image-location-finder-43db266d7800.json'
PROJECT='image-location-finder'
credentials = service_account.Credentials.from_service_account_file(KEY)
storage_client = storage.Client(PROJECT,credentials)

# List objects in a bucket
blobs = storage_client.list_blobs("image-finder-datafiles")

for blob in blobs:
    print(blob.name)
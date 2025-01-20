from appwrite.client import Client
from appwrite.services.databases import Databases


client = Client()

client.set_endpoint('https://cloud.appwrite.io/v1') # Your API Endpoint
client.set_project('678df87a00219b30c15f') # Your project ID
client.set_key('standard_875cfa0696fedf2880fb45665b6d580a83612889ce7e002c43d93878f166c36a631a3578cc9dfd989a1020dd60eb0bcb1062dc96fe01c4b77bf2695d756222b9adddbc1a1638b3f88ee34100585d1ae221976647dc47636fabab3ddeac5d50a57663bb7efcf4193ccb4e06ef688d3c5f60db879e4fae65f5848f552883a22dfa')

# Initialize the Databases service
databases = Databases(client)

# List all documents in a collection
try:
    documents = databases.list_documents(
        database_id="NUMBERPLATE",
        collection_id='DATA',  # Your collection ID
        
    )
    
    # Loop through the documents and get both IDs and data
    for doc in documents['documents']:
        document_id = doc['$id']
        document_data = doc  # The full document data (including fields)
        
        print(f"Document ID: {document_id}")
        print(f"Document Data: {document_data}")
        print("-" * 50)
except Exception as e:
    print('Error:', e)

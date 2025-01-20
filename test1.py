from appwrite.client import Client
from appwrite.services.databases import Databases


client = Client()

client.set_endpoint('') # Your API Endpoint
client.set_project('') # Your project ID
client.set_key('')

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

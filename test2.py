import pandas as pd
from appwrite.client import Client
from appwrite.services.databases import Databases
from dotenv import load_dotenv
import os



# Initialize Appwrite Client
client = Client()
client.set_endpoint('https://cloud.appwrite.io/v1') # Your API Endpoint
client.set_project('678df87a00219b30c15f') # Your project ID
client.set_key('standard_875cfa0696fedf2880fb45665b6d580a83612889ce7e002c43d93878f166c36a631a3578cc9dfd989a1020dd60eb0bcb1062dc96fe01c4b77bf2695d756222b9adddbc1a1638b3f88ee34100585d1ae221976647dc47636fabab3ddeac5d50a57663bb7efcf4193ccb4e06ef688d3c5f60db879e4fae65f5848f552883a22dfa')



# Initialize the Databases service
databases = Databases(client)

# Initialize an empty list for documents data
documents_data = []

# List all documents in a collection
try:
    documents = databases.list_documents(
        database_id="NUMBERPLATE",  # Your database ID
        collection_id='DATA',  # Your collection ID
    )
    
    # Loop through the documents and get both IDs and data
    for doc in documents['documents']:
        # Exclude unwanted fields
        doc_data = {key: value for key, value in doc.items() if key not in ['$id', '$createdAt', '$updatedAt', '$permissions', '$databaseId', '$collectionId']}
        documents_data.append(doc_data)
    
    # Convert the document data into a pandas DataFrame
    df = pd.DataFrame(documents_data)

    # Ensure 'Date' is in proper datetime format
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

    # Adjust pandas display options for better view
    pd.set_option('display.max_columns', None)  # Show all columns
    pd.set_option('display.width', None)        # Adjust the width to fit all content
    pd.set_option('display.max_colwidth', None) # Allow full column content

    # Print the DataFrame
    print(df)

except Exception as e:
    print('Error:', e)

import pandas as pd
from appwrite.client import Client
from appwrite.services.databases import Databases
from dotenv import load_dotenv
import os



# Initialize Appwrite Client
client = Client()
client.set_endpoint('') # Your API Endpoint
client.set_project('') # Your project ID
client.set_key('')



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

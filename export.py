import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd
import json

# Initialize Firebase
cred = credentials.Certificate("./serviceAccountKey.json")
app = firebase_admin.initialize_app(cred)

# Read the JSON file containing collection names and field details
with open("./collections.json", "r") as json_file:
    data = json.load(json_file)

# Create an Excel writer object
excel_writer = pd.ExcelWriter("collections_data.xlsx", engine="xlsxwriter")

# Iterate over the collection data in the JSON file
for collection_name, field_names in data.items():
    # Get a reference to the Firestore collection
    collection_ref = firestore.client(app=app).collection(collection_name)

    # Query the Firestore collection and get the documents
    documents = collection_ref.stream()

    # Initialize a dictionary to store the data
    collection_data = {field_name: [] for field_name in field_names}

    # Iterate over the documents and extract the specified fields
    for document in documents:
        data_dict = document.to_dict()
        for field_name in field_names:
            collection_data[field_name].append(data_dict.get(field_name))

    # Create a DataFrame with the extracted data
    df = pd.DataFrame(collection_data)

    # Write the DataFrame to a new Excel sheet (tab)
    df.to_excel(excel_writer, sheet_name=collection_name, index=False)


# Save the Excel file
excel_writer.close()

# Clean up resources
firebase_admin.delete_app(app)

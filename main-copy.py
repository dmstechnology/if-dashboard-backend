from bson import json_util
from flask import Flask, render_template, request, redirect, url_for, jsonify
from pymongo import MongoClient
import os
import csv
from datetime import datetime

app = Flask(__name__)

# MongoDB connection
from pymongo import MongoClient
from urllib.parse import quote_plus

# MongoDB connection
username = "Milindvavare"
password = "Milindvavare"
encoded_username = quote_plus(username)
encoded_password = quote_plus(password)
#uri = f"mongodb+srv://{encoded_username}:{encoded_password}@cluster0.2u1hepu.mongodb.net/csv_database?retryWrites=true&w=majority&appName=Cluster0"
uri = f"mongodb+srv://{encoded_username}:{encoded_password}@if-dashboard-data.3zf02zx.mongodb.net/?retryWrites=true&w=majority&appName=if-dashboard-data"
client = MongoClient(uri)
db = client['csv_database']




# Route for home page
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'csv_file' not in request.files:
        return redirect(request.url)

    file = request.files['csv_file']
    if file.filename == '':
        return redirect(request.url)

    if file:
        filename = file.filename
        upload_date = datetime.now()

        # Save the uploaded file
        file_path = os.path.join('uploads', filename)
        file.save(file_path)

        # Read the CSV file and store its data
        csv_data = []
        with open(file_path, 'r') as csvfile:
            csv_reader = csv.DictReader(csvfile)
            for row in csv_reader:
                # Filter out specific fields or empty values before storing
                filtered_row = {key: value for key, value in row.items() if key not in ["Lead Owner", "Last Call Date", "Next Call Date", "Lead Stage", "Comments", "Call url"] and value.strip() != ""}
                csv_data.append(filtered_row)

        # Store the file data in MongoDB if there is data to store
        if csv_data:
            csv_files_collection = db['csv_files']
            csv_files_collection.insert_one({
                'filename': filename,
                'upload_date': upload_date,
                'user_token': '',
                'data': csv_data
            })

        return redirect(url_for('index'))
# Route for displaying uploaded files
@app.route('/files')
def list_files():
    csv_files_collection = db['csv_files']
    files = csv_files_collection.find({})
    return render_template('files.html', files=files)

@app.route('/api/fetch')
def fetch_data_api():
    csv_files_collection = db['csv_files']
    files = csv_files_collection.find({})

    # Convert MongoDB cursor to a list of dictionaries
    files_data = list(files)
    for file_data in files_data:
        file_data['_id'] = str(file_data['_id'])
        for data_row in file_data['data']:
            data_row['_id'] = str(data_row.get('_id'))

        # Return data as JSON
    return json_util.dumps(files_data)



if __name__ == '__main__':
    app.run(debug=True)

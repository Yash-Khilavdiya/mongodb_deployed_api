from flask import Flask, jsonify, request
from pymongo import MongoClient
import json
from pymongo.errors import WriteError, WriteConcernError
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
# client = MongoClient('localhost', 27017)  # Connect to MongoDB Local Database
# Connect to MongoDB Local Database on Microsoft Azure
client = MongoClient('mongodb://yash-khilavdiya:roO0h6bj8Ym9YA71AcRFl5FcA8PYY5yhJ7qOXJJxmIWOYQdWpkJ6zhqQdBqtU7D0kefRq4vvnmoXACDbm07ZQg==@yash-khilavdiya.mongo.cosmos.azure.com:10255/?ssl=true&retrywrites=false&replicaSet=globaldb&maxIdleTimeMS=120000&appName=@yash-khilavdiya@')
db = client.sample  # Select the MongoDB database

@app.route('/api/data', methods=['GET'])
def get_data():
    data = {'message': 'Hello from Flask API! for MongoDB'}
    return jsonify(data)

@app.route('/api/display', methods=['GET'])
def display():
    cursor = db.Record.find()
    record_list = []

    for record in cursor:
        record['_id'] = str(record['_id'])
        record_list.append(record)
    return jsonify(record_list)

@app.route('/api/insert', methods=['POST'])
def insert():
    raw_data = request.get_data()
    data_str = raw_data.decode('utf-8')
    json_data = json.loads(data_str)

    Name = json_data['Name']
    ContactNo = json_data['ContactNo']
    Address = json_data['Address']
    CollegeName = json_data['CollegeName']

    employees = {
            'Name': Name,
            'ContactNo': ContactNo,
            'Address': Address,
            'CollegeName': CollegeName
        }
        
    try:
        # Insert the document into the collection
        result = db.Record.insert_one(employees)

        # Access the inserted document's _id
        inserted_id = result.inserted_id
        return {"inserted_document_id" : str(inserted_id), "msg" : "document inserted successfully"}
    
    except (WriteError, WriteConcernError) as e:
        # Handle the exception
        return {"msg" : "failed in inserting document"}
    
# @app.route('/add', methods=['POST'])
# def add():
#     if request.method == 'POST':
#         Name = request.form['Name']
#         ContactNo = request.form['ContactNo']
#         Address = request.form['Address']
#         CollegeName = request.form['CollegeName']

#         employees = {
#             'Name': Name,
#             'ContactNo': ContactNo,
#             'Address': Address,
#             'CollegeName': CollegeName
#         }
        
#         db.Record.insert_one(employees)  
#         return redirect('/')

# @app.route('/edit/<string:id>', methods=['GET', 'POST'])
# def edit_employees(id):
#     id = ObjectId(id)
#     record = db.Record.find_one({'_id': id}) 
#     return render_template('edit.html', record=record)

# @app.route('/update_record', methods=['POST'])
# def edit():
#     if request.method == 'POST':
#         id = request.form['record_id']
#         Name = request.form['Name']
#         ContactNo = request.form['ContactNo']
#         Address = request.form['Address']
#         CollegeName = request.form['CollegeName']

#         # updated_Record = {
#         #     '_id' : ObjectId(id),
#         #     'Name': Name,
#         #     'ContactNo': ContactNo,
#         #     'Address': Address,
#         #     'CollegeName': CollegeName
#         # }

#         updated_Record = {
#             '$set': {
#                 '_id' : ObjectId(id),
#                 'Name': Name,
#                 'ContactNo': ContactNo,
#                 'Address': Address,
#                 'CollegeName': CollegeName
#             }
#         }
 
#         db.Record.update_one({'_id': ObjectId(id)}, updated_Record) 
#         return redirect('/')

# @app.route('/delete/<string:id>', methods=['POST'])
# def delete(id):
#     id = ObjectId(id)
#     db.Record.delete_one({'_id': id})  
#     return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)


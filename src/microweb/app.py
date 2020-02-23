
from datetime import datetime

from flask import Flask
from flask import request
from flask import jsonify

from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
app.config['mongo'] = MongoClient()


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/request', methods=['GET', 'POST'])
def request_post():
    found = app.config['mongo'].microweb.requests.find()
    if request.method == 'GET':
        results = [dict(
            id=str(document['_id']),
            email=document['email'],
            title=document['title'],
            timestamp=document['timestamp']
        ) for document in found]
        return jsonify(results), 200
    elif request.method == 'POST':
        data = request.json.copy()
        data['timestamp'] = datetime.now().isoformat()

        result = app.config['mongo'].microweb.requests.insert_one(data)

        document = app.config['mongo'].microweb.requests.find_one(
            {'_id': result.inserted_id})

        return jsonify(
            id=str(document['_id']),
            email=document['email'],
            title=document['title'],
            timestamp=document['timestamp']), 201


@app.route('/request/<request_id>', methods=['GET', 'DELETE'])
def request_get(request_id):
    if request.method == 'GET':
        document = app.config['mongo'].microweb.requests.find_one(
            {'_id': ObjectId(request_id)})

        if document:
            return jsonify(
                id=str(document['_id']),
                email=document['email'],
                title=document['title'],
                timestamp=document['timestamp']), 200
        else:
            return "Not found", 404
    elif request.method == 'DELETE':
        result = app.config['mongo'].microweb.requests.delete_one({
            '_id': ObjectId(request_id)})
        if result.deleted_count:
            return "", 204
        else:
            return "Not Found", 404

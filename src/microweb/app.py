
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


@app.route('/request', methods=['POST'])
def request_post():
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


@app.route('/request/<request_id>', methods=['GET'])
def request_get(request_id):
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


import os

from datetime import datetime

from flask import Flask
from flask import request
from flask import jsonify
from flask import redirect

from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
app.config['mongo'] = MongoClient(host=os.getenv('MONGODB_HOST'))


def serialize_request(document):
    return dict(
        id=str(document['_id']),
        email=document['email'],
        title=document['title'],
        timestamp=document['timestamp']
    )


def get_collection():
    db_name = os.getenv('MONGODB_DBNAME') or 'microweb'
    return app.config['mongo'][db_name].requests


@app.route('/', methods=['GET'])
def index():
    return redirect('request_root')


@app.route('/request', methods=['GET', 'POST'])
def request_root():
    found = get_collection().find()
    if request.method == 'GET':
        results = [serialize_request(document) for document in found]
        return jsonify(results), 200

    elif request.method == 'POST':
        data = request.json.copy()
        data['timestamp'] = datetime.now().isoformat()

        result = get_collection().insert_one(data)

        document = get_collection().find_one(
            {'_id': result.inserted_id})

        return jsonify(serialize_request(document)), 201


@app.route('/request/<request_id>', methods=['GET', 'DELETE'])
def request_get(request_id):
    if request.method == 'GET':
        document = get_collection().find_one(
            {'_id': ObjectId(request_id)})

        if document:
            return jsonify(serialize_request(document)), 200
        else:
            return "Not found", 404

    elif request.method == 'DELETE':
        result = get_collection().delete_one({
            '_id': ObjectId(request_id)})

        if result.deleted_count:
            return "", 204
        else:
            return "Not Found", 404

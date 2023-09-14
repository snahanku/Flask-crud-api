from flask import Flask

from flask_pymongo import PyMongo
from bson.json_util import dumps 
from bson.raw_bson import RawBSONDocument
from bson.objectid import ObjectId
from bson import _get_object_size, _raw_to_dict
from flask import jsonify, request

import json

app = Flask(__name__)

app.secret_key = "secretkey"

app.config['MONGO_URI'] = "mongodb://localhost:27017/userdb"

mongo = PyMongo(app)


@app.route('/add', methods=['POST'])
def add_user():
    _json = request.json
    _name = _json['name']
    _email = _json['email']
    _phone = _json['phone']

    if _name and _email and _phone and request.method == 'POST':

        id = mongo.db.users.insert_one(
            {'name': _name, 'email': _email, 'phone': _phone})

        resp = jsonify("User Added Successfully")

        resp.status_code = 200

        return resp
    else:
        return not_found()


@app.route('/users', methods=['GET'])
def users():
    users = mongo.db.users.find()
    resp = dumps(users)
    return resp



@app.route('/users/<id>')
def user(id):
    user = mongo.db.users.find_one({'_id': ObjectId(id)})
    resp = dumps(user)
    return resp





@app.route('/delete/<id>', methods=['DELETE'])
def delete(id):
    mongo.db.users.delete_one({'_id': ObjectId(id)})
    resp = jsonify("user deleted successfully")
    return resp


@app.route('/update/<id>', methods=['PUT'])
def update_user(id):
    _id = id
    _json = request.json
    _name = _json['name']
    _email = _json['email']
    _phone = _json['phone']

    if _name and _email and _id and request.method == 'PUT':
        mongo.db.users.update_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(
            _id)}, {'$set': {'name': _name, 'email': _email, 'phone':_phone}})
        resp = jsonify("user updated successfully")
        resp.status_code = 200

        return resp

    else:
        return not_found()


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found' + request.url
    }
    resp = jsonify(message)

    resp.status_code = 404

    return resp


### for specific user ######


if __name__ == "__main__":
    app.run(debug=True)

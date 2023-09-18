from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId

app = Flask(__name__)
app.secret_key = "secretkey"
app.config['MONGO_URI'] = "mongodb://localhost:27017/userdb"
mongo = PyMongo(app)

class UserAPI:
    @classmethod
    def add_user(cls):
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
            return cls.not_found()

    @classmethod
    def get_users(cls):
        users = mongo.db.users.find()
        resp = dumps(users)
        return resp

    @classmethod
    def get_user(cls, id):
        user = mongo.db.users.find_one({'_id': ObjectId(id)})
        resp = dumps(user)
        return resp

    @classmethod
    def delete_user(cls, id):
        mongo.db.users.delete_one({'_id': ObjectId(id)})
        resp = jsonify("User deleted successfully")
        return resp

    @classmethod
    def update_user(cls, id):
        _json = request.json
        _name = _json['name']
        _email = _json['email']
        _phone = _json['phone']

        if _name and _email and id and request.method == 'PUT':
            mongo.db.users.update_one({'_id': ObjectId(id)}, {'$set': {'name': _name, 'email': _email, 'phone': _phone}})
            resp = jsonify("User updated successfully")
            resp.status_code = 200
            return resp
        else:
            return cls.not_found()

    @staticmethod
    def not_found():
        message = {
            'status': 404,
            'message': 'Not Found ' + request.url
        }
        resp = jsonify(message)
        resp.status_code = 404
        return resp

# Routes included 
@app.route('/add', methods=['POST'])
def add_user():
    return UserAPI.add_user()

@app.route('/users', methods=['GET'])
def get_users():
    return UserAPI.get_users()

@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    return UserAPI.get_user(id)

@app.route('/delete/<id>', methods=['DELETE'])
def delete_user(id):
    return UserAPI.delete_user(id)

@app.route('/update/<id>', methods=['PUT'])
def update_user(id):
    return UserAPI.update_user(id)

if __name__ == "__main__":
    app.run(debug=True)

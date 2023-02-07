from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime
import os

# Init App
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# DB Config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init DB
db = SQLAlchemy(app)

# Init Ma
ma = Marshmallow(app)

# User Class/Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), unique=True, nullable=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    avatar = db.Column(db.String(50))
    # created_at = db.Column(db.DateTime)
    # updated_at = db.Column(db.DateTime)
    # deleted_at = db.Column(db.DateTime)

    def __init__(self, email, first_name, last_name, avatar):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.avatar = avatar
        # self.created_at = created_at
        # self.updated_at = updated_at
        # self.deleted_at = deleted_at

# User Schema
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'email', 'first_name', 'last_name', 'avatar')

# Init Schema
user_schema = UserSchema
users_schema = UserSchema(many=True)

# Home
@app.route('/', methods=['GET'])
def home():
    return jsonify({
            'msg': 'Introduction My First API With Python Flask'
        })

# Get All User
@app.route('/user', methods=['GET'])
def get_users():
    all_users = User.query.all()
    result = users_schema.dump(all_users)
    return jsonify({
            'msg': 'OK',
            'data': result
        })

# Get Specific User
@app.route('/user/<id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    return user_schema.jsonify({
            'msg': 'OK',
            'data': user
        })

# Add User
@app.route('/user', methods=['POST'])
def add_user():
    email = request.json['email']
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    avatar = request.json['avatar']
    # created_at = datetime.today()
    # created_at = created_at.strftime('%Y-%m-%d')
    # updated_at = datetime.today()
    # updated_at = updated_at.strftime('%Y-%m-%d')
    # deleted_at = ""

    new_user = User(email, first_name, last_name, avatar)

    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify({
            'msg': 'user created successfully',
            'data': new_user
        })

# Update User
@app.route('/user/<id>', methods=['PUT'])
def update_user(id):
    user = User.query.get(id)

    email = request.json['email']
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    avatar = request.json['avatar']
    # created_at = datetime.today()
    # created_at = created_at.strftime('%Y-%m-%d')
    # updated_at = datetime.today()
    # updated_at = updated_at.strftime('%Y-%m-%d')
    # deleted_at = ""

    user.email = email
    user.first_name = first_name
    user.last_name = last_name
    user.avatar = avatar

    db.session.commit()

    return user_schema.jsonify({
            'msg': 'user updated successfully',
            'data': user
        })

# Delete User
@app.route('/user/<id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)

    db.session.delete(user)
    db.session.commit()

    return user_schema.jsonify({
            'msg': 'Data Deleted Successfully'
        })

#run server
if __name__ == '__main__':
    app.run(debug=True)
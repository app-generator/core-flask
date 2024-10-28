# app.py
from flask import Flask, request
from flask_restx import Api, Resource, fields
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
api = Api(app, title="Secure API", description="A Simple, Secure Flask API with SQLite and Flask-RESTx")

# Import the models after initializing db to avoid circular imports
from models import User

# Define a namespace for user routes
user_ns = api.namespace('users', description='User operations')

# Define the user model for input validation
user_model = api.model('User', {
    'username': fields.String(required=True, description='Username'),
    'password': fields.String(required=True, description='Password')
})

@user_ns.route('/register')
class UserRegister(Resource):
    @api.expect(user_model, validate=True)
    def post(self):
        data = request.json
        hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        new_user = User(username=data['username'], password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return {'message': 'User registered successfully'}, 201

@user_ns.route('/login')
class UserLogin(Resource):
    @api.expect(user_model, validate=True)
    def post(self):
        data = request.json
        user = User.query.filter_by(username=data['username']).first()
        if user and bcrypt.check_password_hash(user.password_hash, data['password']):
            access_token = create_access_token(identity=user.username)
            return {'access_token': access_token}, 200
        return {'message': 'Invalid credentials'}, 401

@user_ns.route('/profile')
class UserProfile(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        return {'username': current_user}, 200

# Create the database tables if they do not exist
@app.before_first_request
def create_tables():
    db.create_all()

# Run the app
if __name__ == '__main__':
    app.run(debug=True)

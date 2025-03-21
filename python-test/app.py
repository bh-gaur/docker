from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask app and configure SQLite database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

# Create the database if it doesn't exist yet
@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def home():
    return "Welcome to the Flask API!"

@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.ico')

# Endpoint to create a new user
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = User(name=data['name'], email=data['email'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created!'}), 201

# Endpoint to retrieve all users
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{'id': user.id, 'name': user.name, 'email': user.email} for user in users])

# Endpoint to retrieve a specific user by ID
@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify({'id': user.id, 'name': user.name, 'email': user.email})

# Endpoint to update a user by ID
@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get_or_404(id)
    data = request.get_json()
    user.name = data.get('name', user.name)
    user.email = data.get('email', user.email)
    db.session.commit()
    return jsonify({'message': 'User updated!'})

# Endpoint to delete a user by ID
@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted!'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

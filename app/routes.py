from flask import Blueprint, request, jsonify
from .services import get_dynamo_client
from services import create_user_table, create_post_table
from .utils import generate_jwt_token, decode_jwt_token
from .models import User, BlogPost
import uuid

main = Blueprint('main', __name__)

# Initialize DynamoDB tables
create_user_table()
create_post_table()

@main.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')  # In real applications, hash this password
    user = User(username, password)

    dynamodb = get_dynamo_client()
    table = dynamodb.Table('Users')
    table.put_item(Item={'username': user.username, 'password': user.password})
    
    return jsonify({"message": "User registered successfully."}), 201

@main.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    dynamodb = get_dynamo_client()
    table = dynamodb.Table('Users')
    response = table.get_item(Key={'username': username})
    
    user = response.get('Item')
    if user and user['password'] == password:
        token = generate_jwt_token(username)
        return jsonify({"token": token}), 200

    return jsonify({"message": "Invalid credentials."}), 401

@main.route('/posts', methods=['POST'])
def create_post():
    data = request.get_json()
    token = request.headers.get('Authorization').split(" ")[1]
    username = decode_jwt_token(token)
    
    if username:
        post_id = str(uuid.uuid4())
        blog_post = BlogPost(data['title'], data['content'], username)

        dynamodb = get_dynamo_client()
        table = dynamodb.Table('BlogPosts')
        table.put_item(Item={'post_id': post_id, 'title': blog_post.title, 'content': blog_post.content, 'author': blog_post.author})
        
        return jsonify({"message": "Post created successfully."}), 201
    
    return jsonify({"message": "Token is invalid."}), 401

@main.route('/posts', methods=['GET'])
def get_posts():
    dynamodb = get_dynamo_client()
    table = dynamodb.Table('BlogPosts')
    response = table.scan()
    
    return jsonify(response['Items']), 200

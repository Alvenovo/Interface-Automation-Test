# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify

app = Flask(__name__)

users_db = [
    {"id": 1, "username": "admin", "password": "123456", "email": "admin@test.com", "name": "张三"},
    {"id": 2, "username": "testuser", "password": "123456", "email": "test@test.com", "name": "李四"},
    {"id": 3, "username": "wangwu", "password": "123456", "email": "wangwu@test.com", "name": "王五"},
    {"id": 4, "username": "zhaoliu", "password": "123456", "email": "zhaoliu@test.com", "name": "赵六"},
]

@app.route("/", methods=["GET"])
@app.route("/health", methods=["GET"])
@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "message": "服务正常运行中"}), 200

@app.route("/api/users", methods=["GET"])
def get_users():
    result = []
    for u in users_db:
        result.append({"id": u["id"], "username": u["username"], "email": u["email"], "name": u["name"]})
    return jsonify(result), 200

@app.route("/api/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    for u in users_db:
        if u["id"] == user_id:
            return jsonify({"id": u["id"], "username": u["username"], "email": u["email"], "name": u["name"]}), 200
    return jsonify({"error": "User not found"}), 404

@app.route("/api/users", methods=["POST"])
def register_user():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400
    username = data.get("username", "").strip()
    password = data.get("password", "").strip()
    email = data.get("email", "").strip()
    if not username:
        return jsonify({"error": "Username is required"}), 400
    if not password:
        return jsonify({"error": "Password is required"}), 400
    if not email:
        email = username + "@test.com"
    if "@" not in email or "." not in email:
        return jsonify({"error": "Invalid email format"}), 400
    for user in users_db:
        if user["username"] == username:
            return jsonify({"error": "Username already exists"}), 409
    new_id = max(u["id"] for u in users_db) + 1 if users_db else 1
    new_user = {"id": new_id, "username": username, "password": password, "email": email, "name": username}
    users_db.append(new_user)
    return jsonify({"message": "User registered successfully", "user": {"id": new_id, "username": username, "email": email}}), 201

@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400
    username = data.get("username", "").strip()
    password = data.get("password", "").strip()
    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400
    for u in users_db:
        if u["username"] == username and u["password"] == password:
            return jsonify({"message": "登录成功", "user": {"id": u["id"], "username": u["username"], "email": u["email"]}}), 200
    return jsonify({"error": "Invalid username or password"}), 401

@app.route("/api/echo", methods=["POST"])
def echo():
    data = request.get_json()
    return jsonify({"data": data}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)

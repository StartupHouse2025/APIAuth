from flask import Blueprint, request, jsonify
from bcrypt import hashpw, gensalt
from src.mongodb.connect import ConnectionMongo

# Crear un Blueprint en lugar de usar @app.route
register_bp = Blueprint('register', __name__)

# Conectar a MongoDB
mongo_connection = ConnectionMongo()

@register_bp.route('/signup', methods=['POST'])
def signup():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not name or not email or not password:
        return jsonify({"error": "Todos los campos son obligatorios"}), 400

    # Verificar si el usuario ya existe
    existing_user = mongo_connection.con.users.find_one({"email": email})
    if existing_user:
        return jsonify({"error": "El usuario ya está registrado"}), 400

    # Encriptar la contraseña antes de guardarla
    hashed_password = hashpw(password.encode('utf-8'), gensalt()).decode('utf-8')

    # Guardar usuario en la base de datos
    mongo_connection.con.users.insert_one({
        "name": name,
        "email": email,
        "password": hashed_password
    })

    return jsonify({"message": "Usuario registrado correctamente"}), 201


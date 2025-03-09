from flask import Blueprint, request, jsonify
from bcrypt import checkpw
from flask import current_app  # Para acceder a la conexión de MongoDB desde `app.py`

credential_bp = Blueprint('credential', __name__)

@credential_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    name = data.get("name")
    password = data.get("password")

    if not name or not password:
        return jsonify({"error": "Faltan campos requeridos"}), 400

    # Buscar usuario en MongoDB
    user = current_app.mongo_connection.con.users.find_one({"name": name})

    if user:
        # Verificar la contraseña encriptada
        if checkpw(password.encode('utf-8'), user["password"].encode('utf-8') if isinstance(user["password"], str) else user["password"]):
            return jsonify({"message": "Inicio de sesión exitoso"}), 200
        else:
            return jsonify({"error": "Contraseña incorrecta"}), 401
    else:
        return jsonify({"error": "Usuario no encontrado"}), 404



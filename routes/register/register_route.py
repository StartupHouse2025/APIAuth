from flask import Blueprint, request, abort

from src.crear_credential.infrastructure.controller import CrearCredentialController
from src.mongodb.connect import ConnectionMongo

# Crear un Blueprint en lugar de usar @app.route
register_bp = Blueprint('register', __name__)
credential_crear_controller = CrearCredentialController()

# Función de consulta
def consulta(info):
    credential_info = credential_crear_controller.crear_credential(info)  # Pasar credencial y contraseña
    return credential_info

# Conectar a MongoDB
mongo_connection = ConnectionMongo()

@register_bp.route('/signup', methods=['POST'])
def signup():
    """
    Crear una nueva credencial.
    ---
    tags:
      - Crear Credencial
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - in: body
        name: body
        description: Datos necesarios para crear la credencial
        required: true
        schema:
          type: object
          properties:
            data:
              type: object
              properties:
                user_name:
                  type: string
                  example: "Example User"
                email:
                  type: string
                  example: "example@example.com"
                cel_number:
                  type: int
                  example: "1234567890"
                password:
                  type: string
                  example: "password123"
    responses:
      200:
        description: Credencial creada correctamente
      404:
        description: Error al crear
    """
    data = request.get_json().get('data')
    if not data:
        return abort(400, description="Datos no proporcionados")
    try:
        return consulta(data)
    except FileNotFoundError:
        return abort(404, description="Error al crear")

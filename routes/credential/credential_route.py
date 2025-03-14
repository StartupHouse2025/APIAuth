from flask import Blueprint, request, jsonify
from bcrypt import checkpw
from src.credential.infrastructure.controller import CredentialController
from include.validators import checkArgs, parsedRespond


# Crear un blueprint para el manejo de rutas de usuario
credential_bp = Blueprint('credential', __name__)

# Instanciar el controlador de usuario
credential_controller = CredentialController()

# Función de consulta
def consulta(credential, pasw):
    if "@" not in credential:
        credential = int(credential)
    credential_info = credential_controller.authenticate_credential(credential, pasw)  # Pasar credencial y contraseña
    return parsedRespond(credential_info)



@credential_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Autenticación de usuario por credenciales.
    ---
    tags:
      - Consulta Credenciales
    parameters:
      - name: credential
        in: query
        type: string
        required: true
        description: Credencial del usuario (correo o número de teléfono).
      - name: pass
        in: query
        type: string
        required: true
        description: Contraseña del usuario.
    responses:
      200:
        description: Autenticación exitosa.
        schema:
          type: object
          properties:
            status:
              type: boolean
              example: true
            message:
              type: string
              example: "ok"
            data:
              type: object
              properties:
                id:
                  type: string
                  description: ID del usuario autenticado.
                  example: "12345"
                email:
                  type: string
                  description: Correo electrónico del usuario.
                  example: "user@example.com"
                cel_number:
                  type: int
                  description: Número de celular del usuario.
                  example: 1234567890
                user_name:
                  type: string
                  description: Nombre del usuario.
                  example: Example User
                role:
                  type: string
                  description: Rol del usuario.
                  example: "user"
      400:
        description: Error de autenticación.
        schema:
          type: object
          properties:
            error:
              type: string
              description: Mensaje de error.
              example: "Usuario o contraseña incorrectos"
    """
    if request.method == 'GET':
        # Si los parámetros vienen en la URL
        checkArgs(['credential', 'pass'], request.args)
        credential = request.args['credential']
        pasw = request.args['pass']
    elif request.method == 'POST':
        # Si los parámetros vienen en un formulario POST
        credential = request.form.get('credential')
        pasw = request.form.get('password')

    try:
        # Llamar al método de autenticación del controlador
        return jsonify(consulta(credential, pasw)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400



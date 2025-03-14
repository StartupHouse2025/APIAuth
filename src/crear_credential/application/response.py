from flask import abort, jsonify
from bcrypt import hashpw, gensalt

def reestructurar_cadena(diccionario):
    # Encriptar la contraseña antes de guardarla
    hashed_password = hashpw(diccionario.get('password').encode('utf-8'), gensalt())
    transformed_data = {
        'user_name': diccionario.get('user_name', ''),  # Si no hay 'user_name', se usa ''
        'email': diccionario.get('email', ''),  # Si no hay 'email', se usa ''
        'cel_number': diccionario.get('cel_number', ''),  # Renombrar 'cel_number' a 'cel_mobile'
        'password': hashed_password,  # Renombrar 'id' a 'pass'
        'role': 'user'
    }
    return transformed_data

class CrearCredentialResponse():
    @staticmethod
    def SetCrearCredential(col, data): 
        if not data.get("user_name") or not data.get("email") or not data.get("password") or not data.get("cel_number"):
            return abort(400, description="Todos los campos son obligatorios")
        
        # Verificar si el usuario ya existe
        if col.find_one({"email": data.get("email")}) or col.find_one({"cel_number": data.get("cel_number")}):

            return abort(400, description="El usuario ya existe")
        else:
            print(data) 
            if data:
                newData = reestructurar_cadena(data)
                result = col.insert_one(newData)
                print(result)
                return jsonify({"message": "Usuario registrado correctamente"}), 200
import jwt as pyjwt
import datetime
import os


def generate_token(credential_info):
    payload = {
        "user_id": str(credential_info.get("_id")),  # ID del usuario
        "email": credential_info.get("email"),
        "cel_number": credential_info.get("cel_number"),
        "user_name": credential_info.get("user_name"),
        "role": credential_info.get("role"),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=int(os.getenv("ACCESS_TOKEN_EXPIRE_HOURS")))  # Expira en 2 horas
    }
    token = pyjwt.encode(payload, os.getenv("SECRET_KEY"), algorithm=os.getenv("ALGORITHM"))
    return token


class CredentialResponse():
    @staticmethod
    def parsedCredential(credential_info):
        if credential_info:
            return generate_token(credential_info)
        else:
            raise Exception("Usuario o contraseña incorrectos")
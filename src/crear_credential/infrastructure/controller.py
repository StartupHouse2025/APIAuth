from src.crear_credential.infrastructure.mongod import MongodCrearCredential
from ..application.response import CrearCredentialResponse

class CrearCredentialController:

    def __init__(self):
        self.mongo_number_validar = MongodCrearCredential()
        self.response = CrearCredentialResponse()

    def crear_credential(self, data):
        col = self.mongo_number_validar.CrearCredentialConnect()
        status = self.response.SetCrearCredential(col, data)
        return status



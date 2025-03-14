from src.credential.infrastructure.mongod import MongodCredential
from ..application.response import CredentialResponse

class CredentialController:

    def __init__(self):
        self.mongo_credential = MongodCredential()
        self.response = CredentialResponse()

    def authenticate_credential(self, credential, pasw):
        credential_info = self.mongo_credential.CredentialConnect(credential, pasw)
        parsed = self.response.parsedCredential(credential_info)
        return parsed



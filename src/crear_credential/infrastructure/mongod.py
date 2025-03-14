from ...mongodb.connect import ConnectionMongo

class MongodCrearCredential:
    def __init__(self) -> None:
        self.connect = ConnectionMongo()

    def CrearCredentialConnect(self):
        db = self.connect.con  # Asegúrate de que esté accediendo a la conexión correcta
        col = db["credential"]
        return col

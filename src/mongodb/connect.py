from pymongo import MongoClient
import os

class ConnectionMongo:
    def __init__(self):
        # Nombre de la base de datos
        db = "startup"
        
        self.connection = MongoClient(os.getenv("DATABASE_URL")) #Clave insegura
        self.con = self.connection[db]

        try:
            databases = self.connection.list_database_names()
            print(f"✅ Conectado a MongoDB. Bases de datos disponibles: {databases}")
        except Exception as e:
            print(f"❌ Error al conectar a MongoDB: {e}")

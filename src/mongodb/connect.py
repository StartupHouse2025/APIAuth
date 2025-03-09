from pymongo import MongoClient

class ConnectionMongo:
    def __init__(self):
        db = "startup"
        self.connection = MongoClient("mongodb+srv://admin2025:toolOne2025@databaseone.cqltp.mongodb.net/")
        self.con = self.connection[db]

        try:
            databases = self.connection.list_database_names()
            print(f"✅ Conectado a MongoDB. Bases de datos disponibles: {databases}")
        except Exception as e:
            print(f"❌ Error al conectar a MongoDB: {e}")

    def check_connection(self):
        try:
            return {"message": "Conexión a MongoDB exitosa", "databases": self.connection.list_database_names()}
        except Exception as e:
            return {"message": f"Error al conectar a MongoDB: {e}"}

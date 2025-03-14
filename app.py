from dotenv import load_dotenv
load_dotenv()

from flask import Flask
from flask_cors import CORS
from routes.credential.credential_route import credential_bp
from routes.register.register_route import register_bp

from swagger_config import configure_swagger

app = Flask(__name__)
CORS(app)

app.register_blueprint(credential_bp, url_prefix='/get_credential')
app.register_blueprint(register_bp, url_prefix='/set_register')

# Configurar Swagger
configure_swagger(app)

@app.route('/')
def index():
    return "Hello, World!"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
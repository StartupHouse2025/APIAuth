from flask import Flask, jsonify, render_template_string, request, redirect, url_for # type: ignore
from bcrypt import hashpw, gensalt, checkpw
from route.credential.credential_route import credential_bp
from route.register.register_route import register_bp
from src.mongodb.connect import ConnectionMongo

app = Flask(__name__)

# Inicializar la conexión a MongoDB
mongo_connection = ConnectionMongo()
app.mongo_connection = mongo_connection

app.register_blueprint(credential_bp, url_prefix='/credential')
app.register_blueprint(register_bp, url_prefix='/register')

@app.route('/')
def home():
    return render_template_string('''
        <!doctype html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Holi, Flask!</title>
            <style>
                button {
                    display: block;
                    margin: 10px 0;
                    padding: 10px 20px;
                    font-size: 16px;
                }
            </style>
        </head>
        <body>
            <h1>Holi, Flask!</h1>
            <button onclick="window.location.href='/login'">Login</button>
            <button onclick="window.location.href='/register'">Register</button>
        </body>
        </html>
    ''')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        
        # Encriptar la contraseña antes de guardarla
        hashed_password = hashpw(password.encode('utf-8'), gensalt()).decode('utf-8')
        
        # Guardar en la base de datos
        app.mongo_connection.con.users.insert_one({
            "name": name,
            "email": email,
            "password": hashed_password
        })
        
        return redirect(url_for('home'))
    
    return render_template_string('''
        <!doctype html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Registro</title>
        </head>
        <body>
            <h1>Registro</h1>
            <form method="POST">
                <label for="name">Nombre:</label>
                <input type="text" id="name" name="name" required><br>
                <label for="email">Email:</label>
                <input type="email" id="email" name="email" required><br>
                <label for="password">Contraseña:</label>
                <input type="password" id="password" name="password" required><br>
                <button type="submit">Registrar</button>
            </form>
        </body>
        </html>
    ''')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        
        user = app.mongo_connection.con.users.find_one({"name": name})
        if user and checkpw(password.encode('utf-8'), user["password"].encode('utf-8') if isinstance(user["password"], str) else user["password"]):
            return redirect(url_for('login_success'))
        else:
            return render_template_string('''
                <!doctype html>
                <html lang="es">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Login</title>
                </head>
                <body>
                    <h1>Error: Credenciales inválidas</h1>
                    <a href="/login">Intentar de nuevo</a>
                </body>
                </html>
            ''')
    
    return render_template_string('''
        <!doctype html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Login</title>
        </head>
        <body>
            <h1>Login</h1>
            <form method="POST">
                <label for="name">Nombre:</label>
                <input type="text" id="name" name="name" required><br>
                <label for="password">Contraseña:</label>
                <input type="password" id="password" name="password" required><br>
                <button type="submit">Iniciar sesión</button>
            </form>
        </body>
        </html>
    ''')

@app.route('/login_success')
def login_success():
    return render_template_string('''
        <!doctype html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Login Exitoso</title>
        </head>
        <body>
            <h1>Inicio de sesión exitoso</h1>
            <a href="/">Volver a la página principal</a>
        </body>
        </html>
    ''')

@app.route('/test_db')
def test_db():
    result = mongo_connection.check_connection()
    return jsonify(result), 200 if "databases" in result else 500

if __name__ == '__main__':
    app.run(debug=True)
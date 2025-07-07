import os
import sqlite3
from flask import Flask, request, render_template_string

app = Flask(__name__)

# Vulnerabilidade 1: Segredo Hardcoded
# Chaves e segredos nunca devem ser colocados diretamente no código.
API_KEY = "sk_live_abcdef1234567890_muitosecreto"

# Vulnerabilidade 4: Adicionando um novo segredo para o teste
SECRET_ACCESS_KEY = "aws_secret_key_exemplo_12345"

# Configuração do banco de dados (simples, em memória para a PoC)
def init_db():
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    cursor.execute("INSERT INTO users (username, password) VALUES ('admin', 'password123')")
    cursor.execute("INSERT INTO users (username, password) VALUES ('user', 'userpass')")
    conn.commit()
    return conn

db_connection = init_db()

@app.route('/')
def home():
    # Adicionando um comentário para testar o fluxo de PR.
    return """
    <h1>Aplicação de Teste SAST</h1>
    <p>Esta aplicação contém vulnerabilidades para a PoC do Semgrep.</p>
    <ul>
        <li><a href="/search?username=admin">Pesquisar Usuário (Injeção de SQL)</a></li>
        <li><a href="/file?name=README.md">Verificar Arquivo (Injeção de Comando)</a></li>
    </ul>
    """

@app.route('/search')
def search_user():
    username = request.args.get('username')
    
    # Vulnerabilidade 2: Injeção de SQL
    # A query é construída concatenando a entrada do usuário diretamente,
    # permitindo que um atacante manipule a query.
    # Exemplo de ataque: /search?username=admin'--
    query = "SELECT username FROM users WHERE username = '" + username + "'"
    
    cursor = db_connection.cursor()
    try:
        cursor.execute(query)
        user = cursor.fetchone()
        if user:
            return f"<h1>Usuário encontrado: {user[0]}</h1>"
        else:
            return "<h1>Usuário não encontrado.</h1>"
    except sqlite3.Error as e:
        return f"<h1>Erro no banco de dados:</h1><p>{e}</p>"


@app.route('/file')
def check_file():
    filename = request.args.get('name')

    # Vulnerabilidade 3: Injeção de Comando
    # O sistema operacional executa um comando que inclui a entrada do usuário
    # sem sanitização, permitindo a execução de comandos arbitrários.
    # Exemplo de ataque: /file?name=test;ls
    cmd = 'echo "Verificando o arquivo: ' + filename + '"'
    output = os.popen(cmd).read()

    return f"<h2>Resultado do Comando:</h2><pre>{output}</pre>"

if __name__ == '__main__':
    # AVISO: Não use o servidor de desenvolvimento do Flask em produção.
    # O modo debug também é inseguro.
    app.run(debug=True, host='0.0.0.0', port=5001) 
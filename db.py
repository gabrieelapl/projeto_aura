import mysql.connector

# Conexão com o banco de dados
db = mysql.connector.connect(
    host="localhost",
    user="root",           # usuário do MySQL
    password="",  # senha do usuário
    database="aura_db"     # nome do banco de dados
)

# Cursor com dicionário para facilitar o acesso às colunas pelo nome
cursor = db.cursor(dictionary=True)

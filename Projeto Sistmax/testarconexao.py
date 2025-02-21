# db.py - Módulo de conexão e operações com o banco de dados
import mysql.connector
import bcrypt
from mysql.connector import Error

# Configuração do banco de dados
DB_CONFIG = {
    "host": "localhost",
    "port": "3306",
    "user": "root",
    "password": "",
    "database": "SISTMAX"
}

def conectar():
    """Conecta ao banco de dados e retorna a conexão."""
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except Error as e:
        print(f"\033[91m❌ Erro ao conectar ao banco: {e}\033[0m")
        return None

def criar_usuario(nome, email, senha, tipo_usuario):
    """Cria um novo usuário com senha criptografada."""
    senha_hash = bcrypt.hashpw(senha.encode(), bcrypt.gensalt()).decode()
    try:
        conexao = conectar()
        if conexao:
            cursor = conexao.cursor()
            query = """
                INSERT INTO usuarios (nome, email, senha, tipo_usuario)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (nome, email, senha_hash, tipo_usuario))
            conexao.commit()
            print("✅ Usuário criado com sucesso!")
            cursor.close()
            conexao.close()
    except Error as e:
        print(f"\033[91m❌ Erro ao criar usuário: {e}\033[0m")

def verificar_login(email, senha):
    """Verifica credenciais de login."""
    try:
        conexao = conectar()
        if conexao:
            cursor = conexao.cursor()
            cursor.execute("SELECT id, nome, senha FROM usuarios WHERE email = %s", (email,))
            usuario = cursor.fetchone()
            cursor.close()
            conexao.close()
            
            if usuario and bcrypt.checkpw(senha.encode(), usuario[2].encode()):
                return usuario[0], usuario[1]
            else:
                return None, None
    except Error as e:
        print(f"\033[91m❌ Erro ao verificar login: {e}\033[0m")
    return None, None

def listar_usuarios():
    """Lista todos os usuários cadastrados."""
    try:
        conexao = conectar()
        if conexao:
            cursor = conexao.cursor()
            cursor.execute("SELECT id, nome, email, tipo_usuario FROM usuarios")
            usuarios = cursor.fetchall()
            cursor.close()
            conexao.close()
            return usuarios
    except Error as e:
        print(f"\033[91m❌ Erro ao listar usuários: {e}\033[0m")
    return []

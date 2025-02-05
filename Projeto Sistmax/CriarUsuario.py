import mysql.connector
from mysql.connector import Error

# Função de conexão
def conectar():
    try:
        conexao = mysql.connector.connect(
            host="localhost", 
            port="3306", 
            user="root", 
            password="12345678", 
            database="Sistmax"
        )
        return conexao
    except Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

# Função para criar o usuário
def criar_usuario():
    # Solicitar dados ao usuário
    nome = input("Digite o nome do usuário: ")
    email = input("Digite o e-mail do usuário: ")
    senha = input("Digite a senha do usuário: ")
    
    # Solicitar plano de usuário com validação
    planos_validos = ['básico + anúncios', 'pro', 'premium']
    while True:
        tipo_usuario = input(f"Escolha o plano de usuário ({', '.join(planos_validos)}): ").strip()
        if tipo_usuario.lower() in [plano.lower() for plano in planos_validos]:  # Ignore case na validação
            tipo_usuario = tipo_usuario.lower()  # Garantir que o valor inserido será armazenado corretamente
            break
        else:
            print("Plano inválido. Tente novamente.")
    
    # Inserir no banco de dados
    try:
        conexao = conectar()
        if conexao:
            cursor = conexao.cursor()
            query = "INSERT INTO usuarios (nome, email, senha, tipo_usuario) VALUES (%s, %s, %s, %s)"
            valores = (nome, email, senha, tipo_usuario)
            cursor.execute(query, valores)
            conexao.commit()
            cursor.close()
            conexao.close()
            print(f"Usuário '{nome}' criado com sucesso com o plano '{tipo_usuario}'.")
        else:
            print("Não foi possível conectar ao banco de dados.")
    except mysql.connector.Error as erro:
        print(f"Erro ao inserir o usuário no banco de dados: {erro}")

# Chamar a função para criar o usuário
criar_usuario()

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

# Função para listar os usuários
def listar_usuarios():
    try:
        conexao = conectar()
        if conexao:
            cursor = conexao.cursor()
            cursor.execute("SELECT id, nome, email, tipo_usuario FROM usuarios")
            usuarios = cursor.fetchall()  # Recupera todos os resultados da consulta

            if usuarios:
                print(f"{'ID':<5} {'Nome':<30} {'Email':<40} {'Tipo de Usuário':<20}")
                print("-" * 100)
                for usuario in usuarios:
                    print(f"{usuario[0]:<5} {usuario[1]:<30} {usuario[2]:<40} {usuario[3]:<20}")
            else:
                print("Nenhum usuário encontrado.")
            
            cursor.close()
            conexao.close()
        else:
            print("Não foi possível conectar ao banco de dados.")
    except mysql.connector.Error as erro:
        print(f"Erro ao consultar usuários: {erro}")

# Função para atualizar usuário
def atualizar_usuario():
    try:
        conexao = conectar()
        if conexao:
            id_usuario = int(input("Digite o ID do usuário que deseja atualizar: "))
            novo_nome = input("Digite o novo nome do usuário: ")
            novo_email = input("Digite o novo e-mail do usuário: ")
            novo_tipo = input("Escolha o novo plano de usuário (básico + anúncios, pro, premium): ").strip().lower()
            
            # Validar o tipo de usuário
            planos_validos = ['básico + anúncios', 'pro', 'premium']
            if novo_tipo not in planos_validos:
                print("Plano inválido. Tente novamente.")
                return

            cursor = conexao.cursor()
            query = "UPDATE usuarios SET nome = %s, email = %s, tipo_usuario = %s WHERE id = %s"
            valores = (novo_nome, novo_email, novo_tipo, id_usuario)
            cursor.execute(query, valores)
            conexao.commit()
            
            if cursor.rowcount > 0:
                print(f"Usuário com ID {id_usuario} atualizado com sucesso.")
            else:
                print(f"Não foi possível atualizar o usuário com ID {id_usuario}.")
            
            cursor.close()
            conexao.close()
        else:
            print("Não foi possível conectar ao banco de dados.")
    except mysql.connector.Error as erro:
        print(f"Erro ao atualizar usuário: {erro}")

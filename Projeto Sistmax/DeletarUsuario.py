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

# Função para deletar usuário
def deletar_usuario():
    try:
        conexao = conectar()
        if conexao:
            id_usuario = int(input("Digite o ID do usuário que deseja deletar: "))
            
            cursor = conexao.cursor()
            query = "DELETE FROM usuarios WHERE id = %s"
            cursor.execute(query, (id_usuario,))
            conexao.commit()

            if cursor.rowcount > 0:
                print(f"Usuário com ID {id_usuario} deletado com sucesso.")
            else:
                print(f"Não foi possível deletar o usuário com ID {id_usuario}.")
            
            cursor.close()
            conexao.close()
        else:
            print("Não foi possível conectar ao banco de dados.")
    except mysql.connector.Error as erro:
        print(f"Erro ao deletar usuário: {erro}")


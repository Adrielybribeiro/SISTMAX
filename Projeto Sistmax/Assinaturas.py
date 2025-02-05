import mysql.connector
from mysql.connector import Error
from datetime import datetime, timedelta 

# Função de conexão com o banco de dados
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
# Função para listar assinaturas
def listar_assinaturas():
    try:
        conexao = conectar()
        if conexao:
            cursor = conexao.cursor()
            cursor.execute("SELECT a.id, u.nome, a.plano, a.data_inicio, a.data_fim, a.status FROM assinaturas a JOIN usuarios u ON a.usuario_id = u.id")
            assinaturas = cursor.fetchall()

            if assinaturas:
                print(f"\n{'ID':<5} {'Usuário':<20} {'Plano':<15} {'Data Início':<20} {'Data Fim':<20} {'Status':<10}")
                print("-" * 90)
                for assinatura in assinaturas:
                    print(f"{assinatura[0]:<5} {assinatura[1]:<20} {assinatura[2]:<15} {assinatura[3]:<20} {assinatura[4]:<20} {assinatura[5]:<10}")
            else:
                print("Nenhuma assinatura encontrada.")
            
            cursor.close()
            conexao.close()
    except mysql.connector.Error as erro:
        print(f"Erro ao listar assinaturas: {erro}")

# Função para criar assinatura
def criar_assinatura():
    try:
        usuario_id = input("\nDigite o ID do usuário para a assinatura: ").strip()
        
        planos_validos = ['Básico + Anúncios', 'Pro', 'Premium']
        while True:
            plano = input(f"Escolha o plano de assinatura ({', '.join(planos_validos)}): ").strip()
            if plano in planos_validos:
                break
            else:
                print("Plano inválido. Tente novamente.")

        # Definir as datas de início e fim da assinatura
        data_inicio = datetime.now()
        data_fim = data_inicio + timedelta(days=30)  # 30 dias de duração para todos os planos

        status = 'ativa'

        conexao = conectar()
        if conexao:
            cursor = conexao.cursor()
            query = "INSERT INTO assinaturas (usuario_id, plano, data_inicio, data_fim, status) VALUES (%s, %s, %s, %s, %s)"
            valores = (usuario_id, plano, data_inicio, data_fim, status)
            cursor.execute(query, valores)
            conexao.commit()
            print(f"\nAssinatura criada para o usuário com ID {usuario_id} no plano '{plano}'.")

            cursor.close()
            conexao.close()
    except mysql.connector.Error as erro:
        print(f"Erro ao criar assinatura: {erro}")

# Função para atualizar assinatura
def atualizar_assinatura():
    try:
        assinatura_id = input("\nDigite o ID da assinatura a ser atualizada: ").strip()
        
        planos_validos = ['Básico + Anúncios', 'Pro', 'Premium']
        while True:
            novo_plano = input(f"Escolha o novo plano de assinatura ({', '.join(planos_validos)}): ").strip()
            if novo_plano in planos_validos:
                break
            else:
                print("Plano inválido. Tente novamente.")

        # Atualizar a data de fim para 30 dias a partir de hoje
        nova_data_fim = datetime.now() + timedelta(days=30)

        conexao = conectar()
        if conexao:
            cursor = conexao.cursor()
            query = "UPDATE assinaturas SET plano = %s, data_fim = %s WHERE id = %s"
            valores = (novo_plano, nova_data_fim, assinatura_id)
            cursor.execute(query, valores)
            conexao.commit()

            if cursor.rowcount > 0:
                print(f"\nAssinatura de ID {assinatura_id} atualizada para o plano '{novo_plano}'.")
            else:
                print("\nAssinatura não encontrada.")
            
            cursor.close()
            conexao.close()
    except mysql.connector.Error as erro:
        print(f"Erro ao atualizar assinatura: {erro}")

# Função para deletar assinatura
def deletar_assinatura():
    try:
        assinatura_id = input("\nDigite o ID da assinatura a ser deletada: ").strip()

        conexao = conectar()
        if conexao:
            cursor = conexao.cursor()
            query = "DELETE FROM assinaturas WHERE id = %s"
            cursor.execute(query, (assinatura_id,))
            conexao.commit()

            if cursor.rowcount > 0:
                print(f"\nAssinatura de ID {assinatura_id} deletada com sucesso.")
            else:
                print("\nAssinatura não encontrada.")
            
            cursor.close()
            conexao.close()
    except mysql.connector.Error as erro:
        print(f"Erro ao deletar assinatura: {erro}")

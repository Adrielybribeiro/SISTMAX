import mysql.connector
from mysql.connector import Error

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

# Função para listar usuários
def listar_usuarios():
    try:
        conexao = conectar()
        if conexao:
            cursor = conexao.cursor()
            cursor.execute("SELECT id, nome, email, tipo_usuario FROM usuarios")
            usuarios = cursor.fetchall()

            if usuarios:
                print(f"\n{'ID':<5} {'Nome':<25} {'E-mail':<30} {'Tipo de Usuário':<15}")
                print("-" * 75)
                for usuario in usuarios:
                    print(f"{usuario[0]:<5} {usuario[1]:<25} {usuario[2]:<30} {usuario[3]:<15}")
            else:
                print("Nenhum usuário encontrado.")
            
            cursor.close()
            conexao.close()
    except mysql.connector.Error as erro:
        print(f"Erro ao listar usuários: {erro}")

# Função para criar usuário
def criar_usuario():
    try:
        nome = input("\nDigite o nome do usuário: ").strip()
        email = input("Digite o e-mail do usuário: ").strip()
        senha = input("Digite a senha do usuário: ").strip()

        planos_validos = ['básico + anúncios', 'pro', 'premium']
        while True:
            tipo_usuario = input(f"Escolha o plano de usuário ({', '.join(planos_validos)}): ").strip().lower()
            if tipo_usuario in planos_validos:
                break
            else:
                print("Plano inválido. Tente novamente.")

        conexao = conectar()
        if conexao:
            cursor = conexao.cursor()
            query = "INSERT INTO usuarios (nome, email, senha, tipo_usuario) VALUES (%s, %s, %s, %s)"
            valores = (nome, email, senha, tipo_usuario)
            cursor.execute(query, valores)
            conexao.commit()
            print(f"\nUsuário '{nome}' criado com sucesso com o plano '{tipo_usuario}'.")
            
            cursor.close()
            conexao.close()
    except mysql.connector.Error as erro:
        print(f"Erro ao criar o usuário: {erro}")

# Função para atualizar usuário
def atualizar_usuario():
    try:
        usuario_id = input("\nDigite o ID do usuário a ser atualizado: ").strip()
        novo_nome = input("Digite o novo nome: ").strip()
        novo_email = input("Digite o novo e-mail: ").strip()
        novo_tipo = input("Escolha o novo tipo de usuário (básico + anúncios, pro, premium): ").strip().lower()

        conexao = conectar()
        if conexao:
            cursor = conexao.cursor()
            query = "UPDATE usuarios SET nome = %s, email = %s, tipo_usuario = %s WHERE id = %s"
            valores = (novo_nome, novo_email, novo_tipo, usuario_id)
            cursor.execute(query, valores)
            conexao.commit()

            if cursor.rowcount > 0:
                print(f"\nUsuário de ID {usuario_id} atualizado com sucesso.")
            else:
                print(f"\nNenhum usuário encontrado com ID {usuario_id}.")
            
            cursor.close()
            conexao.close()
    except mysql.connector.Error as erro:
        print(f"Erro ao atualizar o usuário: {erro}")

# Função para deletar usuário
def deletar_usuario():
    try:
        usuario_id = input("\nDigite o ID do usuário a ser deletado: ").strip()

        conexao = conectar()
        if conexao:
            cursor = conexao.cursor()
            query = "DELETE FROM usuarios WHERE id = %s"
            cursor.execute(query, (usuario_id,))
            conexao.commit()

            if cursor.rowcount > 0:
                print(f"\nUsuário de ID {usuario_id} deletado com sucesso.")
            else:
                print(f"\nNenhum usuário encontrado com ID {usuario_id}.")
            
            cursor.close()
            conexao.close()
    except mysql.connector.Error as erro:
        print(f"Erro ao deletar o usuário: {erro}")

# Função para exibir o menu
def menu():
    while True:
        print("\n===============================")
        print("   Bem-vindo ao SistMax")
        print("===============================")
        print("1. Criar usuário")
        print("2. Listar usuários")
        print("3. Editar/Atualizar usuário")
        print("4. Deletar usuário")
        print("5. Sair")
        
        opcao = input("\nDigite o número da opção desejada: ").strip()

        if opcao == '1':
            criar_usuario()
        elif opcao == '2':
            listar_usuarios()
        elif opcao == '3':
            atualizar_usuario()
        elif opcao == '4':
            deletar_usuario()
        elif opcao == '5':
            print("\nSaindo... Até logo!")
            break
        else:
            print("\nOpção inválida. Por favor, escolha uma opção válida.")

# Chamar a função de menu
menu()

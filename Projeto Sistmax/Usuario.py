import mysql.connector
from mysql.connector import Error
from colorama import Fore, Style

# Função de conexão
def conectar():
    try:
        conexao = mysql.connector.connect(
            host="localhost",
            port="3306",
            user="root",
            password="",
            database="SISTMAX"
        )
        return conexao
    except Error as e:
        print(Fore.RED + f"Erro ao conectar ao banco de dados: {e}" + Style.RESET_ALL)
        return None

# Função para criar usuário
def criar_usuario():
    try:
        conexao = conectar()
        if conexao:
            nome = input("Digite o nome do usuário: ")
            email = input("Digite o e-mail do usuário: ")
            senha = input("Digite a senha do usuário: ")
            tipo_usuario = input("Escolha o plano de usuário (BÁSICO, PRO, PREMIUM): ").strip().lower()

            # Lista de opções válidas
            correcao_planos = {
                "básico": "BÁSICO",
                "pro": "PRO",
                "premium": "PREMIUM"
            }

            # Verifica se o plano informado é válido
            if tipo_usuario in correcao_planos:
                tipo_usuario = correcao_planos[tipo_usuario]
            else:
                print(Fore.RED + "Plano inválido. Tente novamente." + Style.RESET_ALL)
                return

            cursor = conexao.cursor()
            query = "INSERT INTO usuarios (nome, email, senha, tipo_usuario) VALUES (%s, %s, SHA2(%s, 256), %s)"
            valores = (nome, email, senha, tipo_usuario)
            cursor.execute(query, valores)
            conexao.commit()

            print(f"\nUsuário '{nome}' criado com sucesso!")
            cursor.close()
            conexao.close()
        else:
            print(Fore.RED + "Não foi possível conectar ao banco de dados." + Style.RESET_ALL)
    except mysql.connector.Error as erro:
        print(Fore.RED + f"Erro ao criar usuário: {erro}" + Style.RESET_ALL)

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
                print(Fore.RED + "Nenhum usuário encontrado." + Style.RESET_ALL)

            cursor.close()
            conexao.close()
        else:
            print(Fore.RED + "Não foi possível conectar ao banco de dados." + Style.RESET_ALL)
    except mysql.connector.Error as erro:
        print(Fore.RED + f"Erro ao consultar usuários: {erro}" + Style.RESET_ALL)

# Função para atualizar usuário
def atualizar_usuario():
    try:
        conexao = conectar()
        if conexao:
            id_usuario = int(input("Digite o ID do usuário que deseja atualizar: "))
            novo_nome = input("Digite o novo nome do usuário: ")
            novo_email = input("Digite o novo e-mail do usuário: ")
            novo_tipo = input("Escolha o novo plano de usuário (BÁSICO, PRO, PREMIUM): ").strip().lower()

            # Lista de opções válidas
            correcao_planos = {
                "básico": "BÁSICO",
                "pro": "PRO",
                "premium": "PREMIUM"
            }

            # Verifica se o plano informado é válido
            if novo_tipo in correcao_planos:
                novo_tipo = correcao_planos[novo_tipo]
            else:
                print(Fore.RED + "Plano inválido. Tente novamente." + Style.RESET_ALL)
                return

            cursor = conexao.cursor()
            query = "UPDATE usuarios SET nome = %s, email = %s, tipo_usuario = %s WHERE id = %s"
            valores = (novo_nome, novo_email, novo_tipo, id_usuario)
            cursor.execute(query, valores)
            conexao.commit()

            if cursor.rowcount > 0:
                print(f"Usuário com ID {id_usuario} atualizado com sucesso.")
            else:
                print(Fore.RED + f"Não foi possível atualizar o usuário com ID {id_usuario}." + Style.RESET_ALL)

            cursor.close()
            conexao.close()
        else:
            print(Fore.RED + "Não foi possível conectar ao banco de dados." + Style.RESET_ALL)
    except mysql.connector.Error as erro:
        print(Fore.RED + f"Erro ao atualizar usuário: {erro}" + Style.RESET_ALL)

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
                print(Fore.RED + f"Não foi possível deletar o usuário com ID {id_usuario}." + Style.RESET_ALL)

            cursor.close()
            conexao.close()
        else:
            print(Fore.RED + "Não foi possível conectar ao banco de dados." + Style.RESET_ALL)
    except mysql.connector.Error as erro:
        print(Fore.RED + f"Erro ao deletar usuário: {erro}" + Style.RESET_ALL)

# Função para o menu principal
def menu_principal():
    while True:
        print(Fore.MAGENTA + "\n===== SISTEMA DE USUÁRIOS =====" + Style.RESET_ALL)
        print("1 - Criar Usuário")
        print("2 - Atualizar Usuário")
        print("3 - Listar Usuários")
        print("4 - Deletar Usuário")
        print("5 - Sair")
        opcao = input("\nEscolha uma opção: ")

        if opcao == '1':
            criar_usuario()
        elif opcao == '2':
            atualizar_usuario()
        elif opcao == '3':
            listar_usuarios()
        elif opcao == '4':
            deletar_usuario()
        elif opcao == '5':
            print(Fore.CYAN + "Saindo do sistema..." + Style.RESET_ALL)
            break
        else:
            print(Fore.RED + "Opção inválida! Tente novamente." + Style.RESET_ALL)

# Chama a função de menu principal
if __name__ == "__main__":
    menu_principal()

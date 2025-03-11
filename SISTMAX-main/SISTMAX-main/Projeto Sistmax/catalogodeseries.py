import mysql.connector
from mysql.connector import Error
from datetime import datetime
from colorama import Fore, Style, init

init(autoreset=True)

def conectar():
    """Estabelece conexão com o banco de dados."""
    try:
        conexao = mysql.connector.connect(
            host="localhost",
            port="3307",
            user="root",
            password="",
            database="SISTMAX"
        )
        if conexao.is_connected():
            print(Fore.GREEN + "Conexão estabelecida com sucesso!" + Style.RESET_ALL)
        return conexao
    except Error as e:
        print(Fore.RED + f"Erro ao conectar ao banco de dados: {e}" + Style.RESET_ALL)
        return None

def validar_entrada_int(mensagem):
    """Valida entrada de inteiros do usuário."""
    while True:
        try:
            return int(input(mensagem))
        except ValueError:
            print(Fore.RED + "Entrada inválida. Digite um número inteiro." + Style.RESET_ALL)

def adicionar_serie():
    """Adiciona uma nova série ao banco de dados."""
    try:
        titulo = input("Digite o título da série: ")
        descricao = input("Digite a descrição da série: ")
        categoria = input("Digite a categoria da série (ex: ação, drama): ")
        ano_lancamento = validar_entrada_int("Digite o ano de lançamento da série: ")
        duracao = validar_entrada_int("Digite a duração média de cada episódio em minutos: ")
        classificacao = input("Digite a classificação indicativa da série: ")
        imagem_url = input("Digite a URL da imagem da capa ou poster: ")
        
        conexao = conectar()
        if conexao:
            cursor = conexao.cursor()
            query = """
                INSERT INTO conteudos (titulo, descricao, categoria, ano_lancamento, tipo, duracao_minutos, classificacao_indicativa, imagem_url)
                VALUES (%s, %s, %s, %s, 'serie', %s, %s, %s)
            """
            valores = (titulo, descricao, categoria, ano_lancamento, duracao, classificacao, imagem_url)
            cursor.execute(query, valores)
            conexao.commit()
            print(Fore.GREEN + f"Série '{titulo}' adicionada com sucesso!" + Style.RESET_ALL)
    except mysql.connector.Error as erro:
        print(Fore.RED + f"Erro ao adicionar série: {erro}" + Style.RESET_ALL)
    finally:
        if conexao:
            cursor.close()
            conexao.close()

def listar_series():
    """Lista todas as séries cadastradas."""
    try:
        conexao = conectar()
        if conexao:
            cursor = conexao.cursor()
            cursor.execute("SELECT id, titulo, ano_lancamento, categoria, duracao_minutos FROM conteudos WHERE tipo = 'serie'")
            series = cursor.fetchall()

            if series:
                print("\n===== Lista de Séries =====")
                print(f"{'ID':<5} {'Título':<30} {'Ano':<5} {'Categoria':<15} {'Duração':<10}")
                for serie in series:
                    print(f"{serie[0]:<5} {serie[1]:<30} {serie[2]:<5} {serie[3]:<15} {serie[4]:<10}")
            else:
                print(Fore.RED + "Nenhuma série encontrada." + Style.RESET_ALL)
    except mysql.connector.Error as erro:
        print(Fore.RED + f"Erro ao listar séries: {erro}" + Style.RESET_ALL)
    finally:
        if conexao:
            cursor.close()
            conexao.close()

def excluir_serie():
    """Exclui uma série do banco de dados pelo ID."""
    try:
        serie_id = validar_entrada_int("Digite o ID da série a ser excluída: ")
        conexao = conectar()
        if conexao:
            cursor = conexao.cursor()
            query = "DELETE FROM conteudos WHERE id = %s AND tipo = 'serie'"
            cursor.execute(query, (serie_id,))
            conexao.commit()
            print(Fore.GREEN + f"Série com ID {serie_id} excluída com sucesso!" + Style.RESET_ALL)
    except mysql.connector.Error as erro:
        print(Fore.RED + f"Erro ao excluir série: {erro}" + Style.RESET_ALL)
    finally:
        if conexao:
            cursor.close()
            conexao.close()

def menu():
    while True:
        print(Fore.MAGENTA + "\n===== Bem-vindo ao Catálogo de Filmes e Séries =====" + Style.RESET_ALL)
        print("1. Adicionar série")
        print("2. Listar séries")
        print("3. Excluir série")
        print("4. Sair")
        opcao = validar_entrada_int("\nEscolha uma opção: ")
        
        if opcao == 1:
            adicionar_serie()
        elif opcao == 2:
            listar_series()
        elif opcao == 3:
            excluir_serie()
        elif opcao == 4:
            print(Fore.YELLOW + "Saindo do sistema..." + Style.RESET_ALL)
            break
        else:
            print(Fore.RED + "Opção inválida! Tente novamente." + Style.RESET_ALL)

if __name__ == "__main__":
    menu()

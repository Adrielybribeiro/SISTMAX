import mysql.connector
from mysql.connector import Error
from datetime import datetime
from colorama import Fore, Style

# Função de conexão com o banco de dados
def conectar():
    try:
        conexao = mysql.connector.connect(
            host="localhost",
            port="3307",
            user="root",
            password="",
            database="SISTMAX"
        )
        return conexao
    except Error as e:
        print(Fore.RED + f"Erro ao conectar ao banco de dados: {e}" + Style.RESET.ALL)
        return None

# Função para adicionar uma nova série
def adicionar_serie():
    try:
        titulo = input("Digite o título da série: ")
        descricao = input("Digite a descrição da série: ")
        categoria = input("Digite a categoria da série (ex: ação, drama): ")
        ano_lancamento = int(input("Digite o ano de lançamento da série: "))
        duracao = int(input("Digite a duração média de cada episódio em minutos: "))
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
            print(f"Série '{titulo}' adicionada com sucesso.")
            cursor.close()
            conexao.close()
    except mysql.connector.Error as erro:
        print(Fore.RED + f"Erro ao adicionar série: {erro}"+ Style.RESET.ALL)

# Função para listar todas as séries
def listar_series():
    try:
        conexao = conectar()
        if conexao:
            cursor = conexao.cursor()
            cursor.execute("SELECT * FROM conteudos WHERE tipo = 'serie'")
            series = cursor.fetchall()

            if series:
                print("\nLista de Séries:")
                print(f"{'ID':<5} {'Título':<30} {'Ano':<5} {'Categoria':<15} {'Duração':<10}")
                for serie in series:
                    print(f"{serie[0]:<5} {serie[1]:<30} {serie[4]:<5} {serie[3]:<15} {serie[6]:<10}")
            else:
                print(Fore.RED + "Nenhuma série encontrada." + Style.RESET.ALL)
            
            cursor.close()
            conexao.close()
    except mysql.connector.Error as erro:
        print(Fore.RED + f"Erro ao listar séries: {erro}" + Style.RESET.ALL)

# Função para adicionar um episódio a uma série
def adicionar_episodio():
    try:
        conteudo_id = int(input("Digite o ID da série: "))
        temporada = int(input("Digite o número da temporada: "))
        numero_episodio = int(input("Digite o número do episódio: "))
        titulo = input("Digite o título do episódio: ")
        duracao = int(input("Digite a duração do episódio em minutos: "))
        descricao = input("Digite a descrição do episódio: ")

        conexao = conectar()
        if conexao:
            cursor = conexao.cursor()
            query = """
                INSERT INTO episodios (conteudo_id, temporada, numero_episodio, titulo, duracao_minutos, descricao)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            valores = (conteudo_id, temporada, numero_episodio, titulo, duracao, descricao)
            cursor.execute(query, valores)
            conexao.commit()
            print(f"Episódio '{titulo}' adicionado à série com ID {conteudo_id}.")
            cursor.close()
            conexao.close()
    except mysql.connector.Error as erro:
        print(Fore.RED + f"Erro ao adicionar episódio: {erro}" + Style.RESET.ALL)

# Função para avaliar uma série
def avaliar_serie():
    try:
        usuario_id = int(input("Digite seu ID de usuário: "))
        conteudo_id = int(input("Digite o ID da série a ser avaliada: "))
        nota = float(input("Digite sua nota para a série (de 1 a 10): "))
        comentario = input("Digite seu comentário sobre a série: ")

        conexao = conectar()
        if conexao:
            cursor = conexao.cursor()
            query = """
                INSERT INTO avaliacoes (usuario_id, conteudo_id, nota, comentario)
                VALUES (%s, %s, %s, %s)
            """
            valores = (usuario_id, conteudo_id, nota, comentario)
            cursor.execute(query, valores)
            conexao.commit()
            print(f"Série com ID {conteudo_id} avaliada com sucesso.")
            cursor.close()
            conexao.close()
    except mysql.connector.Error as erro:
        print(Fore.RED + f"Erro ao avaliar série: {erro}" + Style.RESET.ALL)

# Função para adicionar uma série aos favoritos
def adicionar_favorito():
    try:
        usuario_id = int(input("Digite seu ID de usuário: "))
        conteudo_id = int(input("Digite o ID da série a ser adicionada aos favoritos: "))

        conexao = conectar()
        if conexao:
            cursor = conexao.cursor()
            query = """
                INSERT INTO favoritos (usuario_id, conteudo_id)
                VALUES (%s, %s)
            """
            valores = (usuario_id, conteudo_id)
            cursor.execute(query, valores)
            conexao.commit()
            print(f"Série com ID {conteudo_id} adicionada aos favoritos.")
            cursor.close()
            conexao.close()
    except mysql.connector.Error as erro:
        print(Fore.RED + f"Erro ao adicionar aos favoritos: {erro}" + Style.RESET.ALL)

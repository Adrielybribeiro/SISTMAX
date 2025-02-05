import mysql.connector
from mysql.connector import Error

# Função para conectar ao banco de dados
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

# Função para adicionar filme
def adicionar_filme(titulo, ano, genero, diretor, duracao):
    try:
        conexao = conectar()
        if conexao:
            cursor = conexao.cursor()
            query = "INSERT INTO filmes (titulo, ano, genero, diretor, duracao) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query, (titulo, ano, genero, diretor, duracao))
            conexao.commit()
            print(f"Filme '{titulo}' adicionado ao catálogo.")
            cursor.close()
            conexao.close()
    except mysql.connector.Error as erro:
        print(f"Erro ao adicionar filme: {erro}")

# Função para listar filmes
def listar_filmes():
    try:
        conexao = conectar()
        if conexao:
            cursor = conexao.cursor()
            cursor.execute("SELECT * FROM filmes")
            filmes = cursor.fetchall()
            if filmes:
                print(f"\n{'ID':<5} {'Título':<20} {'Ano':<10} {'Gênero':<15} {'Diretor':<20} {'Duração':<10}")
                print("-" * 75)
                for filme in filmes:
                    print(f"{filme[0]:<5} {filme[1]:<20} {filme[2]:<10} {filme[3]:<15} {filme[4]:<20} {filme[5]:<10}")
            else:
                print("Nenhum filme no catálogo.")
            cursor.close()
            conexao.close()
    except mysql.connector.Error as erro:
        print(f"Erro ao listar filmes: {erro}")

# Função para buscar filme
def buscar_filme(titulo):
    try:
        conexao = conectar()
        if conexao:
            cursor = conexao.cursor()
            query = "SELECT * FROM filmes WHERE titulo LIKE %s"
            cursor.execute(query, ('%' + titulo + '%',))
            filmes = cursor.fetchall()
            if filmes:
                print(f"\n{'ID':<5} {'Título':<20} {'Ano':<10} {'Gênero':<15} {'Diretor':<20} {'Duração':<10}")
                print("-" * 75)
                for filme in filmes:
                    print(f"{filme[0]:<5} {filme[1]:<20} {filme[2]:<10} {filme[3]:<15} {filme[4]:<20} {filme[5]:<10}")
            else:
                print(f"Nenhum filme encontrado com o título '{titulo}'.")
            cursor.close()
            conexao.close()
    except mysql.connector.Error as erro:
        print(f"Erro ao buscar filme: {erro}")

# Função principal de menu
def menu():
    while True:
        print("\nCatálogo de Filmes")
        print("1. Adicionar filme")
        print("2. Listar filmes")
        print("3. Buscar filme por título")
        print("4. Sair")
        
        escolha = input("Escolha uma opção: ")
        
        if escolha == "1":
            titulo = input("Digite o título do filme: ")
            ano = input("Digite o ano do filme: ")
            genero = input("Digite o gênero do filme: ")
            diretor = input("Digite o nome do diretor: ")
            duracao = input("Digite a duração do filme (em minutos): ")
            adicionar_filme(titulo, ano, genero, diretor, duracao)
        elif escolha == "2":
            listar_filmes()
        elif escolha == "3":
            titulo = input("Digite o título do filme que deseja buscar: ")
            buscar_filme(titulo)
        elif escolha == "4":
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")

# Iniciar o menu
menu()

import sqlite3
import os

# Nome do Banco de Dados
DB_NAME = "dados_sensores.db"

def criar_banco():
    # Verifica se o banco já existe para não sobreescrever (opcional)
    if os.path.exists(DB_NAME):
        print(f"O banco '{DB_NAME}' já existe. Verificando tabelas...")
    
    # Conecta ao banco (o arquivo será criado se não existir)
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # 1. Criação da Tabela de Leituras (Sensores)
    print("Criando tabela 'leituras'...")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS leituras (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data_hora DATETIME,
            tensao REAL,
            corrente REAL,
            temperatura REAL,
            status_rele TEXT
        )
    ''')

    # 2. Criação da Tabela de Logs (Eventos do Sistema/IA)
    print("Criando tabela 'logs_eventos'...")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs_eventos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data_hora DATETIME,
            tipo TEXT,
            descricao TEXT
        )
    ''')
    
    conn.commit()
    conn.close()
    print(f"\n[SUCESSO] Banco de dados '{DB_NAME}' configurado com sucesso!")

if __name__ == "__main__":
    criar_banco()

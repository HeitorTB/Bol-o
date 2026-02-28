import sqlite3
class database:
    conn = None
    nome_bd = "tabela.db"
      
    def criar_tabelas(cls):
        cls.abrir()

        cls.execute("""
            CREATE TABLE IF NOT EXISTS usuario (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                nome TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE, 
                senha TEXT NOT NULL,
                pontos INTEGER
            );
        """)

        cls.execute("""
            CREATE TABLE IF NOT EXISTS jogos
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                time_a TEXT NOT NULL, 
                time_b TEXT NOT NULL,
                data_hora DATETIME, 
                gols_time_a INTEGER,
                gols_time_b INTEGER,
                finalizado BOOLEAN
        """)

        cls.execute("""
            CREATE TABLE IF NOT EXISTS palpites
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                FOREIGN KEY(usuario_id) REFERENCES usuario(id), 
                FOREIGN KEY(jogo_id) REFERENCES jogo(id),
                gols_time_a INTEGER,
                gols_time_b INTEGER,
                pontos_ganhos INTEGER, 
        """)

        

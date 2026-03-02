import libsql_client as libsql
import streamlit as st

class database:
    conn = None
    
    @classmethod
    def abrir(cls):
        # 1. Pega as chaves de acesso do Streamlit Secrets
        url_banco = st.secrets["TURSO_DATABASE_URL"]
        token_banco = st.secrets["TURSO_AUTH_TOKEN"]
        
        # 2. Conecta no Turso (Ajustado para a sintaxe correta do libsql-client)
        # Usamos o sync para facilitar o uso com Streamlit
        cls.conn = libsql.create_client_sync(url=url_banco, auth_token=token_banco)
        
        # O libsql-client sync já gerencia a conexão, mas se precisar rodar PRAGMAs:
        cls.conn.execute("PRAGMA foreign_keys = ON") 

    @classmethod
    def fechar(cls):
        if cls.conn:
            cls.conn.close()

    @classmethod
    def execute(cls, sql, params=None):
        # O libsql-client não usa cursor() da mesma forma que o sqlite3 padrão
        # Ele permite executar direto da conexão
        resultado = cls.conn.execute(sql, params or [])
        return resultado

    @classmethod
    def criar_tabelas(cls):
        cls.abrir()

        # Tabela Usuário 
        cls.execute("""
            CREATE TABLE IF NOT EXISTS usuario (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                nome TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE, 
                senha TEXT NOT NULL,
                pontos INTEGER
            );
        """)

        # Tabela Jogos 
        cls.execute("""
            CREATE TABLE IF NOT EXISTS jogos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                time_a TEXT NOT NULL, 
                time_b TEXT NOT NULL,
                data_hora DATETIME, 
                gols_time_a INTEGER,
                gols_time_b INTEGER,
                finalizado BOOLEAN
            );
        """)

        # Tabela Palpites 
        cls.execute("""
            CREATE TABLE IF NOT EXISTS palpites (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                usuario_id INTEGER, 
                jogo_id INTEGER,    
                gols_time_a INTEGER,
                gols_time_b INTEGER,
                pontos_ganhos INTEGER, 
                FOREIGN KEY(usuario_id) REFERENCES usuario(id), 
                FOREIGN KEY(jogo_id) REFERENCES jogos(id) 
            ); 
        """)
        
        cls.fechar()
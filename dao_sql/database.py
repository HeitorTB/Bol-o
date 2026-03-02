import libsql_client as libsql
import streamlit as st

class database:
    
    @classmethod
    def abrir(cls):
        # 1. Deixamos vazio para neutralizar os 'abrir()' espalhados pelo seu sistema
        pass 

    @classmethod
    def fechar(cls):
        # 2. Deixamos vazio para neutralizar os 'fechar()' espalhados pelo seu sistema
        pass 

    @classmethod
    def execute(cls, sql, params=None):
        url_banco = st.secrets["TURSO_DATABASE_URL"]
        token_banco = st.secrets["TURSO_AUTH_TOKEN"]
        
        # Força a usar o formato de link correto
        if url_banco.startswith("libsql://"):
            url_banco = url_banco.replace("libsql://", "https://")
        elif url_banco.startswith("wss://"):
            url_banco = url_banco.replace("wss://", "https://")
            
        # 🛡️ 3. A SOLUÇÃO DEFINITIVA: O bloco 'with'
        # Ele abre a conexão, executa o SQL e GARANTE que ela seja fechada e devolvida
        # para o sistema operacional instantaneamente, custe o que custar.
        with libsql.create_client_sync(url=url_banco, auth_token=token_banco) as conn:
            return conn.execute(sql, params or [])

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
                pontos INTEGER DEFAULT 0
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
                finalizado BOOLEAN DEFAULT FALSE
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
                pontos_ganhos INTEGER DEFAULT 0, 
                FOREIGN KEY(usuario_id) REFERENCES usuario(id), 
                FOREIGN KEY(jogo_id) REFERENCES jogos(id) 
            ); 
        """)
        
        cls.fechar()
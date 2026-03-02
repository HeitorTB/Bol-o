import libsql_client as libsql
import streamlit as st

class database:
    conn = None
    
    @staticmethod
    @st.cache_resource # 🌟 A MÁGICA DO STREAMLIT CONTINUA AQUI 🌟
    def abrir(): # Mudamos o nome de volta para 'abrir' para ficar no seu padrão!
        url_banco = st.secrets["TURSO_DATABASE_URL"]
        token_banco = st.secrets["TURSO_AUTH_TOKEN"]
        
        # Força o uso de HTTPS para evitar o erro 505
        if url_banco.startswith("libsql://"):
            url_banco = url_banco.replace("libsql://", "https://")
        elif url_banco.startswith("wss://"):
            url_banco = url_banco.replace("wss://", "https://")
        
        try:
            # Cria a conexão UMA ÚNICA VEZ e guarda na memória
            conn = libsql.create_client_sync(url=url_banco, auth_token=token_banco)
            conn.execute("PRAGMA foreign_keys = ON") 
            return conn # Importante: o abrir agora "devolve" a conexão pronta
        except Exception as e:
            st.error(f"Erro crítico ao conectar no banco: {e}")
            return None

    @classmethod
    def fechar(cls):
        # Deixamos vazio para não quebrar seu código antigo, 
        # pois agora o Streamlit gerencia a conexão sozinho!
        pass 

    @classmethod
    def execute(cls, sql, params=None):
        # Pega a conexão inteligente chamando o seu 'abrir'
        conn = cls.abrir()
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
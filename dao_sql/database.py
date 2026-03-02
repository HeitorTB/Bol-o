import libsql_client as libsql
import streamlit as st

# 🌟 1. A FUNÇÃO MÁGICA AGORA FICA DO LADO DE FORA DA CLASSE 🌟
@st.cache_resource
def get_conexao_turso():
    url_banco = st.secrets["TURSO_DATABASE_URL"]
    token_banco = st.secrets["TURSO_AUTH_TOKEN"]
    
    # Força o HTTPS para evitar o erro 505
    if url_banco.startswith("libsql://"):
        url_banco = url_banco.replace("libsql://", "https://")
    elif url_banco.startswith("wss://"):
        url_banco = url_banco.replace("wss://", "https://")
    
    try:
        conn = libsql.create_client_sync(url=url_banco, auth_token=token_banco)
        conn.execute("PRAGMA foreign_keys = ON") 
        return conn
    except Exception as e:
        st.error(f"Erro crítico ao conectar no banco: {e}")
        return None

# 🌟 2. A SUA CLASSE FICA MUITO MAIS SIMPLES AGORA 🌟
class database:
    
    @classmethod
    def abrir(cls):
        # Mantemos a função vazia só para não dar erro no seu código antigo!
        pass 

    @classmethod
    def fechar(cls):
        # Também mantemos vazia, o Streamlit cuida disso sozinho agora.
        pass 

    @classmethod
    def execute(cls, sql, params=None):
        # Ele puxa a conexão global que o Streamlit guardou na memória
        conn = get_conexao_turso()
        if conn:
            return conn.execute(sql, params or [])
        return None

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
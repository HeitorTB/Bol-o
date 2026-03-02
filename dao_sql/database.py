import libsql_client as libsql
import streamlit as st

class database:
    
    @staticmethod
    @st.cache_resource # 🌟 A MÁGICA DO STREAMLIT AQUI 🌟
    def abrir():
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
            return conn
        except Exception as e:
            st.error(f"Erro crítico ao conectar no banco: {e}")
            return None

    @classmethod
    def fechar(cls):
        # Deixamos vazio para não dar erro no seu código antigo, 
        # pois agora o Streamlit gerencia a conexão sozinho!
        pass 

    @classmethod
    def execute(cls, sql, params=None):
        # Pega a conexão inteligente salva na memória
        conn = cls.get_conexao()
        return conn.execute(sql, params or [])

    @classmethod
    def criar_tabelas(cls):
        # ... AQUI PARA BAIXO VOCÊ MANTÉM O SEU CÓDIGO EXATAMENTE COMO ESTÁ ...
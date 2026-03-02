import libsql_client as libsql
import streamlit as st

class database:
    conn = None
    
    @classmethod
    def abrir(cls):
        # 1. Pega as chaves de acesso do Streamlit Secrets
        url_banco = st.secrets["TURSO_DATABASE_URL"]
        token_banco = st.secrets["TURSO_AUTH_TOKEN"]
        
        # 2. Força o HTTPS por garantia (caso ainda esteja libsql:// nos secrets locais)
        if url_banco.startswith("libsql://"):
            url_banco = url_banco.replace("libsql://", "https://")
        elif url_banco.startswith("wss://"):
            url_banco = url_banco.replace("wss://", "https://")
        
        try:
            # 3. Cria uma NOVA conexão sempre que for chamado
            cls.conn = libsql.create_client_sync(url=url_banco, auth_token=token_banco)
            cls.conn.execute("PRAGMA foreign_keys = ON") 
        except Exception as e:
            st.error(f"Erro crítico ao conectar no banco: {e}")

    @classmethod
    def fechar(cls):
        if cls.conn is not None:
            try:
                cls.conn.close()
            except:
                pass
            cls.conn = None # ISSO AQUI EVITA O ERRO CLIENT_CLOSED!

    @classmethod
    def execute(cls, sql, params=None):
        # Para o Streamlit, o jeito mais seguro é abrir, executar e fechar a cada comando
        cls.abrir()
        resultado = cls.conn.execute(sql, params or [])
        cls.fechar() # Fecha limpinho logo após o uso
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
import streamlit as st
from streamlit_gsheets import GSheetsConnection

class DAO:
    # Mudamos para uma função para garantir que a conexão seja refrescada se falhar
    @classmethod
    def get_conn(cls):
        return st.connection("gsheets", type=GSheetsConnection)

    @classmethod
    def abrir(cls): pass

    @classmethod
    def fechar(cls): pass

    @classmethod
    def listar_aba(cls, nome_aba):
        conn = cls.get_conn()
        # O ttl=0 é importante para ler dados novos, mas o nome da aba deve ser exato
        return conn.read(worksheet=nome_aba, ttl=10)

    @classmethod
    def salvar_aba(cls, nome_aba, df):
        conn = cls.get_conn()
        conn.update(worksheet=nome_aba, data=df)
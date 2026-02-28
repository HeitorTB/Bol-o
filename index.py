import streamlit as st
from templates.loginUI import LoginUI
from templates.abrirContaUI import AbrirContaUI
from templates.minhasApostasUI import MinhasApostasUI
from templates.CadastrarJogosUI import cadastrarJogoUI
from templates.atualizarPlacarUI import AtualizarPlacarUI
from views import View
from dao_sql.database import database

if __name__ == "__main__":
    try:
        database.criar_tabelas()
    except Exception as e:
        st.error(f"Erro ao conectar no banco {e}")
class IndexUI: 
    
    @staticmethod
    def menu_visitante():
        op = st.sidebar.selectbox("Menu", ["Entrar no Sistema","Abrir Conta"])
        if op == "Entrar no Sistema": LoginUI.main()
        if op == "Abrir Conta": AbrirContaUI.main()
    
    @staticmethod
    def menu_usuario():
        op = st.sidebar.selectbox("Menu", ["Minhas Apostas", "Visualizar Placar"])
        if op == "Minhas apostas": MinhasApostasUI.main()
        if op == "Visualizar Placar": visualizarPlacarUI.main()
    
    @staticmethod
    def sidebar():
        if "usuario_id" not in st.session_state:
            IndexUI.menu_visitante()
        else:
            st.sidebar.write("Bem-vindo(a), " + st.session_state["usuario_nome"] + " ⚽")
            if st.session_state["usuario_nome"] == "admin":
                IndexUI.menu_admin()
            else:
                IndexUI.menu_usuario()

    @staticmethod
    def menu_admin():
        op = st.sidebar.selectbox("Menu",["Cadastrar jogos", "Atualizar Resultados"])
        if op == "Cadastrar jogos": cadastrarJogoUI.main()
        if op == "Atualizar Resultados": AtualizarPlacarUI.main()

    @staticmethod
    def main():
        View.criar_admin()
        IndexUI.sidebar()

IndexUI.main()
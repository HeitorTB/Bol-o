import streamlit as st
from views import View
import time

class AbrirContaUI:
    def main():
        st.header("Criar uma conta")
        nome = st.text_input("Informe o nome")
        email = st.text_input("Informe o e-mail")
        senha = st.text_input("Informe a senha", type="password")

        if st.button("Inserir"):
            try:
                View.usuario_inserir(nome, email, senha)
                st.success("Conta criada com sucesso!")
            except Exception as erro:
                st.error(erro)
            time.sleep(2)
            st.rerun()
            
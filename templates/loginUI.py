import streamlit as st
from views import View

class LoginUI:
    def main():
        st.header("Entrar")
        email = st.text_input("Informe o e-mail")
        senha = st.text_input("Informe a senha", type="password")

        if st.button("Entrar"):
            usuario_valido = None
            c = View.usuario_autenticar(email, senha)
            if c:
                st.session_state['logado'] = True
                st.session_state['usuario_logado'] = usuario_valido
                st.success("Login realizado com sucesso!")
                st.rerun()
            else:
                st.error("E-mail ou senha incorretos.")

            
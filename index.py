import streamlit as st
from templates import loginUI
from templates import abrirContaUI

class IndexUI: 
    def menu_visitante():
        op = st.sidebar.selectbox("Menu", ["Entrar no Sistema","Abrir Conta"])
        if op == "Entrar": loginUI.main()
        if op == "Abrir Conta": abrirContaUI.main()

    def menu_usuario():
        op = st.sidebar.selectbox("Menu", ["Minhas apostas", "Visualizar Placar"])
        if op == "Minhas apostas": minhasApostasUI.main()
        if op == "Agendar Serviço": visualizarPlacarUI.main()
    
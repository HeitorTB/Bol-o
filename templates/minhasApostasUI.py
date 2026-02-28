import streamlit as st
import time
from views import View

class MinhasApostasUI:
    def main():
        st.header("Faça seus Palpites 🎯")
        usuario_id = st.session_state.get("usuario_id")
        
        

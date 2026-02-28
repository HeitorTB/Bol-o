import streamlit as st
import datetime
from views import View

class cadastrarJogoUI:
    @classmethod
    def main(cls):
        st.header("Cadastrar Novo Jogo ⚽")
        st.write("Preencha os dados da próxima partida:")

        with st.form("form_novo_jogo"):
            time_a = st.text_input("Time A (Mandante)")
            time_b = st.text_input("Time B (Visitante)")

            # O Streamlit tem componentes ótimos para data e hora
            col1, col2 = st.columns(2)
            with col1:
                data = st.date_input("Data do Jogo")
            with col2:
                hora = st.time_input("Hora do Jogo")

            submit = st.form_submit_button("Salvar Jogo")

            if submit:
                if time_a and time_b:
                    # Junta a data e a hora num formato de texto padrão para o banco
                    data_hora = datetime.datetime.combine(data, hora).strftime("%Y-%m-%d %H:%M")
                    
                    # Manda a View salvar
                    View.jogo_inserir(time_a, time_b, data_hora)
                    
                    st.success("Jogo cadastrado com sucesso!")
                else:
                    st.error("Por favor, preencha o nome dos dois times.")
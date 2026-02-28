import streamlit as st
import datetime
import pandas as pd
from views import View

class cadastrarJogoUI:
    @classmethod
    def main(cls):
        st.header("Cadastrar Novo Jogo")
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
                    data_hora = datetime.datetime.combine(data, hora).strftime("%Y-%m-%d %H:%M")
                    
                    View.jogo_inserir(time_a, time_b, data_hora)
                    
                    st.success("Jogo cadastrado com sucesso!")
                else:
                    st.error("Por favor, preencha o nome dos dois times.")
            
        st.header("Jogos cadastrados")
        jogos = View.jogo_listar()

        if not jogos:
            st.info("Nenhum jogo registado no momento.")
            return

        # 2. Preparamos uma lista vazia para organizar os dados linha a linha
        dados = []
        
        for j in jogos:
            # Transforma o True/False do sistema em texto amigável
            status = "Finalizado" if j.get_finalizado() else "Aberto"
            
            # Se o jogo já acabou, mostra o resultado. Se não, mostra uns tracinhos.
            if j.get_finalizado():
                placar = f"{j.get_gols_time_a()} x {j.get_gols_time_b()}"
            else:
                placar = " - x - "

            # Adicionamos a linha à nossa lista
            dados.append({
                "Data e Hora": j.get_data_hora(),
                "Equipa da Casa": j.get_time_a(),
                "Resultado": placar,
                "Equipa Visitante": j.get_time_b(),
                "Estado": status
            })

        # 3. Transformamos a lista na tabela inteligente do Pandas
        df = pd.DataFrame(dados)

        st.write("---")

        # 4. Mostramos no ecrã usando st.dataframe
        # O hide_index=True serve para esconder aquela primeira coluna com números (0, 1, 2...)
        st.dataframe(df, use_container_width=True, hide_index=True)



import streamlit as st
import pandas as pd
from views import View

class MeusPalpitesUI:
    @classmethod
    def main(cls):
        st.header("Meus Palpites 📝")

        if "usuario_id" not in st.session_state:
            st.error("Você precisa estar logado!")
            return

        usuario_id = st.session_state["usuario_id"]

        # Busca as apostas do usuário e a lista de todos os jogos
        palpites = View.palpite_listar_por_usuario(usuario_id)
        todos_jogos = View.jogo_listar()

        if not palpites:
            st.info("Você ainda não fez nenhum palpite. Vá na aba de apostas!")
            return

        # Cria um "dicionário" de jogos para facilitar a busca do nome dos times pelo ID
        dic_jogos = {j.get_id(): j for j in todos_jogos}

        dados = []
        for p in palpites:
            jogo = dic_jogos.get(p.get_jogo_id())
            if jogo:
                status = "Finalizado" if jogo.get_finalizado() else "Aberto"
                
                dados.append({
                    "Data": jogo.get_data_hora(),
                    "Time da Casa": jogo.get_time_a(),
                    "Meu Palpite": f"{p.get_gols_time_a()} x {p.get_gols_time_b()}",
                    "Time Visitante": jogo.get_time_b(),
                    "Status": status,
                    "Pontos Ganhos": p.get_pontos_ganhos()
                })

        df = pd.DataFrame(dados)
        st.dataframe(df, hide_index=True, use_container_width=True)
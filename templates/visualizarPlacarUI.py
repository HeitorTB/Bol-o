import streamlit as st
import pandas as pd
from views import View

class VisualizarPlacarUI:
    @classmethod
    def main(cls):
        st.header("Ranking Geral 🏆")
        st.write("Acompanhe quem são os melhores palpiteiros do bolão!")

        st.header("Ouro: Charles!")
        st.header("Prata: Gustavo Leão")
        st.header("Bronze: Sayonara")

        st.write("Parabéns a todos, até daqui a 4 anos!")
 
        # 1. Chama a nova função que soma os palpites em tempo real
        usuarios_ranking = View.ranking_geral()

        if not usuarios_ranking:
            st.info("Nenhum usuário encontrado.")
            return

        # 2. Monta os dados pegando os pontos somados (pontos_temp)
        dados = []
        for u in usuarios_ranking:
            dados.append({
                "Jogador": u.get_nome(),
                "Pontos Totais": u.pontos_temp # Usamos o valor somado
            })

        # 3. Exibe a tabela com colocação
        df = pd.DataFrame(dados)
        df.index = df.index + 1
        df.reset_index(inplace=True)
        df.rename(columns={"index": "Colocação"}, inplace=True)

        st.write("---")
        st.table(df)  
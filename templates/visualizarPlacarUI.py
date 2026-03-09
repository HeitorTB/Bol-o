import streamlit as st
import pandas as pd
from views import View

class VisualizarPlacarUI:
    @classmethod
    def main(cls):
        st.header("Ranking Geral 🏆")
        st.write("Acompanhe quem são os melhores palpiteiros do bolão!")

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

        # 3. Exibe a tabela
        df = pd.DataFrame(dados)
        df.index = df.index + 1 # Posição 1, 2, 3...
        
        st.write("---")
        st.table(df) # Usar st.table fica bem elegante para rankings fixa
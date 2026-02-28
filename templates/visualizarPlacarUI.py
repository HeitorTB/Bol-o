import streamlit as st
import pandas as pd
from views import View

class VisualizarPlacarUI:
    @classmethod
    def main(cls):
        st.header("Ranking Geral (Placar) 🏆")
        st.write("Acompanhe quem são os melhores palpiteiros do bolão!")

        # 1. Puxa todos os usuários do banco (já com os pontos calculados)
        usuarios = View.usuario_listar()

        if not usuarios:
            st.info("Nenhum usuário encontrado.")
            return

        # 2. Monta os dados para o Pandas
        dados = []
        for u in usuarios:
            # Se você tiver um admin, podemos escondê-lo do ranking com este if:
            if u.get_nome() != "admin": 
                dados.append({
                    "Jogador": u.get_nome(),
                    "Pontos Totais": u.get_pontos()
                })

        # 3. Transforma na tabela bonitona
        df = pd.DataFrame(dados)
        
        if df.empty:
            st.info("Ainda não há jogadores no ranking.")
            return

        # Ordena do maior para o menor
        df = df.sort_values(by="Pontos Totais", ascending=False).reset_index(drop=True)
        # Ajusta o índice para parecer "Posição" (1, 2, 3...)
        df.index = df.index + 1
        
        st.write("---")
        # Mostra a tabela na tela
        st.dataframe(df, use_container_width=True)
import streamlit as st
import pandas as pd
from views import View

class fazerApostasUI:
    @classmethod
    def main(cls):
        st.header("Faça seus Palpites 🎯")
        st.info("Preencha os placares na tabela abaixo. Clique na célula para digitar!")

        if "usuario_id" not in st.session_state:
            st.error("Você precisa estar logado!")
            return

        usuario_id = st.session_state["usuario_id"]

        # Inicializa flag de salvamento
        if "salvou_apostas" not in st.session_state:
            st.session_state.salvou_apostas = False

        # Se acabou de salvar, limpa a flag e recarrega os dados
        if st.session_state.salvou_apostas:
            st.session_state.salvou_apostas = False
            st.cache_data.clear()
            st.rerun()
            return

        # 1. Puxar todos os jogos e os palpites que o usuário já fez
        todos_jogos = View.jogo_listar()
        meus_palpites = View.palpite_listar_por_usuario(usuario_id)
        
        # Dicionário de palpites já feitos
        dic_palpites = {p.get_jogo_id(): p for p in meus_palpites}

        # 2. Montar os dados para a Tabela
        dados = []
        for jogo in todos_jogos:
            if not jogo.get_finalizado() and jogo.get_id() not in dic_palpites:
                dados.append({
                    "ID": jogo.get_id(),
                    "Casa": jogo.get_time_a(),
                    "Gols Casa": None,
                    "X": "X",
                    "Gols Visit": None,
                    "Visitante": jogo.get_time_b()
                })

        if not dados:
            st.success("Você já palpitou em todos os jogos disponíveis! 🎉 Vá para a aba 'Meus Palpites' para conferir.")
            return

        df = pd.DataFrame(dados)

        # 3. Tabela editável
        df_editado = st.data_editor(
            df,
            hide_index=True,
            use_container_width=True,
            height=600,
            column_config={
                "ID": None,
                "Casa": st.column_config.TextColumn("Mandante", disabled=True),
                "X": st.column_config.TextColumn("", disabled=True),
                "Visitante": st.column_config.TextColumn("Visitante", disabled=True),
                "Gols Casa": st.column_config.NumberColumn(
                    "Gols", min_value=0, max_value=20, step=1, format="%d"
                ),
                "Gols Visit": st.column_config.NumberColumn(
                    "Gols", min_value=0, max_value=20, step=1, format="%d"
                )
            }
        )

        # 4. Botão para Salvar
        if st.button("Salvar Meus Palpites", type="primary", use_container_width=True):
            salvos = 0
            for _, row in df_editado.iterrows():
                if pd.notna(row["Gols Casa"]) and pd.notna(row["Gols Visit"]):
                    jogo_id = int(row["ID"])
                    gols_a = int(row["Gols Casa"])
                    gols_b = int(row["Gols Visit"])
                    View.palpite_inserir(usuario_id, jogo_id, gols_a, gols_b)
                    salvos += 1
            if salvos > 0:
                st.success(f"{salvos} palpite(s) salvos com sucesso!")
                st.session_state.salvou_apostas = True
                st.rerun()
            else:
                st.warning("Nenhum palpite foi salvo. Preencha os dois campos de gols!")
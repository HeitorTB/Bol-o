import streamlit as st
import pandas as pd
from views import View

class fazerApostasUI:
    @classmethod
    def main(cls):
        st.header("Faça seus Palpites 🎉🎉")
        st.caption("Use os botões + e - para ajustar os gols. Tabela otimizada para celular.")

        if "usuario_id" not in st.session_state:
            st.error("Você precisa estar logado!")
            return

        usuario_id = st.session_state["usuario_id"]

        @st.cache_data(ttl=60)
        def carregar_jogos():
            todos_jogos = View.jogo_listar()
            meus_palpites = View.palpite_listar_por_usuario(usuario_id)
            palpites_feitos = {p.get_jogo_id() for p in meus_palpites}
            return [
                {"id": j.get_id(), "mandante": j.get_time_a(), "visitante": j.get_time_b()}
                for j in todos_jogos
                if not j.get_finalizado() and j.get_id() not in palpites_feitos
            ]

        jogos = carregar_jogos()
        if not jogos:
            st.success("🎉 Você já palpitou em todos os jogos!")
            return

        # CSS ultra compacto para forçar linha única no celular
        st.markdown("""
        <style>
        /* Remove espaços extras */
        .stForm div[data-testid="stVerticalBlock"] {
            gap: 0px;
        }
        .stForm hr {
            margin: 2px 0px;
        }
        /* Força as colunas a ficarem em linha sem quebrar */
        div[data-testid="column"] {
            padding: 0px 2px !important;
        }
        /* Tamanho dos inputs */
        .stNumberInput > div > div > input {
            text-align: center;
            padding: 2px 0px !important;
            font-size: 12px;
            height: 32px;
        }
        .stNumberInput > div {
            width: 60px;
            margin: 0 auto;
        }
        /* Botões de incremento/decremento mais compactos */
        .stNumberInput button {
            height: 16px;
            width: 20px;
        }
        /* Texto dos times */
        .team-name {
            font-size: 12px;
            font-weight: bold;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        /* X vermelho */
        .vs-x {
            text-align: center;
            font-size: 14px;
            font-weight: bold;
            color: #FF4B4B;
            margin: 0px;
        }
        /* Ajuste para celular muito pequeno: reduz ainda mais */
        @media (max-width: 480px) {
            .stNumberInput > div {
                width: 50px;
            }
            .team-name {
                font-size: 10px;
            }
        }
        </style>
        """, unsafe_allow_html=True)

        # Inicializar estado temporário
        if "temp_gols" not in st.session_state:
            st.session_state.temp_gols = {j["id"]: (0, 0) for j in jogos}

        # Formulário para evitar rerun a cada clique
        with st.form(key="form_palpites"):
            # Cabeçalho da tabela
            cols = st.columns([2.2, 1, 0.5, 1, 2.2])
            with cols[0]: st.markdown("**Mandante**")
            with cols[1]: st.markdown("**Gols**")
            with cols[2]: st.markdown("**VS**")
            with cols[3]: st.markdown("**Gols**")
            with cols[4]: st.markdown("**Visitante**")
            st.divider()

            for jogo in jogos:
                cols = st.columns([2.2, 1, 0.5, 1, 2.2])
                with cols[0]:
                    st.markdown(f"<div class='team-name'>{jogo['mandante']}</div>", unsafe_allow_html=True)
                
                with cols[1]:
                    gols_casa = st.number_input(
                        "gols_casa",
                        min_value=0, max_value=20, value=st.session_state.temp_gols[jogo["id"]][0],
                        step=1, key=f"casa_{jogo['id']}", label_visibility="collapsed"
                    )
                    st.session_state.temp_gols[jogo["id"]] = (gols_casa, st.session_state.temp_gols[jogo["id"]][1])
                
                with cols[2]:
                    st.markdown("<div class='vs-x'>X</div>", unsafe_allow_html=True)
                
                with cols[3]:
                    gols_visit = st.number_input(
                        "gols_visit",
                        min_value=0, max_value=20, value=st.session_state.temp_gols[jogo["id"]][1],
                        step=1, key=f"visit_{jogo['id']}", label_visibility="collapsed"
                    )
                    st.session_state.temp_gols[jogo["id"]] = (st.session_state.temp_gols[jogo["id"]][0], gols_visit)
                
                with cols[4]:
                    st.markdown(f"<div class='team-name'>{jogo['visitante']}</div>", unsafe_allow_html=True)
                
                # Linha divisória sutil
                st.markdown("<hr style='margin: 4px 0px;'>", unsafe_allow_html=True)

            # Botão salvar
            submitted = st.form_submit_button("✅ Salvar Todos os Palpites", type="primary", use_container_width=True)
            if submitted:
                salvos = 0
                for jogo in jogos:
                    gols_casa, gols_visit = st.session_state.temp_gols[jogo["id"]]
                    try:
                        View.palpite_inserir(usuario_id, jogo["id"], gols_casa, gols_visit)
                        salvos += 1
                    except Exception as e:
                        st.error(f"Erro: {e}")
                if salvos > 0:
                    st.cache_data.clear()
                    st.session_state.temp_gols = {}
                    st.success(f"✅ {salvos} palpite(s) salvos!")
                    st.rerun()
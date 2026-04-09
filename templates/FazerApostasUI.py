import streamlit as st
import pandas as pd
from views import View

class fazerApostasUI:
    @classmethod
    def main(cls):
        st.header("Faça seus Palpites")
        st.caption("Ajuste os gols de cada jogo e clique em salvar.")

        if "usuario_id" not in st.session_state:
            st.error("Você precisa estar logado!")
            return

        usuario_id = st.session_state["usuario_id"]

        # Carrega os dados com cache para não recarregar toda hora
        @st.cache_data(ttl=60)
        def carregar_jogos_disponiveis():
            todos_jogos = View.jogo_listar()
            meus_palpites = View.palpite_listar_por_usuario(usuario_id)
            palpites_feitos = {p.get_jogo_id() for p in meus_palpites}
            
            jogos = []
            for jogo in todos_jogos:
                if not jogo.get_finalizado() and jogo.get_id() not in palpites_feitos:
                    jogos.append({
                        "id": jogo.get_id(),
                        "mandante": jogo.get_time_a(),
                        "visitante": jogo.get_time_b()
                    })
            return jogos

        jogos = carregar_jogos_disponiveis()

        if not jogos:
            st.success("🎉 Você já palpitou em todos os jogos disponíveis!")
            return

        # CSS para deixar a tabela compacta
        st.markdown("""
        <style>
        /* Remove espaços extras entre colunas */
        div[data-testid="column"] {
            padding: 0px 4px !important;
        }
        /* Deixa o number_input menor e centralizado */
        .stNumberInput input {
            text-align: center;
            padding: 4px 0px;
            font-size: 14px;
        }
        .stNumberInput > div {
            width: 70px;
            margin: 0 auto;
        }
        hr {
            margin: 5px 0px;
        }
        </style>
        """, unsafe_allow_html=True)

        # Cabeçalho da tabela
        col1, col2, col3, col4, col5 = st.columns([2, 1, 0.5, 1, 2])
        with col1: st.markdown("**Mandante**")
        with col2: st.markdown("**Gols**")
        with col3: st.markdown("**VS**")
        with col4: st.markdown("**Gols**")
        with col5: st.markdown("**Visitante**")
        st.divider()

        # Cria um formulário para evitar reruns a cada clique
        with st.form(key="palpites_form"):
            palpites = {}  # dicionário para armazenar os valores

            for jogo in jogos:
                cols = st.columns([2, 1, 0.5, 1, 2])
                
                with cols[0]:
                    st.markdown(f"**{jogo['mandante']}**")
                
                with cols[1]:
                    gols_casa = st.number_input(
                        label=f"gols_casa_{jogo['id']}",
                        min_value=0,
                        max_value=20,
                        value=0,
                        step=1,
                        label_visibility="collapsed",
                        key=f"casa_{jogo['id']}"
                    )
                
                with cols[2]:
                    st.markdown("<div style='text-align: center; font-weight: bold; color: #FF4B4B;'>X</div>", 
                                unsafe_allow_html=True)
                
                with cols[3]:
                    gols_visit = st.number_input(
                        label=f"gols_visit_{jogo['id']}",
                        min_value=0,
                        max_value=20,
                        value=0,
                        step=1,
                        label_visibility="collapsed",
                        key=f"visit_{jogo['id']}"
                    )
                
                with cols[4]:
                    st.markdown(f"**{jogo['visitante']}**")
                
                palpites[jogo['id']] = (gols_casa, gols_visit)
                
                # Linha divisória fina entre os jogos
                st.markdown("<hr style='margin: 2px 0px;'>", unsafe_allow_html=True)

            # Botão de salvar
            salvar = st.form_submit_button("✅ Salvar Todos os Palpites", 
                                           type="primary", 
                                           use_container_width=True)

            if salvar:
                salvos = 0
                for jogo_id, (casa, visit) in palpites.items():
                    try:
                        View.palpite_inserir(usuario_id, jogo_id, casa, visit)
                        salvos += 1
                    except Exception as e:
                        st.error(f"Erro no jogo {jogo_id}: {str(e)}")
                
                if salvos > 0:
                    # Limpa o cache e recarrega a página para remover os jogos já palpitaados
                    st.cache_data.clear()
                    st.success(f"✅ {salvos} palpite(s) salvos com sucesso!")
                    st.balloons()
                    st.rerun()
import streamlit as st
import pandas as pd
from views import View

class fazerApostasUI:
    @classmethod
    def main(cls):
        st.header("Faça seus Palpites 🎯")
        st.info("Use os controles + e - para ajustar os gols de cada partida!")
        
        if "usuario_id" not in st.session_state:
            st.error("Você precisa estar logado!")
            return

        usuario_id = st.session_state["usuario_id"]
        
        if "palpites_temp" not in st.session_state:
            st.session_state.palpites_temp = {}

        # Buscar jogos disponíveis
        todos_jogos = View.jogo_listar()
        meus_palpites = View.palpite_listar_por_usuario(usuario_id)
        dic_palpites = {p.get_jogo_id(): p for p in meus_palpites}
        
        jogos_disponiveis = [
            jogo for jogo in todos_jogos 
            if not jogo.get_finalizado() and jogo.get_id() not in dic_palpites
        ]
        
        if not jogos_disponiveis:
            st.success("🎉 Todos os palpites estão em dia!")
            return
        
        # CSS personalizado
        st.markdown("""
        <style>
        div[data-testid="column"] {
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .stButton button {
            padding: 0.25rem 0.5rem;
            margin: 0;
            font-size: 1.2rem;
            font-weight: bold;
        }
        hr {
            margin: 0.5rem 0;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Cabeçalho da tabela
        col1, col2, col3, col4, col5 = st.columns([2, 1.5, 0.5, 1.5, 2])
        with col1:
            st.markdown("**Mandante**")
        with col2:
            st.markdown("**Gols**")
        with col3:
            st.markdown("**VS**")
        with col4:
            st.markdown("**Gols**")
        with col5:
            st.markdown("**Visitante**")
        
        st.divider()
        
        # Lista de jogos
        for jogo in jogos_disponiveis:
            col1, col2, col3, col4, col5 = st.columns([2, 1.5, 0.5, 1.5, 2])
            
            # Time da casa
            with col1:
                st.markdown(f"**{jogo.get_time_a()}**")
            
            # Gols Casa
            with col2:
                key_casa = f"casa_{jogo.get_id()}"
                if key_casa not in st.session_state.palpites_temp:
                    st.session_state.palpites_temp[key_casa] = 0
                
                cols = st.columns([1, 1.5, 1])
                with cols[0]:
                    if st.button("−", key=f"c_{jogo.get_id()}"):
                        if st.session_state.palpites_temp[key_casa] > 0:
                            st.session_state.palpites_temp[key_casa] -= 1
                            st.rerun()
                with cols[1]:
                    st.markdown(f"<div style='text-align: center; font-size: 1.3rem; font-weight: bold;'>{st.session_state.palpites_temp[key_casa]}</div>", 
                               unsafe_allow_html=True)
                with cols[2]:
                    if st.button("+", key=f"c+_{jogo.get_id()}"):
                        if st.session_state.palpites_temp[key_casa] < 20:
                            st.session_state.palpites_temp[key_casa] += 1
                            st.rerun()
            
            # X centralizado
            with col3:
                st.markdown("<div style='text-align: center; font-size: 1.5rem; font-weight: bold; color: #FF4B4B;'>X</div>", 
                           unsafe_allow_html=True)
            
            # Gols Visitante
            with col4:
                key_visit = f"visit_{jogo.get_id()}"
                if key_visit not in st.session_state.palpites_temp:
                    st.session_state.palpites_temp[key_visit] = 0
                
                cols = st.columns([1, 1.5, 1])
                with cols[0]:
                    if st.button("−", key=f"v_{jogo.get_id()}"):
                        if st.session_state.palpites_temp[key_visit] > 0:
                            st.session_state.palpites_temp[key_visit] -= 1
                            st.rerun()
                with cols[1]:
                    st.markdown(f"<div style='text-align: center; font-size: 1.3rem; font-weight: bold;'>{st.session_state.palpites_temp[key_visit]}</div>", 
                               unsafe_allow_html=True)
                with cols[2]:
                    if st.button("+", key=f"v+_{jogo.get_id()}"):
                        if st.session_state.palpites_temp[key_visit] < 20:
                            st.session_state.palpites_temp[key_visit] += 1
                            st.rerun()
            
            # Time visitante
            with col5:
                st.markdown(f"**{jogo.get_time_b()}**")
            
            st.divider()
        
        # Botão centralizado para salvar
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("✅ Salvar Todos os Palpites", type="primary", use_container_width=True):
                salvos = 0
                for jogo in jogos_disponiveis:
                    gols_casa = st.session_state.palpites_temp.get(f"casa_{jogo.get_id()}", 0)
                    gols_visit = st.session_state.palpites_temp.get(f"visit_{jogo.get_id()}", 0)
                    
                    try:
                        View.palpite_inserir(usuario_id, jogo.get_id(), gols_casa, gols_visit)
                        salvos += 1
                    except Exception as e:
                        st.error(f"Erro ao salvar {jogo.get_time_a()} vs {jogo.get_time_b()}: {e}")
                
                if salvos > 0:
                    # Limpar estado
                    for jogo in jogos_disponiveis:
                        st.session_state.palpites_temp.pop(f"casa_{jogo.get_id()}", None)
                        st.session_state.palpites_temp.pop(f"visit_{jogo.get_id()}", None)
                    
                    st.success(f"✅ {salvos} palpite(s) salvos com sucesso!")
                    st.balloons()
                    st.rerun()
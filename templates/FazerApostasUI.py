import streamlit as st
import pandas as pd
from views import View

class fazerApostasUI:
    @classmethod
    def main(cls):
        st.header("Faça seus Palpites 🎉🎉")
        
        if "usuario_id" not in st.session_state:
            st.error("Você precisa estar logado!")
            return

        usuario_id = st.session_state["usuario_id"]
        
        # Carregar dados com cache
        @st.cache_data(ttl=60)
        def carregar_dados():
            todos_jogos = View.jogo_listar()
            meus_palpites = View.palpite_listar_por_usuario(usuario_id)
            dic_palpites = {p.get_jogo_id(): p for p in meus_palpites}
            
            return [
                (jogo.get_id(), jogo.get_time_a(), jogo.get_time_b())
                for jogo in todos_jogos 
                if not jogo.get_finalizado() and jogo.get_id() not in dic_palpites
            ]
        
        jogos = carregar_dados()
        
        if not jogos:
            st.success("🎉 Você já palpitou em todos os jogos!")
            return
        
        # Usar expander para organização
        with st.form("palpites_form"):
            palpites = {}
            
            for jogo_id, mandante, visitante in jogos:
                col1, col2, col3, col4, col5 = st.columns([2, 1.5, 0.5, 1.5, 2])
                
                with col1:
                    st.markdown(f"**{mandante}**")
                
                with col2:
                    gols_casa = st.number_input(
                        "", 
                        min_value=0, 
                        max_value=20, 
                        value=0,
                        key=f"casa_{jogo_id}",
                        label_visibility="collapsed"
                    )
                
                with col3:
                    st.markdown("<h3 style='text-align: center; color: #FF4B4B;'>X</h3>", 
                               unsafe_allow_html=True)
                
                with col4:
                    gols_visit = st.number_input(
                        "",
                        min_value=0,
                        max_value=20,
                        value=0,
                        key=f"visit_{jogo_id}",
                        label_visibility="collapsed"
                    )
                
                with col5:
                    st.markdown(f"**{visitante}**")
                
                palpites[jogo_id] = (gols_casa, gols_visit)
                st.divider()
            
            if st.form_submit_button("Salvar Palpites", type="primary", use_container_width=True):
                salvos = 0
                for jogo_id, (gols_casa, gols_visit) in palpites.items():
                    View.palpite_inserir(usuario_id, jogo_id, gols_casa, gols_visit)
                    salvos += 1
                
                if salvos > 0:
                    st.cache_data.clear()
                    st.success(f"✅ {salvos} palpites salvos!")
                    st.rerun()
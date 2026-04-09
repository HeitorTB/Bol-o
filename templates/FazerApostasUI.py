import streamlit as st
import pandas as pd
from views import View

# --- DICIONÁRIO DE SIGLAS (PADRÃO ISO) PARA AS BANDEIRAS ---
SIGLAS_PAISES = {
    "Canadá": "ca", "Estados Unidos": "us", "México": "mx", "Curaçao": "cw",
    "Haiti": "ht", "Panamá": "pa", "Japão": "jp", "Irã": "ir",
    "Uzbequistão": "uz", "Coreia do Sul": "kr", "Jordânia": "jo", "Austrália": "au",
    "Catar": "qa", "Arábia Saudita": "sa", "Nova Zelândia": "nz", "Argentina": "ar",
    "Brasil": "br", "Equador": "ec", "Uruguai": "uy", "Colômbia": "co",
    "Paraguai": "py", "Marrocos": "ma", "Tunísia": "tn", "Egito": "eg",
    "Argélia": "dz", "Gana": "gh", "Cabo Verde": "cv", "África do Sul": "za",
    "Costa do Marfim": "ci", "Senegal": "sn", "Inglaterra": "gb-eng", "França": "fr",
    "Croácia": "hr", "Portugal": "pt", "Noruega": "no", "Holanda": "nl",
    "Alemanha": "de", "Suíça": "ch", "Áustria": "at", "Bélgica": "be",
    "Espanha": "es", "Escócia": "gb-sct", "Turquia": "tr", "República Tcheca": "cz",
    "Suécia": "se", "Bósnia e Herzegovina": "ba", "RD Congo": "cd", "Iraque": "iq"
}
# -----------------------------------------------------------

class fazerApostasUI:
    @classmethod
    def main(cls):
        st.header("Faça seus Palpites 🎯")
        
        # --- CSS PARA DEIXAR OS CARDS MENOS LARGOS ---
        st.markdown("""
            <style>
            [data-testid="stForm"] {
                max-width: 800px; 
                margin: 0 auto;  
            }    
            @media (max-width: 640px) {   
                max-width: 450px;
                margin: 0 auto;
            }   
            </style>
        """, unsafe_allow_html=True)
        # ---------------------------------------------

        st.info("Ajuste os placares usando os botões nos cards abaixo!")

        if "usuario_id" not in st.session_state:
            st.error("Você precisa estar logado!")
            return

        usuario_id = st.session_state["usuario_id"]

        if "salvou_apostas" not in st.session_state:
            st.session_state.salvou_apostas = False

        if st.session_state.salvou_apostas:
            st.session_state.salvou_apostas = False
            st.cache_data.clear()
            st.rerun()
            return

        todos_jogos = View.jogo_listar()
        meus_palpites = View.palpite_listar_por_usuario(usuario_id)
        
        dic_palpites = {p.get_jogo_id(): p for p in meus_palpites}

        jogos_disponiveis = [
            jogo for jogo in todos_jogos 
            if not jogo.get_finalizado() and jogo.get_id() not in dic_palpites
        ]

        if not jogos_disponiveis:
            st.success("Você já palpitou em todos os jogos disponíveis! 🎉 Vá para a aba 'Meus Palpites' para conferir.")
            return

        with st.form("form_palpites"):
            
            for i in range(0, len(jogos_disponiveis), 2):
                cols = st.columns(2)
                
                with cols[0]:
                    jogo1 = jogos_disponiveis[i]
                    cls.criar_card_jogo(jogo1)
                
                if i + 1 < len(jogos_disponiveis):
                    with cols[1]:
                        jogo2 = jogos_disponiveis[i+1]
                        cls.criar_card_jogo(jogo2)

            submit = st.form_submit_button("Salvar Meus Palpites", type="primary", use_container_width=True)

        if submit:
            salvos = 0
            for jogo in jogos_disponiveis:
                gols_a = st.session_state.get(f"gols_a_{jogo.get_id()}")
                gols_b = st.session_state.get(f"gols_b_{jogo.get_id()}")

                if gols_a is not None and gols_b is not None:
                    View.palpite_inserir(usuario_id, jogo.get_id(), int(gols_a), int(gols_b))
                    salvos += 1
            
            if salvos > 0:
                st.success(f"{salvos} palpite(s) salvos com sucesso!")
                st.session_state.salvou_apostas = True
                st.rerun()

    @classmethod
    def criar_card_jogo(cls, jogo):
        with st.container(border=True):
            st.markdown(f"<h5 style='text-align: center; color: gray;'>Jogo #{int(jogo.get_id())}</h5>", unsafe_allow_html=True)
            
            # --- BUSCA AS SIGLAS PARA AS BANDEIRAS ---
            sigla_a = SIGLAS_PAISES.get(jogo.get_time_a(), "xx")
            sigla_b = SIGLAS_PAISES.get(jogo.get_time_b(), "xx")
            
            # --- MONTA A TAG HTML DAS BANDEIRAS ---
            img_a = f"<img src='https://flagcdn.com/w40/{sigla_a}.png' style='height: 1.2em; vertical-align: middle; border-radius: 2px;'>" if sigla_a != "xx" else ""
            img_b = f"<img src='https://flagcdn.com/w40/{sigla_b}.png' style='height: 1.2em; vertical-align: middle; border-radius: 2px;'>" if sigla_b != "xx" else ""
            
            col_a, col_x, col_b = st.columns([2, 1, 2])
            
            with col_a:
                # O nome do time e a bandeira ficam soltos em cima do campo de número
                st.markdown(f"<div style='margin-bottom: 5px; font-size: 14px;'>{img_a} <b>{jogo.get_time_a()}</b></div>", unsafe_allow_html=True)
                st.number_input(
                    "Gols A", # Esse nome agora é invisível para o usuário
                    min_value=0, max_value=20, step=1, value=0, 
                    key=f"gols_a_{jogo.get_id()}",
                    label_visibility="collapsed" # Mágica para esconder o rótulo
                )
                
            with col_x:
                # Ajustamos o margin-top para 25px para alinhar o X com o campo numérico
                st.markdown("<h4 style='text-align: center; margin-top: 25px;'>X</h4>", unsafe_allow_html=True)
                
            with col_b:
                st.markdown(f"<div style='margin-bottom: 5px; font-size: 14px;'>{img_b} <b>{jogo.get_time_b()}</b></div>", unsafe_allow_html=True)
                st.number_input(
                    "Gols B", 
                    min_value=0, max_value=20, step=1, value=0, 
                    key=f"gols_b_{jogo.get_id()}",
                    label_visibility="collapsed"
                )
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
        
        # --- CSS AJUSTADO PARA O LAYOUT SEM FORM ---
        st.markdown("""
            <style>
            .block-container {
                max-width: 900px;
                margin: 0 auto;
            }
            </style>
        """, unsafe_allow_html=True)
        # ---------------------------------------------

        st.info("Ative o interruptor de um jogo para liberar os botões de + e - e palpitar!")

        if "usuario_id" not in st.session_state:
            st.error("Você precisa estar logado!")
            return

        usuario_id = st.session_state["usuario_id"]

        if "salvou_apostas" not in st.session_state:
            st.session_state.salvou_apostas = False

        if st.session_state.salvou_apostas:
            st.success("Seus palpites foram salvos com sucesso! 🎉")
            st.session_state.salvou_apostas = False

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

        # Renderização dos cards diretamente na tela (sem st.form)
        for i in range(0, len(jogos_disponiveis), 2):
            cols = st.columns(2)
            
            with cols[0]:
                jogo1 = jogos_disponiveis[i]
                cls.criar_card_jogo(jogo1)
            
            if i + 1 < len(jogos_disponiveis):
                with cols[1]:
                    jogo2 = jogos_disponiveis[i+1]
                    cls.criar_card_jogo(jogo2)

        st.markdown("<br>", unsafe_allow_html=True)
        # Botão de salvar comum que processa as informações instantaneamente
        submit = st.button("Salvar Meus Palpites", type="primary", use_container_width=True)

        # Lógica de Salvamento
        if submit:
            palpites_lote = []
            
            for jogo in jogos_disponiveis:
                ativado = st.session_state.get(f"ativar_{jogo.get_id()}")
                
                if ativado:
                    gols_a = st.session_state.get(f"gols_a_{jogo.get_id()}")
                    gols_b = st.session_state.get(f"gols_b_{jogo.get_id()}")

                    palpites_lote.append({
                        "id_usuario": usuario_id,
                        "id_jogo": jogo.get_id(),
                        "gols_a": int(gols_a),
                        "gols_b": int(gols_b)
                    })
            
            if len(palpites_lote) > 0:
                View.palpite_inserir_lote(palpites_lote)
                
                st.session_state.salvou_apostas = True
                st.cache_data.clear() 
                st.rerun()
            else:
                st.warning("Você precisa ativar o interruptor de pelo menos um jogo para salvar seus palpites!")


    @classmethod
    def criar_card_jogo(cls, jogo):
        with st.container(border=True):
            
            col_titulo, col_toggle = st.columns([2, 1])
            with col_titulo:
                st.markdown(f"<h5 style='margin-top: 5px; color: gray;'>Jogo #{int(jogo.get_id())}</h5>", unsafe_allow_html=True)
            with col_toggle:
                # Captura o estado do interruptor na variável 'ativado'
                ativado = st.toggle("Palpitar", key=f"ativar_{jogo.get_id()}")
            
            # --- BUSCA AS SIGLAS PARA AS BANDEIRAS ---
            sigla_a = SIGLAS_PAISES.get(jogo.get_time_a(), "xx")
            sigla_b = SIGLAS_PAISES.get(jogo.get_time_b(), "xx")
            
            # --- MONTA A TAG HTML DAS BANDEIRAS ---
            img_a = f"<img src='https://flagcdn.com/w40/{sigla_a}.png' style='height: 1.2em; vertical-align: middle; border-radius: 2px;'>" if sigla_a != "xx" else ""
            img_b = f"<img src='https://flagcdn.com/w40/{sigla_b}.png' style='height: 1.2em; vertical-align: middle; border-radius: 2px;'>" if sigla_b != "xx" else ""
            
            col_a, col_x, col_b = st.columns([2, 1, 2])
            
            with col_a:
                st.markdown(f"<div style='margin-bottom: 5px; font-size: 14px;'>{img_a} <b>{jogo.get_time_a()}</b></div>", unsafe_allow_html=True)
                # O parâmetro disabled=not ativado faz a mágica acontecer
                st.number_input(
                    "Gols A", 
                    min_value=0, max_value=20, step=1, value=0,
                    key=f"gols_a_{jogo.get_id()}",
                    label_visibility="collapsed",
                    disabled=not ativado
                )
                
            with col_x:
                st.markdown("<h4 style='text-align: center; margin-top: 25px;'>X</h4>", unsafe_allow_html=True)
                
            with col_b:
                st.markdown(f"<div style='margin-bottom: 5px; font-size: 14px;'>{img_b} <b>{jogo.get_time_b()}</b></div>", unsafe_allow_html=True)
                # O parâmetro disabled=not ativado faz a mágica acontecer
                st.number_input(
                    "Gols B", 
                    min_value=0, max_value=20, step=1, value=0,
                    key=f"gols_b_{jogo.get_id()}",
                    label_visibility="collapsed",
                    disabled=not ativado
                )
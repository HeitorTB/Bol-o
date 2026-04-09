import streamlit as st
import pandas as pd
from views import View

class fazerApostasUI:
    @classmethod
    def main(cls):
        st.header("Faça seus Palpites 🎯")
        
        # --- CSS PARA DEIXAR OS CARDS MENOS LARGOS ---
        # Limita a largura do formulário e centraliza na tela
        st.markdown("""
            <style>
            [data-testid="stForm"] {
                max-width: 550px; /* Altere esse número para deixar mais largo ou mais fino */
                margin: 0 auto;   /* Centraliza o bloco na tela */
            }
            </style>
        """, unsafe_allow_html=True)
        # ---------------------------------------------

        st.info("Ajuste os placares usando os botões de + e - nos cards abaixo!")

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

        # 2. Filtrar apenas os jogos disponíveis para palpitar
        jogos_disponiveis = [
            jogo for jogo in todos_jogos 
            if not jogo.get_finalizado() and jogo.get_id() not in dic_palpites
        ]

        if not jogos_disponiveis:
            st.success("Você já palpitou em todos os jogos disponíveis! 🎉 Vá para a aba 'Meus Palpites' para conferir.")
            return

        # 3. Construir a Interface em Formato de Cards
        with st.form("form_palpites"):
            
            # Criando o layout de 2 colunas por linha (No celular, o Streamlit empilha para 1 automaticamente)
            for i in range(0, len(jogos_disponiveis), 2):
                cols = st.columns(2)
                
                with cols[0]:
                    jogo1 = jogos_disponiveis[i]
                    cls.criar_card_jogo(jogo1)
                
                if i + 1 < len(jogos_disponiveis):
                    with cols[1]:
                        jogo2 = jogos_disponiveis[i+1]
                        cls.criar_card_jogo(jogo2)

            # 4. Botão para Salvar
            submit = st.form_submit_button("Salvar Meus Palpites", type="primary", use_container_width=True)

        # 5. Lógica de Salvamento
        if submit:
            salvos = 0
            for jogo in jogos_disponiveis:
                gols_a = st.session_state.get(f"gols_a_{jogo.get_id()}")
                gols_b = st.session_state.get(f"gols_b_{jogo.get_id()}")

                # Como agora value=0, gols_a e gols_b nunca serão None. 
                # Ele vai salvar todos os jogos da tela, mesmo os que ficaram 0x0.
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
            st.markdown(f"<h5 style='text-align: center; color: gray;'>Jogo #{jogo.get_id()}</h5>", unsafe_allow_html=True)
            
            col_a, col_x, col_b = st.columns([2, 1, 2])
            
            with col_a:
                # Mudamos value=None para value=0
                st.number_input(
                    f"{jogo.get_time_a()}", 
                    min_value=0, max_value=20, step=1, value=0, 
                    key=f"gols_a_{jogo.get_id()}"
                )
                
            with col_x:
                st.markdown("<h4 style='text-align: center; margin-top: 35px;'>X</h4>", unsafe_allow_html=True)
                
            with col_b:
                # Mudamos value=None para value=0
                st.number_input(
                    f"{jogo.get_time_b()}", 
                    min_value=0, max_value=20, step=1, value=0, 
                    key=f"gols_b_{jogo.get_id()}"
                )
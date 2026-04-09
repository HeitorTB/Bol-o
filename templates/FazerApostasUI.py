import streamlit as st
import pandas as pd
from views import View

class fazerApostasUI:
    @classmethod
    def main(cls):
        st.header("Faça seus Palpites 🎯")
        
        # --- CSS AGRESSIVO PARA FORÇAR MESMA LINHA NO MOBILE ---
        st.markdown("""
            <style>
            /* Limita a largura geral do formulário no computador */
            [data-testid="stForm"] {
                max-width: 500px; 
                margin: 0 auto;   
            }
            
            /* Força as colunas internas a ficarem lado a lado no celular */
            @media (max-width: 640px) {
                [data-testid="column"] {
                    width: auto !important;
                    flex: 1 1 0% !important;
                    min-width: 0 !important;
                }
                [data-testid="stHorizontalBlock"] {
                    flex-wrap: nowrap !important;
                    flex-direction: row !important;
                    align-items: center !important;
                }
            }
            </style>
        """, unsafe_allow_html=True)
        # --------------------------------------------------------

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
            # Título do jogo centralizado
            st.markdown(f"<p style='text-align: center; color: gray; margin-bottom: 0px;'>Jogo #{jogo.get_id()}</p>", unsafe_allow_html=True)
            
            # Nomes dos times em destaque, na mesma linha (Ex: Flamengo  X  Vasco)
            st.markdown(
                f"<h4 style='text-align: center; margin-top: 5px; margin-bottom: 15px;'>"
                f"{jogo.get_time_a()} <span style='color: gray; font-size: 18px;'>&nbsp; X &nbsp;</span> {jogo.get_time_b()}"
                f"</h4>", 
                unsafe_allow_html=True
            )
            
            # Colunas apenas para os campos numéricos. 
            # Demos mais espaço para os botões e menos espaço para o meio.
            col_a, col_x, col_b = st.columns([3, 1, 3])
            
            with col_a:
                st.number_input(
                    "Gols A", # O nome é obrigatório, mas não vai aparecer na tela
                    min_value=0, max_value=20, step=1, value=0, 
                    key=f"gols_a_{jogo.get_id()}",
                    label_visibility="collapsed" # ISSO É A MÁGICA: Esconde o texto
                )
                
            with col_x:
                # Apenas um pequeno traço ou nada, já que o "X" já está lá em cima
                st.markdown("<p style='text-align: center; margin-top: 10px;'>-</p>", unsafe_allow_html=True)
                
            with col_b:
                st.number_input(
                    "Gols B", 
                    min_value=0, max_value=20, step=1, value=0, 
                    key=f"gols_b_{jogo.get_id()}",
                    label_visibility="collapsed" # Esconde o texto
                )
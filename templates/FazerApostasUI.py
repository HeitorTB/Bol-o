import streamlit as st
from views import View

class fazerApostasUI:
    @classmethod
    def main(cls):
        # --- CSS MÁGICO PARA O CELULAR ---
        # Isso força as colunas do Streamlit a não quebrarem linha na tela pequena
        st.markdown(
            """
            <style>
            div[data-testid="stForm"] div[data-testid="stHorizontalBlock"] {
                flex-wrap: nowrap !important;
                align-items: center !important;
            }
            div[data-testid="stForm"] div[data-testid="column"] {
                min-width: 0 !important;
                padding: 0 3px !important; /* Deixa os itens mais juntinhos */
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        st.header("Faça seus Palpites 🎯")
        st.warning("Se você sair ou atualizar a página sem clicar em salvar meus palpites e cadastrar todos eles, o progresso será perdido!")

        # 1. Verifica quem é o usuário logado
        if "usuario_id" not in st.session_state:
            st.error("Você precisa estar logado para fazer apostas!")
            return

        usuario_id = st.session_state["usuario_id"]

        # 2. Busca todos os jogos e os palpites que o usuário JÁ FEZ
        todos_jogos = View.jogo_listar()
        meus_palpites = View.palpite_listar_por_usuario(usuario_id)
        
        # Cria uma lista apenas com os IDs dos jogos que ele já apostou
        jogos_apostados_ids = [p.get_jogo_id() for p in meus_palpites]

        # O FILTRO MÁGICO: Só pega os jogos abertos e que NÃO estão na lista de apostados
        jogos_abertos = [j for j in todos_jogos if not j.get_finalizado() and j.get_id() not in jogos_apostados_ids]

        # Se a lista ficar vazia, ele esconde o formulário e mostra o aviso:
        if not jogos_abertos:
            st.success("Você já palpitou em todos os jogos disponíveis! Acompanhe na aba 'Minhas Apostas'.")
            return

        # 3. Cria o formulário apenas para os jogos que sobraram
        with st.form("form_apostas"):           
            palpites_digitados = {}
            for jogo in jogos_abertos:
                
                # Ajustei as proporções para [3, 2, 1, 2, 3] para focar mais espaço nos nomes dos times
                col1, col2, col3, col4, col5 = st.columns([3, 2, 1, 2, 3], vertical_alignment="center")
                
                with col1:
                    # Time A alinhado à direita. O font-size: 16px garante que cabe no celular!
                    st.markdown(f"<h5 style='text-align: right; margin: 0; font-size: 16px;'>{jogo.get_time_a()}</h5>", unsafe_allow_html=True)
                
                with col2:
                    # label_visibility="collapsed" some com o título invisível e alinha a caixinha com o texto
                    gols_a = st.number_input("A", min_value=0, step=1, key=f"gols_a_{jogo.get_id()}", label_visibility="collapsed")
                
                with col3:
                    st.markdown("<h5 style='text-align: center; margin: 0; font-size: 16px;'>X</h5>", unsafe_allow_html=True)
                
                with col4:
                    gols_b = st.number_input("B", min_value=0, step=1, key=f"gols_b_{jogo.get_id()}", label_visibility="collapsed")
                
                with col5:
                    # Time B alinhado à esquerda.
                    st.markdown(f"<h5 style='text-align: left; margin: 0; font-size: 16px;'>{jogo.get_time_b()}</h5>", unsafe_allow_html=True)
                
                st.divider()
                palpites_digitados[jogo.get_id()] = {"gols_a": gols_a, "gols_b": gols_b}

            # O botão de salvar (com use_container_width pra ficar esticado bonito)
            submit = st.form_submit_button("Salvar Meus Palpites", use_container_width=True)

            if submit:
                for jogo_id, placar in palpites_digitados.items():
                    View.palpite_inserir(usuario_id, jogo_id, placar["gols_a"], placar["gols_b"])
                
                st.success("Palpite salvo com sucesso!")
                
                # 4. A MÁGICA ACONTECE AQUI: Atualiza a tela para o jogo sumir na hora!
                st.rerun()
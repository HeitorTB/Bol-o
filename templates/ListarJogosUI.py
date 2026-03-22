import streamlit as st
from views import View

class ListarJogosUI:
    @classmethod
    def main(cls):
        st.header("Tabela de Jogos 🗓️")
        st.markdown("Acompanhe aqui todos os jogos do campeonato e os placares reais.")

        # 1. Busca todos os jogos cadastrados
        jogos = View.jogo_listar()

        if not jogos:
            st.warning("Nenhum jogo cadastrado no sistema ainda.")
            return

        # 2. Organiza a lista por data (do mais antigo para o mais novo)
        # Assumindo que o seu get_data_hora() retorna algo que possa ser ordenado (como string YYYY-MM-DD ou datetime)
        jogos_ordenados = sorted(jogos, key=lambda j: j.get_data_hora())

        # 3. Cria abas para organizar a visualização e não ficar uma lista infinita
        aba_todos, aba_abertos, aba_encerrados = st.tabs(["Todos os Jogos", "⏳ Abertos", "✅ Encerrados"])

        # Função interna só para desenhar os cards e não repetirmos código 3 vezes
        def exibir_lista_jogos(lista):
            if not lista:
                st.info("Nenhum jogo encontrado nesta categoria.")
                return

            for jogo in lista:
                with st.container(border=True):
                    # Cabeçalho do Card com a data e status
                    status = "✅ Encerrado" if jogo.get_finalizado() else "⏳ Aberto"
                    st.caption(f"📅 **{jogo.get_data_hora()}** | Status: {status}")
                    
                    # Colunas para o placar (Layout mobile-friendly: 3, 2, 3)
                    col1, col2, col3 = st.columns([3, 2, 3], vertical_alignment="center")
                    
                    # Pegamos os gols reais do jogo. Se for None (ainda não aconteceu), mostramos um tracinho "-"
                    # Obs: Verifique se os nomes dos seus métodos são get_gols_a() e get_gols_b() no seu Model
                    gols_a = jogo.get_gols_a() if jogo.get_gols_a() is not None else "-"
                    gols_b = jogo.get_gols_b() if jogo.get_gols_b() is not None else "-"
                    
                    with col1:
                        st.markdown(f"<h5 style='text-align: right; margin: 0;'>{jogo.get_time_a()}</h5>", unsafe_allow_html=True)
                    
                    with col2:
                        # O placar centralizado e em destaque
                        st.markdown(f"<h4 style='text-align: center; margin: 0; color: #1f77b4;'>{gols_a} x {gols_b}</h4>", unsafe_allow_html=True)
                    
                    with col3:
                        st.markdown(f"<h5 style='text-align: left; margin: 0;'>{jogo.get_time_b()}</h5>", unsafe_allow_html=True)

        # 4. Preenche as abas com as listas filtradas
        with aba_todos:
            exibir_lista_jogos(jogos_ordenados)
            
        with aba_abertos:
            jogos_abertos = [j for j in jogos_ordenados if not j.get_finalizado()]
            exibir_lista_jogos(jogos_abertos)
            
        with aba_encerrados:
            jogos_encerrados = [j for j in jogos_ordenados if j.get_finalizado()]
            exibir_lista_jogos(jogos_encerrados)
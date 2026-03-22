import streamlit as st
from views import View

class MeusPalpitesUI:
    @classmethod
    def main(cls):
        st.header("Meus Palpites 📝")
        st.markdown("Acompanhe aqui as suas apostas e os pontos conquistados.")

        if "usuario_id" not in st.session_state:
            st.error("Você precisa estar logado!")
            return

        usuario_id = st.session_state["usuario_id"]

        # Busca as apostas do usuário e a lista de todos os jogos
        palpites = View.palpite_listar_por_usuario(usuario_id)
        todos_jogos = View.jogo_listar()

        if not palpites:
            st.info("Você ainda não fez nenhum palpite. Vá na aba de apostas!")
            return

        # Cria um "dicionário" de jogos para facilitar a busca do nome dos times pelo ID
        dic_jogos = {j.get_id(): j for j in todos_jogos}

        # Vamos juntar os palpites com os jogos e ordenar pela data para ficar organizado
        palpites_com_jogo = []
        for p in palpites:
            jogo = dic_jogos.get(p.get_jogo_id())
            if jogo:
                palpites_com_jogo.append((p, jogo))
        
        # Ordena os jogos pela data (do mais antigo pro mais novo)
        palpites_com_jogo.sort(key=lambda x: x[1].get_data_hora())

        # Exibe os Cards na tela
        for p, jogo in palpites_com_jogo:
            with st.container(border=True):
                # Status e Pontuação
                if jogo.get_finalizado():
                    status = "✅ Finalizado"
                    pontos = int(p.get_pontos_ganhos())
                    cor_pontos = "#28a745" if pontos > 0 else "#6c757d" # Verde se ganhou algo, cinza se zerou
                    pontos_html = f"<span style='color: {cor_pontos}; font-weight: bold;'>{pontos} pts</span>"
                else:
                    status = "⏳ Aberto"
                    pontos_html = "<span style='color: #ffc107; font-weight: bold;'>- pts</span>"

                # Linha 1 do Card: Data, Status e Pontos
                col_topo1, col_topo2 = st.columns([3, 1], vertical_alignment="center")
                with col_topo1:
                    st.caption(f"📅 **{jogo.get_data_hora()}** | {status}")
                with col_topo2:
                    st.markdown(f"<div style='text-align: right; font-size: 18px;'>{pontos_html}</div>", unsafe_allow_html=True)
                
                # Linha 2 do Card: O Placar Apostado (Layout 3-2-3 igual a tabela de jogos)
                c1, c2, c3 = st.columns([3, 2, 3], vertical_alignment="center")
                with c1:
                    st.markdown(f"<h5 style='text-align: right; margin: 0;'>{jogo.get_time_a()}</h5>", unsafe_allow_html=True)
                with c2:
                    # O palpite do usuário centralizado e em destaque
                    placar_palpite = f"{int(p.get_gols_time_a())} x {int(p.get_gols_time_b())}"
                    st.markdown(f"<h4 style='text-align: center; margin: 0; color: #1f77b4; background-color: #f0f2f6; border-radius: 5px; padding: 5px;'>{placar_palpite}</h4>", unsafe_allow_html=True)
                with c3:
                    st.markdown(f"<h5 style='text-align: left; margin: 0;'>{jogo.get_time_b()}</h5>", unsafe_allow_html=True)
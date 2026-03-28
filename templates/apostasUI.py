import streamlit as st
from views import View

class MeusPalpitesUI:
    @classmethod
    def main(cls):
        st.header("Meus Palpites 📝")

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

        # --- A MÁGICA DOS CARDS COMEÇA AQUI ---
        for p in palpites:
            jogo = dic_jogos.get(p.get_jogo_id())
            
            if jogo:
                status_finalizado = jogo.get_finalizado()
                
                # Cria a caixinha em volta do palpite
                with st.container(border=True):
                    
                    # 1. Cabeçalho do Card (Status)
                    if status_finalizado:
                        st.caption("🔴 Jogo Finalizado")
                    else:
                        st.caption("🟢 Jogo em Aberto")
                    
                    # 2. Corpo do Card (Times e O SEU PALPITE)
                    col1, col2, col3 = st.columns([3, 2, 3])
                    
                    with col1:
                        # Time da Casa alinhado à direita
                        st.markdown(f"<div style='text-align: right; font-size: 15px;'><b>{jogo.get_time_a()}</b></div>", unsafe_allow_html=True)
                    
                    with col2:
                        # O Seu Palpite centralizado com um fundo cinza clarinho
                        st.markdown(f"<div style='text-align: center; font-size: 16px; background-color: #f0f2f6; border-radius: 5px; color: black; padding: 2px;'>{int(p.get_gols_time_a())} x {int(p.get_gols_time_b())}</div>", unsafe_allow_html=True)
                    
                    with col3:
                        # Time Visitante alinhado à esquerda
                        st.markdown(f"<div style='text-align: left; font-size: 15px;'><b>{jogo.get_time_b()}</b></div>", unsafe_allow_html=True)
                    
                    st.markdown("---") # Linha divisória fina
                    
                    # 3. Rodapé do Card (Placar Real e Pontuação)
                    if status_finalizado:
                        st.markdown(f"""
                        <div style='text-align: center; font-size: 14px;'>
                            Placar Oficial: <b>{int(jogo.get_gols_time_a())} x {int(jogo.get_gols_time_b())}</b><br>
                            <span style='color: #28a745; font-size: 16px;'><b>🎯 Pontos: {p.get_pontos_ganhos()}</b></span>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown("<div style='text-align: center; font-size: 13px; color: gray;'>⏳ Aguardando resultado da partida...</div>", unsafe_allow_html=True)
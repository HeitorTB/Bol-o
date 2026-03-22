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

        palpites = View.palpite_listar_por_usuario(usuario_id)
        todos_jogos = View.jogo_listar()

        if not palpites:
            st.info("Você ainda não fez nenhum palpite. Vá na aba de apostas!")
            return

        dic_jogos = {j.get_id(): j for j in todos_jogos}

        palpites_com_jogo = []
        for p in palpites:
            jogo = dic_jogos.get(p.get_jogo_id())
            if jogo:
                palpites_com_jogo.append((p, jogo))
        
        palpites_com_jogo.sort(key=lambda x: x[1].get_data_hora())

        # Exibe os Cards na tela usando HTML/Flexbox para NUNCA quebrar a linha
        for p, jogo in palpites_com_jogo:
            with st.container(border=True):
                
                # Regras visuais de Status e Pontos (Estilo "Badge/Etiqueta")
                if jogo.get_finalizado():
                    status = "✅ Encerrado"
                    pontos = int(p.get_pontos_ganhos())
                    cor_fundo = "#28a745" if pontos > 0 else "#6c757d" # Fundo verde se ganhou, cinza se zerou
                    pontos_html = f"<span style='color: white; background-color: {cor_fundo}; padding: 2px 8px; border-radius: 10px; font-size: 12px; font-weight: bold;'>{pontos} pts</span>"
                else:
                    status = "⏳ Aberto"
                    pontos_html = f"<span style='color: #856404; background-color: #fff3cd; padding: 2px 8px; border-radius: 10px; font-size: 12px; font-weight: bold;'>Aguardando</span>"

                # Desenhando o Card inteiro em HTML para controle total no celular
                card_html = f"""
                <div style="display: flex; flex-direction: column; gap: 10px;">
                    
                    <div style="display: flex; justify-content: space-between; align-items: center; font-size: 13px; color: #666; border-bottom: 1px solid #eee; padding-bottom: 5px;">
                        <span>📅 {jogo.get_data_hora()} • {status}</span>
                        <span>{pontos_html}</span>
                    </div>
                    
                    <div style="display: flex; justify-content: center; align-items: center; width: 100%; padding-top: 5px;">
                        
                        <div style="flex: 1; text-align: right; font-size: 15px; font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
                            {jogo.get_time_a()}
                        </div>
                        
                        <div style="margin: 0 15px; background-color: #f0f2f6; color: #1f77b4; padding: 5px 15px; border-radius: 8px; font-size: 16px; font-weight: bold; white-space: nowrap;">
                            {int(p.get_gols_time_a())} x {int(p.get_gols_time_b())}
                        </div>
                        
                        <div style="flex: 1; text-align: left; font-size: 15px; font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
                            {jogo.get_time_b()}
                        </div>
                        
                    </div>
                </div>
                """
                
                # Injeta o HTML no Streamlit
                st.markdown(card_html, unsafe_allow_html=True)
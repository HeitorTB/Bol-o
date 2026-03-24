import streamlit as st
from templates.loginUI import LoginUI
from templates.abrirContaUI import AbrirContaUI
from templates.CadastrarJogosUI import cadastrarJogoUI
from templates.atualizarPlacarUI import AtualizarPlacarUI
from templates.apostasUI import MeusPalpitesUI
from templates.FazerApostasUI import fazerApostasUI
from templates.visualizarPlacarUI import VisualizarPlacarUI
from streamlit_option_menu import option_menu
from templates.RegrasUI import regrasUI
from views import View

class IndexUI: 
    
    @staticmethod
    def menu_visitante():
        # Menu superior horizontal
        op = option_menu(
            menu_title=None,
            options=["Entrar", "Abrir Conta"],
            icons=["box-arrow-in-right", "person-plus"], # Ícones do Bootstrap
            orientation="horizontal"
        )
        if op == "Entrar": LoginUI.main()
        if op == "Abrir Conta": AbrirContaUI.main()
    
    @staticmethod
    def menu_usuario():
        op = option_menu(
            menu_title=None,
            options=["Apostar", "Apostas", "Ranking","Regras"],
            icons=["trophy", "card-checklist", "info-circle", "list-check"],
            orientation="horizontal",
            styles={
                "nav": {"flex-wrap": "nowrap"}, 
                "nav-link": {
                    "font-size": "15px", 
                    "text-align": "center", 
                    "margin": "0px", 
                    "padding": "10px 5px" 
                }
            }
        )
        if op == "Apostar": fazerApostasUI.main()
        if op == "Apostas": MeusPalpitesUI.main()
        if op == "Ranking": VisualizarPlacarUI.main()
        if op == "Regras": regrasUI.main()

    @staticmethod
    def menu_admin():
        op = option_menu(
            menu_title=None,
            options=["Cadastrar", "Atualizar"],
            icons=["plus-circle", "arrow-clockwise"],
            orientation="horizontal"
        )
        if op == "Cadastrar": cadastrarJogoUI.main() 
        if op == "Atualizar": AtualizarPlacarUI.main() 
    
    @staticmethod
    def sidebar():
        if "usuario_id" not in st.session_state:
            IndexUI.menu_visitante()
        else:
            st.write(f"Bem-vindo(a), **{st.session_state['usuario_nome']}** ⚽")
            
            # Se for o ADMIN, libera o menu de administrador direto
            if st.session_state["usuario_nome"] == "admin":
                IndexUI.menu_admin()
            else:
                # --- CATRACA VIRTUAL BLINDADA ---
                # Pegamos o status. Se vier Vazio (None), transformamos numa string vazia ""
                status_atual = st.session_state.get("status", "")
                
                # A LÓGICA INVERTIDA: Só entra se for "Aprovado" (ignorando maiúsculas/minúsculas)
                if str(status_atual).strip().lower() == "aprovado":
                    IndexUI.menu_usuario()
                    
                # Se for Pendente, Vazio, ou qualquer outra coisa, TRAVA NA TELA DE PAGAMENTO!
                else:
                    st.error("⚠️ Sua conta está aguardando aprovação!")
                    with st.container(border=True):
                        st.markdown("""
                        ### Quase lá! 🚀
                        Para liberar o seu acesso às áreas de **Palpites** e **Ranking**, você precisa realizar o pagamento da taxa de inscrição do bolão.
                        
                        * **Valor:** R$ 25,00  
                        * **Chave PIX:** `seu-email-ou-telefone@pix.com.br`
                        
                        Após realizar o pagamento, envie o comprovante no WhatsApp do Administrador: **(11) 99999-9999**.
                        """)
                    
                    if st.button("Já paguei e fui aprovado! Atualizar acesso", type="primary", use_container_width=True):
                        st.session_state.clear() 
                        st.rerun()

if __name__ == "__main__":
    IndexUI.sidebar()
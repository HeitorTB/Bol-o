import streamlit as st
from views import View

class AtualizarPlacarUI:
    @classmethod
    def main(cls):
        st.header("Atualizar Placar dos Jogos 🏟️")
        
        # 1. Puxa todos os jogos do banco
        jogos = View.jogo_listar()
        
        if not jogos:
            st.info("Nenhum jogo cadastrado ainda.")
            return

        # 2. Cria uma lista bonita para o Admin escolher qual jogo quer atualizar
        # Exemplo: "Brasil x Argentina (2026-06-15 16:00)"
        opcoes_jogos = {f"{j.get_time_a()} x {j.get_time_b()} ({j.get_data_hora()})": j for j in jogos}
        
        escolha = st.selectbox("Selecione o jogo que deseja atualizar:", list(opcoes_jogos.keys()))
        jogo_selecionado = opcoes_jogos[escolha]

        st.write("---")

        # --- TRATAMENTO DE SEGURANÇA PARA OS DADOS DO GOOGLE SHEETS ---
        # Tenta transformar o valor de gols em um número Inteiro puro (int). 
        # Se vier nulo (None) ou vazio da planilha, ele vira 0.
        try:
            val_gols_a = int(float(jogo_selecionado.get_gols_time_a() or 0))
        except (ValueError, TypeError):
            val_gols_a = 0
            
        try:
            val_gols_b = int(float(jogo_selecionado.get_gols_time_b() or 0))
        except (ValueError, TypeError):
            val_gols_b = 0
            
        # Garante que a marcação de 'finalizado' seja um verdadeiro Booleano (True/False)
        status_fin = jogo_selecionado.get_finalizado()
        val_finalizado = str(status_fin).lower() in ['true', '1', 't', 'sim'] if status_fin else False
        # --------------------------------------------------------------

        # 3. Formulário para digitar o placar
        with st.form("form_placar"):
            col1, col2, col3 = st.columns([2, 1, 2])
            
            with col1:
                st.markdown(f"<h4 style='text-align: right;'>{jogo_selecionado.get_time_a()}</h4>", unsafe_allow_html=True)
                # Agora usamos a variável tratada val_gols_a
                gols_a = st.number_input("Gols", min_value=0, value=val_gols_a, key="gols_a")
                
            with col2:
                st.markdown("<h4 style='text-align: center;'>X</h4>", unsafe_allow_html=True)
                
            with col3:
                st.markdown(f"<h4 style='text-align: left;'>{jogo_selecionado.get_time_b()}</h4>", unsafe_allow_html=True)
                # Agora usamos a variável tratada val_gols_b
                gols_b = st.number_input("Gols", min_value=0, value=val_gols_b, key="gols_b")

            st.write("---")
            
            # Caixa de seleção para dizer se o jogo acabou de verdade
            finalizado = st.checkbox("Jogo Finalizado? (Marque apenas quando a partida acabar)", value=val_finalizado)

            submit = st.form_submit_button("Salvar Resultado Oficial")

            if submit:
                # 4. Manda salvar o jogo no banco de dados
                View.jogo_atualizar(
                    jogo_selecionado.get_id(),
                    jogo_selecionado.get_time_a(),
                    jogo_selecionado.get_time_b(),
                    jogo_selecionado.get_data_hora(),
                    gols_a,
                    gols_b,
                    finalizado
                )
                
                if finalizado:
                    View.processar_pontuacao_jogo(jogo_selecionado.get_id(), gols_a, gols_b)
                
                st.success("Placar oficial atualizado com sucesso e pontos distribuídos!")
                st.rerun() # Atualiza a tela para mostrar os dados novos
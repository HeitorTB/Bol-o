import streamlit as st

class regrasUI:
    @classmethod
    def main(cls):
        st.title("Regras do Bolão")
        st.write("Confira abaixo todas as regras de pontuação, premiação e participação.")

        # --- SEÇÃO 1: PONTUAÇÃO ---
        st.header("🎯 Regras de Pontuação")
        
        st.markdown("""
        | Regra | Descrição | Pontuação |
        | :---: | :--- | :---: |
        | **1** | Acertou o placar cheio. | **12** |
        | **2** | Acertou o ganhador e perdedor acertando o número de gols da seleção ganhadora. | **5** |
        | **3** | Acertou o ganhador e perdedor acertando o número de gols da seleção perdedora. | **4** |
        | **4** | Acertou o ganhador e o perdedor ou empate, sem acertar o número de gols. | **3** |
        | **5** | Acertou apenas a somatória de gols da partida. | **2** |
        | **6** | Acertou os gols de alguma das duas seleções, sem acertar o ganhador e perdedor. | **1** |
        """)
        
        st.info("⚠️ **ATENÇÃO:** As pontuações **não são cumulativas**. Caso seu acerto se enquadre em mais de uma regra, será considerada a que tiver a maior pontuação.")

        st.divider() # Linha de separação

        # --- SEÇÃO 2: PREMIAÇÃO ---
        st.header("🏆 Regras de Premiação")
        st.markdown("""
        1. Serão premiados o **Primeiro**, **Segundo** e **Terceiro** lugar.
        2. O valor arrecadado será dividido assim: **Primeiro Lugar 60%**; **Segundo Lugar 25%** e **Terceiro Lugar 10%**.
        3. **5%** do valor arrecadado é destinado para taxa de administração.
        4. O pagamento da premiação será realizado após o término da primeira fase de jogos (primeiras 48 partidas).
        5. **CRITÉRIO DE DESEMPATE:** Em caso de empate no total dos pontos, o critério de desempate será definido pelo número de vezes de acerto do placar cheio (Regra 1 de Pontuação). Persistindo o empate, o número de acertos da regra seguinte (Regra 2) será utilizado como critério, e assim sucessivamente até a Regra 6. Caso o empate persista de todas as formas, o prêmio será dividido.
        """)

        st.divider()

        # --- SEÇÃO 3: PARTICIPAÇÃO ---
        st.header("🤝 Sobre a Participação")
        st.markdown("""
        1. O valor para a participação é **R$ 25,00**.
        2. O valor deve ser pago até o dia **20/11/2022** *(⚠️ Lembrete: ajuste essa data no código!)*, antes do primeiro jogo.
        3. Os palpites são recolhidos online através de um formulário. Em até 48h você receberá o link para acompanhar as pontuações e uma cópia da sua tabela de palpites caso queira imprimir.
        4. O formulário de palpites estará disponível até o dia **20/11/2022**, antes do primeiro jogo.
        5. Os palpites de todos os jogos de todos os participantes terão visualização liberada **após o término do período de recebimento** dos formulários.
        """)
from dao_sql.DAO import DAO
import pandas as pd
class Palpite:
    # Adicionamos o pontos_ganhos, que começa valendo 0
    def __init__(self, id, usuario_id, jogo_id, gols_time_a, gols_time_b, pontos_ganhos=0):
        self.__id = id
        self.__usuario_id = usuario_id
        self.__jogo_id = jogo_id
        self.__gols_time_a = gols_time_a
        self.__gols_time_b = gols_time_b
        self.__pontos_ganhos = pontos_ganhos

    def get_id(self): return self.__id
    def get_usuario_id(self): return self.__usuario_id
    def get_jogo_id(self): return self.__jogo_id
    def get_gols_time_a(self): return self.__gols_time_a
    def get_gols_time_b(self): return self.__gols_time_b
    def get_pontos_ganhos(self): return self.__pontos_ganhos
    def set_pontos_ganhos(self, pontos): self.__pontos_ganhos = pontos

class PalpiteDAO(DAO):
    @classmethod
    def inserir(cls, obj):
        df = cls.listar_aba("palpites")
        novo_id = int(df["id"].max() + 1) if not df.empty else 1
        
        nova_linha = {
            "id": novo_id,
            "usuario_id": obj.get_usuario_id(),
            "jogo_id": obj.get_jogo_id(),
            "gols_time_a": obj.get_gols_time_a(),
            "gols_time_b": obj.get_gols_time_b()
        }
        
        df_nova = pd.DataFrame([nova_linha])
        df = pd.concat([df, df_nova], ignore_index=True)
        
        # --- O TRUQUE DO CABEÇALHO NA TABELA PALPITES ---
        # Essa é a fórmula gigante que calcula as regras do bolão olhando pra aba "jogos"
        formula = '={"pontos_ganhos"; MAP(C2:C; D2:D; E2:E; LAMBDA(id_jogo; pa; pb; SE(id_jogo=""; ""; SEERRO(LET(ra; PROCV(id_jogo; jogos!A:G; 5; FALSO); rb; PROCV(id_jogo; jogos!A:G; 6; FALSO); final; PROCV(id_jogo; jogos!A:G; 7; FALSO); SE(OU(final=VERDADEIRO; final="TRUE"; final=1; final="1"); SES(E(pa=ra; pb=rb); 12; E(SINAL(pa-pb)=SINAL(ra-rb); ra<>rb; OU(E(ra>rb; pa=ra); E(rb>ra; pb=rb))); 5; E(SINAL(pa-pb)=SINAL(ra-rb); ra<>rb; OU(E(ra>rb; pb=rb); E(rb>ra; pa=ra))); 4; SINAL(pa-pb)=SINAL(ra-rb); 3; (pa+pb)=(ra+rb); 2; OU(pa=ra; pb=rb); 1; VERDADEIRO; 0); 0)); 0))))}'
        
        # Renomeia a coluna para transformar ela na própria fórmula
        if 'pontos_ganhos' in df.columns:
            df = df.rename(columns={'pontos_ganhos': formula})
            
        # Limpa todas as linhas dessa coluna para a ARRAYFORMULA poder expandir e funcionar!
        df[formula] = None
        
        cls.salvar_aba("palpites", df)

    @classmethod
    def atualizar_pontos(cls, id_palpite, pontos):
        # 1. Busca a tabela atual de palpites
        df = cls.listar_aba("palpites")
        
        # 2. Localiza a linha correta pelo ID e atualiza a coluna de pontos
        # Garantimos que os IDs sejam comparados como inteiros
        df.loc[df['id'].astype(int) == int(id_palpite), 'pontos_ganhos'] = pontos
        
        # 3. Salva de volta na planilha
        cls.salvar_aba("palpites", df)

    @classmethod
    def listar_por_usuario(cls, id_usuario):
        df = cls.listar_aba("palpites")
        # Filtra as linhas onde usuario_id é igual ao id_usuario
        filtro = df[df['usuario_id'] == id_usuario]
        return [Palpite(r['id'], r['usuario_id'], r['jogo_id'], 
                        r['gols_time_a'], r['gols_time_b'], r['pontos_ganhos']) 
                for _, r in filtro.iterrows()]

    @classmethod
    def listar_por_jogo(cls, id_jogo):
        df = cls.listar_aba("palpites")
        filtro = df[df['jogo_id'] == id_jogo]
        return [Palpite(r['id'], r['usuario_id'], r['jogo_id'], 
                        r['gols_time_a'], r['gols_time_b'], r['pontos_ganhos']) 
                for _, r in filtro.iterrows()]
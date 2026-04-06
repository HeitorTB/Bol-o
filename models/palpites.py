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
        
        # --- A SUPER FÓRMULA ---
        formula = '={"pontos_ganhos"; MAP(C2:C; D2:D; E2:E; LAMBDA(id_jogo; pa; pb; SE(id_jogo=""; ""; SEERRO(LET(id_num; id_jogo*1; pa_n; pa*1; pb_n; pb*1; ra; PROCV(id_num; jogos!A:G; 5; FALSO)*1; rb; PROCV(id_num; jogos!A:G; 6; FALSO)*1; final; PROCV(id_num; jogos!A:G; 7; FALSO); SE(OU(final=VERDADEIRO; final="TRUE"; final=1; final="1"); SES(E(pa_n=ra; pb_n=rb); 12; E(SINAL(pa_n-pb_n)=SINAL(ra-rb); ra<>rb; OU(E(ra>rb; pa_n=ra); E(rb>ra; pb_n=rb))); 5; E(SINAL(pa_n-pb_n)=SINAL(ra-rb); ra<>rb; OU(E(ra>rb; pb_n=rb); E(rb>ra; pa_n=ra))); 4; SINAL(pa_n-pb_n)=SINAL(ra-rb); 3; (pa_n+pb_n)=(ra+rb); 2; OU(pa_n=ra; pb_n=rb); 1; VERDADEIRO; 0); 0)); 0))))}'
        
        # Truque: Mantém apenas as 5 colunas base. Isso descarta qualquer coluna de pontos bugada ou vazia.
        colunas_base = ["id", "usuario_id", "jogo_id", "gols_time_a", "gols_time_b"]
        df = df[[c for c in colunas_base if c in df.columns]]
        
        # Cria a nova coluna com o nome da fórmula e preenche todas as linhas de baixo com Vazio ("")
        # Isso garante o caminho livre para a ARRAYFORMULA expandir sem dar o erro #REF!
        df[formula] = ""
        
        cls.salvar_aba("palpites", df)

    @classmethod
    def atualizar_pontos(cls, id_palpite, pontos):
        # 🚨 FUNÇÃO DESATIVADA 🚨
        # A planilha agora faz o cálculo sozinha! Se deixarmos o Python gravar 
        # os pontos aqui, ele sobrescreve e destrói a fórmula gerando erros.
        pass

    @classmethod
    def listar_por_usuario(cls, id_usuario):
        df = cls.listar_aba("palpites")
        filtro = df[df['usuario_id'] == id_usuario]
        
        # O 'if' na última linha protege o código contra o KeyError caso o cache demore a carregar
        return [Palpite(r['id'], r['usuario_id'], r['jogo_id'], 
                        r['gols_time_a'], r['gols_time_b'], 
                        r['pontos_ganhos'] if 'pontos_ganhos' in r.index else 0) 
                for _, r in filtro.iterrows()]

    @classmethod
    def listar_por_jogo(cls, id_jogo):
        df = cls.listar_aba("palpites")
        filtro = df[df['jogo_id'] == id_jogo]
        
        # Mesmo esquema de proteção contra o KeyError
        return [Palpite(r['id'], r['usuario_id'], r['jogo_id'], 
                        r['gols_time_a'], r['gols_time_b'], 
                        r['pontos_ganhos'] if 'pontos_ganhos' in r.index else 0) 
                for _, r in filtro.iterrows()]
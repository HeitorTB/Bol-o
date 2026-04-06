from dao_sql.DAO import DAO
import pandas as pd

class Palpite:
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

        # Mantém APENAS as colunas base (sem fórmulas)
        colunas_base = ["id", "usuario_id", "jogo_id", "gols_time_a", "gols_time_b"]
        # Se a coluna "pontos_ganhos" já existir, não a removemos (para preservar dados antigos)
        # Mas não criamos fórmula nova. O Apps Script cuidará disso.
        for col in df.columns:
            if col not in colunas_base and col != "pontos_ganhos":
                df = df.drop(columns=[col])

        cls.salvar_aba("palpites", df)

    # Método opcional: se precisar forçar o cálculo via Python (caso o Apps Script falhe)
    @classmethod
    def atualizar_pontos(cls, id_palpite, pontos):
        df = cls.listar_aba("palpites")
        df.loc[df['id'] == id_palpite, 'pontos_ganhos'] = pontos
        cls.salvar_aba("palpites", df)

    @classmethod
    def listar_por_usuario(cls, id_usuario):
        df = cls.listar_aba("palpites")
        filtro = df[df['usuario_id'] == id_usuario]

        # Garante que a coluna "pontos_ganhos" existe (se não, cria com 0)
        if 'pontos_ganhos' not in df.columns:
            df['pontos_ganhos'] = 0

        return [Palpite(r['id'], r['usuario_id'], r['jogo_id'],
                        r['gols_time_a'], r['gols_time_b'],
                        r['pontos_ganhos'] if pd.notna(r['pontos_ganhos']) else 0)
                for _, r in filtro.iterrows()]

    @classmethod
    def listar_por_jogo(cls, id_jogo):
        df = cls.listar_aba("palpites")
        filtro = df[df['jogo_id'] == id_jogo]

        if 'pontos_ganhos' not in df.columns:
            df['pontos_ganhos'] = 0

        return [Palpite(r['id'], r['usuario_id'], r['jogo_id'],
                        r['gols_time_a'], r['gols_time_b'],
                        r['pontos_ganhos'] if pd.notna(r['pontos_ganhos']) else 0)
                for _, r in filtro.iterrows()]
from dao_sql.DAO import DAO

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

class PalpiteDAO(DAO):
    @classmethod
    def inserir(cls, obj):
        # Nomes exatos: usuario_id, jogo_id e pontos_ganhos
        sql = """
            INSERT INTO palpites (usuario_id, jogo_id, gols_time_a, gols_time_b, pontos_ganhos)
            VALUES (?, ?, ?, ?, ?)
        """
        cls.execute(sql, (
            obj.get_usuario_id(), 
            obj.get_jogo_id(), 
            obj.get_gols_time_a(), 
            obj.get_gols_time_b(),
            obj.get_pontos_ganhos()
        ))
    
    @classmethod
    def listar_por_usuario(cls, id_usuario):
        sql = "SELECT id, usuario_id, jogo_id, gols_time_a, gols_time_b, pontos_ganhos FROM palpites WHERE usuario_id = ?"
        resultado = cls.execute(sql, (id_usuario,))
        # Transforma as linhas do banco de dados em objetos Palpite usando .rows
        return [Palpite(*row) for row in resultado.rows]
    
    @classmethod
    def listar_por_jogo(cls, id_jogo):
        sql = "SELECT id, usuario_id, jogo_id, gols_time_a, gols_time_b, pontos_ganhos FROM palpites WHERE jogo_id = ?"
        resultado = cls.execute(sql, (id_jogo,))
        return [Palpite(*row) for row in resultado.rows]

    @classmethod
    def atualizar_pontos(cls, id_palpite, pontos):
        sql = "UPDATE palpites SET pontos_ganhos = ? WHERE id = ?"
        cls.execute(sql, (pontos, id_palpite))
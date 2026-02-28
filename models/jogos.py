class Jogo:
    # Quando cadastramos um jogo, ele começa com 0 gols e finalizado=False
    def __init__(self, id, time_a, time_b, data_hora, gols_time_a=0, gols_time_b=0, finalizado=False):
        self.__id = id
        self.__time_a = time_a
        self.__time_b = time_b
        self.__data_hora = data_hora
        self.__gols_time_a = gols_time_a
        self.__gols_time_b = gols_time_b
        self.__finalizado = finalizado

    # Getters
    def get_id(self): return self.__id
    def get_time_a(self): return self.__time_a
    def get_time_b(self): return self.__time_b
    def get_data_hora(self): return self.__data_hora
    def get_gols_time_a(self): return self.__gols_time_a
    def get_gols_time_b(self): return self.__gols_time_b
    def get_finalizado(self): return self.__finalizado

from dao_sql.DAO import DAO
class JogoDAO(DAO):
    @classmethod
    def inserir(cls, obj):
        cls.abrir()
        sql = """
            INSERT INTO jogos (time_a, time_b, data_hora, gols_time_a, gols_time_b, finalizado)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        cls.execute(sql, (
            obj.get_time_a(), 
            obj.get_time_b(), 
            obj.get_data_hora(), 
            obj.get_gols_time_a(), 
            obj.get_gols_time_b(), 
            obj.get_finalizado()
        ))
        cls.fechar()

    @classmethod
    def listar(cls):
        cls.abrir()
        sql = "SELECT id, time_a, time_b, data_hora, gols_time_a, gols_time_b, finalizado FROM jogos"
        cursor = cls.execute(sql)
        rows = cursor.fetchall()
        # Cria a lista de objetos Jogo a partir do banco
        objs = [Jogo(*row) for row in rows]
        cls.fechar()
        return objs
    
    @classmethod
    def atualizar(cls, obj):
        cls.abrir()
        sql = """
            UPDATE jogos 
            SET time_a = ?, time_b = ?, data_hora = ?, 
                gols_time_a = ?, gols_time_b = ?, finalizado = ? 
            WHERE id = ?
        """
        cls.execute(sql, (
            obj.get_time_a(), 
            obj.get_time_b(), 
            obj.get_data_hora(), 
            obj.get_gols_time_a(), 
            obj.get_gols_time_b(), 
            obj.get_finalizado(), 
            obj.get_id() # O ID diz EXATAMENTE qual jogo estamos mudando
        ))
        cls.fechar()
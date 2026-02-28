class Usuario:
    def __init__(self, id, nome, email, senha, pontos):
        self.set_id(id)
        self.set_nome(nome)
        self.set_email(email)
        self.set_senha(senha)
        self.set_pontos(pontos)

    def set_id(self, valor):
        self.__id = valor
    def set_nome(self, valor):
        if not valor.strip():
            raise ValueError("Nome não pode ser vazio")
        self.__nome = valor
    def set_email(self, valor):
        if not valor.strip():
            raise ValueError("Email não pode ser vazio")
        self.__email = valor
    def set_senha(self, valor):
        if not valor.strip():
            raise ValueError("Senha não pode ser vazia")
        self.__senha = valor
    def set_pontos(self, valor):
        self.__pontos = valor
    def get_id(self): return self.__id
    def get_nome(self): return self.__nome 
    def get_senha(self): return self.__senha
    def get_email(self): return self.__email
    def get_pontos(self): return self.__pontos

from dao_sql.DAO import DAO
class usuarioDAO(DAO):
    @classmethod
    def inserir(cls, obj):
        cls.abrir()
        sql = """
            INSERT INTO usuario (nome, email, senha, pontos)
            VALUES (?, ?, ?, ?)
        """
        cls.execute(sql, (obj.get_nome(), obj.get_email(), obj.get_senha(), obj.get_pontos()))
        cls.fechar()

    @classmethod
    def listar(cls):
        cls.abrir()
        sql = "SELECT * FROM usuario"
        cursor = cls.execute(sql)
        rows = cursor.fetchall()
        objs = [usuario(id, nome, email, senha, pontos) for (id, nome, email, senha, pontos) in rows]
        cls.fechar()
        return objs
    
    @classmethod
    def listar_id(cls, id):
        cls.abrir()
        sql = "SELECT * FROM usuario WHERE id = ?"
        cursor = cls.execute(sql, (id,))
        row = cursor.fetchone()
        obj = usuario(*row) if row else None
        cls.fechar()
        return obj
    
    @classmethod
    def atualizar(cls, obj):
        cls.abrir()
        sql = """
            UPDATE usuario SET nome=?, email=?, senha=?, pontos=?
            WHERE id=?
        """
        cls.execute(sql, (obj.get_nome(), obj.get_email(), obj.get_senha(), obj.get_pontos(), obj.get_id()))
        cls.fechar()

    @classmethod
    def excluir(cls, obj):
        cls.abrir()
        sql = "DELETE FROM usuario WHERE id=?"
        cls.execute(sql, (obj.get_id(),))
        cls.fechar()

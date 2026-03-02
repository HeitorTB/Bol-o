from dao_sql.DAO import DAO

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

class usuarioDAO(DAO):
    @classmethod
    def inserir(cls, obj):
        sql = """
            INSERT INTO usuario (nome, email, senha, pontos)
            VALUES (?, ?, ?, ?)
        """
        cls.execute(sql, (obj.get_nome(), obj.get_email(), obj.get_senha(), obj.get_pontos()))

    @classmethod
    def listar(cls):
        sql = "SELECT * FROM usuario"
        resultado = cls.execute(sql)
        # Usamos resultado.rows para criar a lista de objetos
        objs = [Usuario(*row) for row in resultado.rows]
        return objs
    
    @classmethod
    def listar_id(cls, id):
        sql = "SELECT * FROM usuario WHERE id = ?"
        resultado = cls.execute(sql, (id,))
        # Como não existe mais fetchone(), pegamos a primeira linha [0] se a lista não estiver vazia
        if resultado.rows:
            return Usuario(*resultado.rows[0])
        return None
    
    @classmethod
    def atualizar(cls, obj):
        sql = """
            UPDATE usuario SET nome=?, email=?, senha=?, pontos=?
            WHERE id=?
        """
        cls.execute(sql, (obj.get_nome(), obj.get_email(), obj.get_senha(), obj.get_pontos(), obj.get_id()))

    @classmethod
    def excluir(cls, obj):
        sql = "DELETE FROM usuario WHERE id=?"
        cls.execute(sql, (obj.get_id(),))
    
    @classmethod
    def atualizar_todos_pontos(cls):
        sql = """
            UPDATE usuario
            SET pontos = (
                SELECT COALESCE(SUM(pontos_ganhos), 0) 
                FROM palpites 
                WHERE usuario_id = usuario.id
            )
        """
        cls.execute(sql)
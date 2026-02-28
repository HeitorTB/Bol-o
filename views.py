from models.usuario import Usuario,usuarioDAO
from models.jogos import Jogo, JogoDAO

class View:
    
    def usuario_listar():
        return usuarioDAO.listar()
    
    def usuario_inserir(nome, email, senha):
        for c in usuarioDAO.listar():
            if c.get_email() == email.lower():
                raise ValueError("Já existe um usuário com esse email")
        usuario = Usuario(0, nome, email, senha, 0)
        usuarioDAO.inserir(usuario)

    def usuario_listar_id(id):
        return usuarioDAO.listar_id(id)
    
    def usuario_atualizar(id, nome, email, senha, pontos):
        for c in usuarioDAO.listar():
            if c.get_id() != id and c.get_email() == email.lower():
                raise ValueError("Já existe outro usuario com este e-mail.")
        usuario = Usuario(id, nome, email, senha, pontos)
        usuarioDAO.atualizar(usuario)
    
    def usuario_excluir(id):
        usuario = usuarioDAO.listar_id(id)
        if usuario is None:
            raise ValueError("usuario não encontrado")
        usuarioDAO.excluir(usuario)

    def usuario_autenticar(email, senha):
        for c in View.usuario_listar():
            if c.get_email() == email and c.get_senha() == senha:
                return {"id": c.get_id(), "nome": c.get_nome()}
        return None
    
    def criar_admin():
        for c in View.usuario_listar():
            if c.get_email() == "admin":
                return
        View.usuario_inserir("admin", "admin", "1234",) 
    
    @classmethod
    def jogo_inserir(cls, time_a, time_b, data_hora):
        # Cria o objeto jogo (id 0, gols 0, e finalizado False)
        jogo = Jogo(0, time_a, time_b, data_hora, 0, 0, False)
        JogoDAO.inserir(jogo)

    @classmethod
    def jogo_listar(cls):
        return JogoDAO.listar()
    
    @classmethod
    def jogo_atualizar(cls, id, time_a, time_b, data_hora, gols_a, gols_b, finalizado):
        # Remonta o objeto Jogo, mas agora com os gols e status atualizados
        jogo_atualizado = Jogo(id, time_a, time_b, data_hora, gols_a, gols_b, finalizado)
        JogoDAO.atualizar(jogo_atualizado)

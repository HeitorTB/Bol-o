from models.usuario import Usuario,usuarioDAO

class View:
    
    def usuario_listar():
        u = usuarioDAO.inserir()
        u.sort(key=lambda obj: obj.get_nome())
        return u
    
    def usuario_inserir(nome, email, senha, pontos):
        for c in usuarioDAO.listar():
            if c.get_email.lower() == email.lower():
                raise ValueError("Já existe um usuário com esse email")
        usuario = Usuario(0, nome, email, senha, pontos)
        usuarioDAO.inserir(usuario)

    def usuario_listar_id(id):
        return usuarioDAO.listar_id(id)
    
    def usuario_atualizar(id, nome, email, senha, pontos):
        for c in usuarioDAO.listar():
            if c.get_id() != id and c.get_email().lower() == email.lower():
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

import pandas as pd
from dao_sql.DAO import DAO

class Usuario:
    def __init__(self, id, nome, email, senha, pontos, status="Pendente"):
        self.set_id(id)
        self.set_nome(nome)
        self.set_email(email)
        self.set_senha(senha)
        self.set_pontos(pontos)
        self.set_status(status)

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
    def set_status(self, valor):
        self.__status = valor
        
    def get_id(self): return self.__id
    def get_nome(self): return self.__nome
    def get_senha(self): return self.__senha
    def get_email(self): return self.__email
    def get_pontos(self): return self.__pontos
    def get_status(self): return self.__status

class usuarioDAO(DAO):
    @classmethod
    def inserir(cls, obj):
        df = cls.listar_aba("usuario")
        novo_id = int(df["id"].max() + 1) if not df.empty else 1
        
        nova_linha = {
            "id": novo_id,
            "nome": obj.get_nome(),
            "email": obj.get_email().lower(),
            "senha": obj.get_senha(),
            "pontos": obj.get_pontos(),
            "status": obj.get_status()
        }
        
        # O Pandas mais novo prefere pd.concat para adicionar linhas
        if df.empty:
             df = pd.DataFrame([nova_linha])
        else:
             df = pd.concat([df, pd.DataFrame([nova_linha])], ignore_index=True)
             
        cls.salvar_aba("usuario", df)

    @classmethod
    def listar(cls):
        df = cls.listar_aba("usuario")
        
        # BLINDAGEM: Se a coluna status não existir na planilha, ele cria ela com "Pendente"
        if "status" not in df.columns:
            df["status"] = "Pendente"
            
        # BLINDAGEM: Se a pessoa existir na planilha mas o status estiver em branco (NaN), coloca Pendente
        df["status"] = df["status"].fillna("Pendente")

        usuarios = []
        for _, row in df.iterrows():
            senha_limpa = str(row['senha']).removesuffix('.0')
            
            usuarios.append(Usuario(
                int(row['id']), 
                str(row['nome']), 
                str(row['email']), 
                senha_limpa, 
                int(row.get('Pontos', 0)),
                str(row['status']) # Agora é seguro ler
            ))
        return usuarios

    @classmethod
    def listar_id(cls, id):
        df = cls.listar_aba("usuario")
        
        # BLINDAGEM: Mesma coisa aqui, garante que a coluna existe
        if "status" not in df.columns:
            df["status"] = "Pendente"
        df["status"] = df["status"].fillna("Pendente")
        
        r = df[df['id'] == id]
        if not r.empty:
            row = r.iloc[0]
            senha_limpa = str(row['senha']).removesuffix('.0')
            
            return Usuario(
                int(row['id']), 
                str(row['nome']), 
                str(row['email']), 
                senha_limpa, 
                int(row['pontos']),
                str(row['status'])
            )
        return None

    @classmethod
    def atualizar(cls, obj):
        df = cls.listar_aba("usuario")
        
        # Se for atualizar, garante que a coluna existe no DF
        if "status" not in df.columns:
            df["status"] = "Pendente"
            
        df.loc[df['id'] == obj.get_id(), ['nome', 'email', 'senha', 'pontos', 'status']] = \
            [obj.get_nome(), obj.get_email(), obj.get_senha(), obj.get_pontos(), obj.get_status()]
            
        cls.salvar_aba("usuario", df)
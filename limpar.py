import libsql

# Cole suas chaves reais aqui dentro das aspas
url_banco = "libsql://bolao-db-heitortb.aws-us-west-2.turso.io"
token_banco = "eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9.eyJhIjoicnciLCJpYXQiOjE3NzIzMTg5MzQsImlkIjoiMDE5Y2E2NTItOGYwMS03NzQwLTg3YjUtZmY3MjUxMTE5MjkwIiwicmlkIjoiMTg1OTRhMTItN2YzZC00MzVlLWIzMzEtM2UyNDgyZmMzZjQzIn0.zvToPWmIWIIyp2h8bQ2byDuiuRNaKQiCCfv3u0rPsZx0qdcvY1E_DM-gutKiuLB7m1yKQERMPbZO7b2aVq4vAQ"

print("Conectando ao banco na nuvem...")
conexao = libsql.connect(database=url_banco, auth_token=token_banco)

print("Apagando palpites antigos...")
conexao.execute("DELETE FROM palpites;")
conexao.commit()

print("Apagando usuários de teste...")
conexao.execute("DELETE FROM usuario;")
conexao.commit()

print("Limpeza concluída com sucesso! 🧹✨")
conexao.close()
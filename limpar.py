import libsql_client as libsql

# Suas chaves de acesso
url_banco = "libsql://bolao-db-heitortb.aws-us-west-2.turso.io"
token_banco = "eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9.eyJhIjoicnciLCJpYXQiOjE3NzIzMTg5MzQsImlkIjoiMDE5Y2E2NTItOGYwMS03NzQwLTg3YjUtZmY3MjUxMTE5MjkwIiwicmlkIjoiMTg1OTRhMTItN2YzZC00MzVlLWIzMzEtM2UyNDgyZmMzZjQzIn0.zvToPWmIWIIyp2h8bQ2byDuiuRNaKQiCCfv3u0rPsZx0qdcvY1E_DM-gutKiuLB7m1yKQERMPbZO7b2aVq4vAQ"

# 💡 A mesma correção que fizemos no sistema: forçar o uso do HTTPS
if url_banco.startswith("libsql://"):
    url_banco = url_banco.replace("libsql://", "https://")

print("Conectando ao banco na nuvem...")
conexao = libsql.create_client_sync(url=url_banco, auth_token=token_banco)

print("Apagando palpites antigos...")
conexao.execute("DELETE FROM palpites;")

print("Apagando usuários de teste...")
conexao.execute("DELETE FROM usuario;")

print ("Apagando jogos... ")
conexao.execute("DELETE FROM jogos;")

print("Limpeza concluída com sucesso! 🧹✨")
conexao.close()
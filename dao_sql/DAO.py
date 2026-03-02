import sqlite3
from datetime import datetime

class DAO:
    conn = None
    nome_bd = "tabela.db"

    @classmethod
    def abrir(cls):
        # Só abre se não houver uma conexão ativa
        if cls.conn is None:
            cls.conn = sqlite3.connect(cls.nome_bd)
            cls.conn.execute("PRAGMA foreign_keys = ON")
 
    @classmethod
    def fechar(cls):
        if cls.conn:
            cls.conn.close()
            cls.conn = None # Importante resetar para None ao fechar
        
    @classmethod
    def execute(cls, sql, params=None):
        # GARANTIA: Se a conexão estiver fechada ou for None, abra-a aqui.
        if cls.conn is None:
            cls.abrir()
            
        try:
            cursor = cls.conn.cursor()
            cursor.execute(sql, params or [])
            cls.conn.commit()
            return cursor
        except sqlite3.ProgrammingError:
            # Caso a conexão tenha sido fechada externamente, reabre e tenta de novo
            cls.abrir()
            return cls.execute(sql, params)
import sqlite3

def open_database()-> sqlite3.Connection:
    sql = open("sql/schema.sql", "r", encoding= "utf-8").read()    
    db = sqlite3.connect("output/solicitacoes.db")
    db.executescript(sql)
    return db


def insert_row(db, row)-> tuple:
    try:            
        db.execute(
        """INSERT INTO solicitacoes
            (id_solicitacao, data, area, descricao, valor, status)
            VALUES (?, ?, ?, ?, ?, ?)""",
        (row["id_solicitacao"], row["data"], row["area"],
        row["descricao"], row["valor"], row["status"]),
        )
        db.commit()    
    except sqlite3.IntegrityError:
        return (False, "Identificador duplicado")
    return (True, "")
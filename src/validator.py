from datetime import datetime
def validate_row(row) -> tuple:
    keys = {"id_solicitacao", "data", "area", "valor", "status", "descricao"}
    status = {"Aprovado", "Pendente", "Cancelado"}
    for k in keys:
      if k not in row:
         return (False, f"O campo {k}, nao esta presente")
      if not row[k].strip():
         return (False, f"O campo {k}, esta vazio")
      if k == "data":
         date = row[k]
         try:
            date = datetime.strptime(row["data"].strip(), "%Y-%m-%d")
         except ValueError:
            return (False, f"O campo data tem um formato errado")
      if k == "valor":
         value = row[k].replace(".", "")
         value = value.replace(",", ".")
         try:
            value = float(value)
         except ValueError:         
            return (False, f"O campo valor deve ser um numero valido")
         if value <= 0:
            return (False, f"O campo valor tem um valor menor ou igual que 0")
      if k == "status":
         if row[k] not in status:
            return (False, f"O campo status tem um valor invalido")
    return (True, {
        "id_solicitacao": row["id_solicitacao"].strip(),
        "data": row["data"].strip(),
        "area": row["area"].strip(),
        "descricao": row["descricao"].strip(),
        "valor": value,
        "status": row["status"].strip(),
    })    

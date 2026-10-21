import csv
def write_rejection(rows):
    with open("output/rejeitados.csv", "w", encoding= "utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["id_solicitacao", "data", "area", "descricao", "valor", "status", "motivo"])
        writer.writeheader()
        writer.writerows(rows)
def write_report(total_report, sum_area):
    with open("output/relatorio.csv", "w", encoding= "utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["total_registros", "total_validos", "total_rejeitados", "total_aprovados", "total_pendentes", "total_cancelados"])
        writer.writeheader()
        writer.writerows(total_report)

        writer_area = csv.DictWriter(f, fieldnames=["area", "soma_aprovado"])
        writer_area.writeheader()
        writer_area.writerows(sum_area)
        
    





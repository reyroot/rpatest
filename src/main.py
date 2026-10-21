from reader import read_csv
from log import log_info, log_error, setup_log
from repository import open_database, insert_row
from validator import validate_row
from report import write_rejection, write_report

if __name__ == "__main__":

    setup_log()
    requests = None
    db = None
    rejected = []
    sum_area = {}
    total_items = 0
    total_items_valid = 0
    total_items_rejected = 0
    total_items_status_aproved = 0
    total_items_status_pending = 0
    total_items_status_cancel = 0

    log_info("Inicio")
    try:
        requests = read_csv("input/solicitacoes.csv")
        total_items = len(requests)
    except Exception:
        log_error("Erro na leitura do arquivo input/solicitacoes.csv")
        exit()
    try:
        db = open_database()
    except Exception:
        log_error("Erro ao abrir o banco de dados output/solicitacoes.db")
        exit()

    for request in requests:
        valid = validate_row(request)
        if valid[0]:
            row = valid[1]
            inserted, reason = insert_row(db, row)
            if not inserted:
                log_error(f"{row['id_solicitacao']}: {reason}")
                rejected.append({**request, "motivo": reason})
                total_items_rejected += 1
                continue

            total_items_valid += 1
            log_info(f"Solicitacao {row['id_solicitacao']} gravada")

            if row["status"] == "Aprovado":
                total_items_status_aproved += 1
                area = row["area"]
                sum_area[area] = sum_area.get(area, 0) + row["valor"]
            elif row["status"] == "Pendente":
                total_items_status_pending += 1
            else:
                total_items_status_cancel += 1
        else:
            log_error(f"{request['id_solicitacao']}: {valid[1]}")
            rejected.append({**request, "motivo": valid[1]})
            total_items_rejected += 1

    write_rejection(rejected)
    write_report(
        [{
            "total_registros": total_items,
            "total_validos": total_items_valid,
            "total_rejeitados": total_items_rejected,
            "total_aprovados": total_items_status_aproved,
            "total_pendentes": total_items_status_pending,
            "total_cancelados": total_items_status_cancel,
        }],
        [{"area": area, "soma_aprovado": total} for area, total in sum_area.items()],
    )

    log_info(
        "Fim. "
        f"lidos={total_items}, validos={total_items_valid}, "
        f"rejeitados={total_items_rejected}, aprovados={total_items_status_aproved}, "
        f"pendentes={total_items_status_pending}, cancelados={total_items_status_cancel}, "
        f"soma_por_area={sum_area}"
    )
    db.close()

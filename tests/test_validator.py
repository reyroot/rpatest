import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from validator import validate_row


def test_fila_valida():
    row = {
        "id_solicitacao": "SOL-001",
        "data": "2026-10-01",
        "area": "Peças",
        "descricao": "Compra de material",
        "valor": "350,00",
        "status": "Aprovado",
    }
    ok, result = validate_row(row)
    assert ok is True
    assert result["valor"] == 350.0


def test_valor_invalido():
    row = {
        "id_solicitacao": "SOL-008",
        "data": "2026-10-05",
        "area": "Oficina",
        "descricao": "Serviço terceirizado",
        "valor": "abc",
        "status": "Aprovado",
    }
    ok, result = validate_row(row)
    assert ok is False
    assert "numero" in result


def test_area_vacia():
    row = {
        "id_solicitacao": "SOL-010",
        "data": "2026-10-06",
        "area": "",
        "descricao": "Compra emergencial",
        "valor": "300,00",
        "status": "Aprovado",
    }
    ok, result = validate_row(row)
    assert ok is False
    assert "area" in result

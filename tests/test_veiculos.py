"""
Testes unitários — Cadastro de Veículos
"""
import os
import tempfile
import pytest

from app import create_app


# ── fixtures ─────────────────────────────────────────────────────────────────

@pytest.fixture
def app():
    """Cria aplicação com banco em arquivo temporário para cada teste."""
    db_fd, db_path = tempfile.mkstemp(suffix=".db")

    application = create_app({
        "TESTING": True,
        "DATABASE": db_path,
    })

    yield application

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


VEICULO_VALIDO = {
    "placa":  "ABC1234",
    "marca":  "Toyota",
    "modelo": "Corolla",
    "ano":    2022,
    "cor":    "Prata",
    "dono":   "Joao Silva",
}


# ── Teste 1 — Cadastro com dados válidos ─────────────────────────────────────

def test_cadastrar_veiculo_sucesso(client):
    resp = client.post("/veiculos/", json=VEICULO_VALIDO)
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["placa"] == "ABC1234"
    assert data["marca"] == "Toyota"
    assert data["modelo"] == "Corolla"


# ── Teste 2 — Placa duplicada retorna 409 ────────────────────────────────────

def test_cadastrar_placa_duplicada(client):
    client.post("/veiculos/", json=VEICULO_VALIDO)
    resp = client.post("/veiculos/", json=VEICULO_VALIDO)
    assert resp.status_code == 409
    assert "já cadastrado" in resp.get_json()["erro"]


# ── Teste 3 — Placa inválida retorna 400 ─────────────────────────────────────

def test_cadastrar_placa_invalida(client):
    veiculo = {**VEICULO_VALIDO, "placa": "INVALIDA"}
    resp = client.post("/veiculos/", json=veiculo)
    assert resp.status_code == 400
    assert "Placa inválida" in resp.get_json()["erro"]


# ── Teste 4 — Ano inválido retorna 400 ───────────────────────────────────────

def test_cadastrar_ano_invalido(client):
    veiculo = {**VEICULO_VALIDO, "placa": "DEF5678", "ano": 1800}
    resp = client.post("/veiculos/", json=veiculo)
    assert resp.status_code == 400
    assert "Ano inválido" in resp.get_json()["erro"]


# ── Teste 5 — Campos obrigatórios ausentes retorna 400 ───────────────────────

def test_cadastrar_campos_faltando(client):
    resp = client.post("/veiculos/", json={"placa": "GHI9012"})
    assert resp.status_code == 400
    assert "Campos obrigatórios ausentes" in resp.get_json()["erro"]


# ── Teste 6 — Busca por placa existente retorna 200 ──────────────────────────

def test_buscar_veiculo_existente(client):
    client.post("/veiculos/", json=VEICULO_VALIDO)
    resp = client.get("/veiculos/ABC1234")
    assert resp.status_code == 200
    assert resp.get_json()["dono"] == "Joao Silva"


# ── Teste 7 — Busca por placa inexistente retorna 404 ────────────────────────

def test_buscar_veiculo_inexistente(client):
    resp = client.get("/veiculos/XYZ9999")
    assert resp.status_code == 404
    assert "Nenhum veículo encontrado" in resp.get_json()["erro"]


# ── Teste 8 — Placa no formato Mercosul é aceita ─────────────────────────────

def test_cadastrar_placa_mercosul(client):
    veiculo = {**VEICULO_VALIDO, "placa": "ABC1D23"}
    resp = client.post("/veiculos/", json=veiculo)
    assert resp.status_code == 201
    assert resp.get_json()["placa"] == "ABC1D23"


# ── Teste 9 — Listar retorna lista vazia inicialmente ────────────────────────

def test_listar_vazio(client):
    resp = client.get("/veiculos/")
    assert resp.status_code == 200
    assert resp.get_json() == []


# ── Teste 10 — Listar retorna veículo cadastrado ─────────────────────────────

def test_listar_apos_cadastro(client):
    client.post("/veiculos/", json=VEICULO_VALIDO)
    resp = client.get("/veiculos/")
    assert resp.status_code == 200
    lista = resp.get_json()
    assert len(lista) == 1
    assert lista[0]["placa"] == "ABC1234"

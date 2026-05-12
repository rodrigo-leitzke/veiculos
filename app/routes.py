import re
from datetime import datetime
from flask import Blueprint, request, jsonify

from .database import get_db

bp = Blueprint("veiculos", __name__, url_prefix="/veiculos")


# helpers


def placa_valida(placa: str) -> bool:
    p = placa.upper().replace("-", "").replace(" ", "")
    antigo = re.fullmatch(r"[A-Z]{3}\d{4}", p)
    mercosul = re.fullmatch(r"[A-Z]{3}\d[A-Z]\d{2}", p)
    return bool(antigo or mercosul)


def normalizar_placa(placa: str) -> str:
    return placa.upper().replace(" ", "")


def ano_valido(ano) -> bool:
    try:
        ano = int(ano)
        return 1886 <= ano <= datetime.now().year + 1
    except (ValueError, TypeError):
        return False


# endpoint 1 - cadastrar veiculo

@bp.route("/", methods=["POST"])
def cadastrar():
    """
    POST /veiculos/
    Body JSON: { placa, marca, modelo, ano, cor, dono }
    """
    data = request.get_json(silent=True) or {}

    campos = ["placa", "marca", "modelo", "ano", "cor", "dono"]
    faltando = [c for c in campos if not data.get(c)]
    if faltando:
        return jsonify({"erro": f"Campos obrigatórios ausentes: {faltando}"}), 400

    placa = normalizar_placa(data["placa"])

    if not placa_valida(placa):
        return jsonify({"erro": "Placa inválida. Use ABC-1234 (antigo) ou ABC1D23 (Mercosul)."}), 400

    if not ano_valido(data["ano"]):
        return jsonify({"erro": f"Ano inválido. Informe entre 1886 e {datetime.now().year + 1}."}), 400

    db = get_db()
    if db.execute("SELECT 1 FROM veiculos WHERE placa = ?", (placa,)).fetchone():
        return jsonify({"erro": f"Veículo com placa {placa} já cadastrado."}), 409

    db.execute(
        """INSERT INTO veiculos (placa, marca, modelo, ano, cor, dono)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (
            placa,
            data["marca"].strip().title(),
            data["modelo"].strip().title(),
            int(data["ano"]),
            data["cor"].strip().capitalize(),
            data["dono"].strip().title(),
        ),
    )
    db.commit()

    veiculo = db.execute(
        "SELECT * FROM veiculos WHERE placa = ?", (placa,)
    ).fetchone()

    return jsonify(dict(veiculo)), 201


# endpoint 2 - buscar por placa

@bp.route("/<string:placa>", methods=["GET"])
def buscar(placa: str):
    """GET /veiculos/<placa>"""
    placa = normalizar_placa(placa)

    if not placa_valida(placa):
        return jsonify({"erro": "Formato de placa inválido."}), 400

    db = get_db()
    veiculo = db.execute(
        "SELECT * FROM veiculos WHERE placa = ?", (placa,)
    ).fetchone()

    if veiculo is None:
        return jsonify({"erro": f"Nenhum veículo encontrado com a placa {placa}."}), 404

    return jsonify(dict(veiculo)), 200


# endpoint 3 - listar todos

@bp.route("/", methods=["GET"])
def listar():
    """GET /veiculos/"""
    db = get_db()
    rows = db.execute(
        "SELECT * FROM veiculos ORDER BY marca, modelo"
    ).fetchall()
    return jsonify([dict(r) for r in rows]), 200

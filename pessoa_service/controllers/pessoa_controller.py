from flask import Blueprint, jsonify, Request
from models import pessoa_model

pessoa_bp = Blueprint('pessoa_bp', __name__)

@pessoa_bp.route('/professores', methods=['GET'])
def listar_professores():
    professores = pessoa_model.listar_professores()
    return jsonify(professores)

@pessoa_bp.route('/alunos', methods=['GET'])
def listar_alunos():
    alunos = pessoa_model.listar_alunos()
    return jsonify(alunos)

@pessoa_bp.route('/disciplinas/<id_disciplina>', methods=['GET'])
def listar_diciplinas(id_disciplina):
    disciplina = pessoa_model.get_disciplina(id_disciplina)
    return jsonify(disciplina)

@pessoa_bp.route('/leciona/<int:id_professor>/<int:id_disciplina>', methods=['GET'])
def verificar_leciona(id_professor, id_disciplina):
    try:
        leciona = pessoa_model.leciona(id_professor, id_disciplina)
        return jsonify({'leciona': leciona}, listar_diciplinas())
    except pessoa_model.DisciplinaNaoEncontrada:
        return jsonify({'erro': 'Disciplina não encontrada'}), 404

from flask import Blueprint, jsonify, request
from models import atividade_model
from clients.pessoa_service_client import PessoaServiceClient

atividade_bp = Blueprint('atividade_bp', __name__)

@atividade_bp.route('/', methods=['GET'])
def listar_atividades():
    atividades = atividade_model.listar_atividades()
    return jsonify(atividades)
    

@atividade_bp.route('/disciplina/<int:id_disciplina>', methods=['GET'])
def listar_atividades_disciplina(id_disciplina):
    data = atividade_model.listar_atividades()
    atividades_da_disciplina = []
    for i in data:
        if i["id_disciplina"] == id_disciplina:
            atividades_da_disciplina.append(i)
    return jsonify(atividades_da_disciplina), 200


@atividade_bp.route('/<int:id_atividade>', methods=['GET'])
def obter_atividade(id_atividade):
    try:
        atividade = atividade_model.obter_atividade(id_atividade)
        return jsonify(atividade)
    except atividade_model.AtividadeNotFound:
        return jsonify({'erro': 'Atividade não encontrada'}), 404

@atividade_bp.route('/<int:id_atividade>/professor/<int:id_professor>', methods=['GET'])
def obter_atividade_para_professor(id_atividade, id_professor):
    try:
        atividade = atividade_model.obter_atividade(id_atividade)
        if not PessoaServiceClient.verificar_leciona(id_professor, atividade['id_disciplina']):
            atividade = atividade.copy()
            atividade.pop('respostas', None)
        return jsonify(atividade)
    except atividade_model.AtividadeNotFound:
        return jsonify({'erro': 'Atividade não encontrada'}), 404


#cria atividade
#      |
#      v
@atividade_bp.route('/adicionar', methods=["POST"])
def criar_atividades():
    id = len(atividade_model.atividades)
    data = request.get_json()
    respostas = data.get("respostas", [])
    nova_atividade = {
        "enunciado": data.get("enunciado"),
        "id_atividade": id + 1,
        "id_disciplina": data.get("id_disciplina"),
        "respostas": [
            {
                "id_aluno": resposta.get("id_aluno"),
                "nota": resposta.get("nota"),
                "resposta": resposta.get("resposta")
            }
            for resposta in respostas
        ]
    }
    try:
        atividade_model.atividades.append(nova_atividade)
        return jsonify(atividade_model.atividades)
    except TypeError:
        return jsonify({"error": "Ocorreu um erro ao adicionar a atividade"}), 500


#deleta atividade
#      |
#      v
@atividade_bp.route('/delete/<int:id_atividade>', methods=["DELETE"])
def apagar_atividades(id_atividade):
    atividades = atividade_model.listar_atividades()
    try:
        atividade = next((a for a in atividade_model.atividades if a["id_atividade"] == id_atividade), None)
        if atividade:
            atividade_model.atividades.remove(atividade)
        return jsonify({"mesage": "atividade removida"}, atividades),200
    except TypeError:
        return jsonify({"error": "Ocorreu um erro ao adicionar a atividade"}), 500
    
#atualiza atividade
#      |
#      v
@atividade_bp.route('/update/<int:id_atividade>', methods=["PUT"])
def atualizar_atividades(id_atividade):
    
    try:
        atividade = next((a for a in atividade_model.atividades if a["id_atividade"] == id_atividade), None)
        if atividade:
            data = request.get_json()
            atividade["enunciado"] = data.get("enunciado")
            atividade["id_disciplina"] = data.get("id_disciplina")

        return jsonify({"mesage": "atividade atualizada"}, ),200
    except TypeError:
        return jsonify({"error": "Ocorreu um erro ao adicionar a atividade"}), 500
    

    # Deve-se implementar os endpoints de POST, PUT  e DELETE, respeitando a arquitetura já definida do microsserviço.

# A atividade deve ter os seguintes campos (já definidos):
# id_atividade: Identificador único da atividade (número inteiro).
# id_disciplina: Identificador da disciplina à qual a atividade pertence (número inteiro).
# enunciado: Descrição da atividade (texto).
# respostas: Lista de respostas fornecidas pelos alunos (lista de objetos com id_aluno, resposta e nota).
# Criar as rotas: POST (/atividades/): Cria uma nova atividade.
# Requer um corpo de solicitação com os campos id_disciplina, enunciado e respostas (campo respostas pode ser uma lista vazia inicialmente).

# PUT (/atividades/<int:id_atividade>/): Atualiza uma atividade existente.
# Requer um corpo de solicitação com os campos id_disciplina, enunciado e respostas (os campos podem ser alterados).

# DELETE (/atividades/<int:id_atividade>/): Exclui uma atividade existente.
# Exclui a atividade com o id_atividade especificado.

# Além disse, enviar alguns prints de TODAS as rotas sendo executadas no Postman + código fonte

# Recomendação: Clone o repositório do projeto, faça as implementações, crie uma pasta "imagens" inserindo as imagens solicitadas e suba em seu github.
import requests
from models import pessoa_model

def verifica_leciona(id_professor, id_disciplina):
    try:
        r = requests.get(f"http://localhost:5001/leciona/{id_professor}/{id_disciplina}")
        if r.status_code == 404:
            return False, 'Disciplina não encontrada'
        return r.json().get('leciona', False)
    except requests.RequestException as e:
        return False, f"Erro na comunicação com pessoa_service: {e}"




def get_disciplina_atividades(id_disciplina):
    try:
        nmr = int(id_disciplina)
        disciplinas = pessoa_model.disciplinas
        disciplina = next((d for d in disciplinas if d['id_disciplina'] == nmr), None)
        
        if not disciplina:
            return False, 'Disciplina não encontrada'

        r = requests.get(f"http://localhost:5002/atividades/disciplina/{id_disciplina}")
        if r.status_code == 404:
            return False, 'Nenhuma atividade para esta disciplina'

        dados = [
            {"disciplina": disciplina['nome']},
            {"atividades": r.json()}
        ]
        return dados
    except requests.RequestException as e:
        return False, f"Erro na comunicação com atividade_service: {e}"
import requests

PESSOA_SERVICE_URL = "http://localhost:5001/pessoas"

class PessoaServiceClient:
    @staticmethod
    def verificar_leciona(id_professor, id_disciplina):
        url = f"{PESSOA_SERVICE_URL}/leciona/{id_professor}/{id_disciplina}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            print(f"Resposta da API: {data}")
            if isinstance(data, list) and len(data) > 0:
                leciona_info = next((item for item in data if "leciona" in item), None)
                if leciona_info and isinstance(leciona_info["leciona"], list) and len(leciona_info["leciona"]) > 0:
                    return leciona_info["leciona"][0]
            print("Formato inesperado na resposta da API.")
            return False
        except requests.RequestException as e:
            print(f"Erro ao acessar o pessoa_service: {e}")
            return False

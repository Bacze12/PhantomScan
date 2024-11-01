import requests

def buscar_exploits_en_github(cve_id, max_resultados=5):
    url = f"https://api.github.com/search/repositories?q={cve_id}+exploit+in:readme+in:description"
    headers = {"Accept": "application/vnd.github.v3+json"}
    params = {
        "sort": "stars",
        "order": "desc",
        "per_page": max_resultados
    }
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        repositorios = response.json().get('items', [])
        resultados = []
        for repo in repositorios:
            info_repo = {
                "Nombre": repo.get("name"),
                "Descripción": repo.get("description"),
                "URL": repo.get("html_url"),
                "Estrellas": repo.get("stargazers_count"),
                "Lenguaje": repo.get("language"),
                "Última actualización": repo.get("updated_at")
            }
            resultados.append(info_repo)
        return resultados
    else:
        print(f"Error {response.status_code}: No se pudo obtener la información.")
        return None



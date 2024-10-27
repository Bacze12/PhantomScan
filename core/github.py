import requests

def buscar_exploits_en_github(cve_id):
    url = f"https://api.github.com/search/repositories?q={cve_id}+exploit"
    headers = {"Accept": "application/vnd.github.v3+json"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get('items', [])
    else:
        return None
import requests

def obtener_cve(servicio, version):
    url = f"https://cve.circl.lu/api/search/{servicio} {version}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def correlacionar_resultados_escaneo(resultados):
    correlaciones = []
    for resultado in resultados:
        for puerto in resultado['ports']:
            if 'service' in puerto:
                servicio = puerto['service']
                version = puerto['version']
                cves = obtener_cve(servicio, version)
                if cves:
                    for cve in cves:
                        correlaciones.append({
                            'host': resultado['host'],
                            'servicio': servicio,
                            'version': version,
                            'CVE': cve['id'],
                            'descripción': cve['summary'],
                            'gravedad': cve.get('cvss', {}).get('score', 'N/A')
                        })
    return correlaciones

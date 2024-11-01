import requests

def obtener_cve(servicio, version, anio_minimo=2020):
    """Busca CVEs recientes para un servicio y versión en una API pública."""
    url = f"https://cve.circl.lu/api/search/{servicio} {version}"
    response = requests.get(url)
    if response.status_code == 200:
        # Filtrar CVEs que sean del año mínimo en adelante
        cves = [
            cve for cve in response.json() 
            if 'id' in cve and 'summary' in cve and int(cve['id'].split('-')[1]) >= anio_minimo
        ]
        return cves
    else:
        return None

def correlacionar_resultados_escaneo(resultados):
    """Correlaciona resultados del escaneo con posibles CVEs."""
    correlaciones = []
    for resultado in resultados:
        for puerto in resultado['ports']:
            if 'service' in puerto:
                servicio = puerto['service']
                version = puerto['version']

                # Filtrar servicios y versiones irrelevantes
                if version == "N/A" or "blackice" in servicio.lower():
                    continue

                cves = obtener_cve(servicio, version)
                if cves:
                    for cve in cves:
                        severidad = cve.get('cvss', {}).get('score', 'N/A')
                        if severidad != 'N/A' and severidad >= 7:  # Considera solo CVEs críticos (7+)
                            correlaciones.append({
                                'host': resultado['host'],
                                'servicio': servicio,
                                'version': version,
                                'CVE': cve['id'],
                                'descripción': cve['summary'],
                                'gravedad': severidad
                            })

    return correlaciones

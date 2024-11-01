import os
import datetime
from core.github import buscar_exploits_en_github
from core.cve import correlacionar_resultados_escaneo

def ensure_directory_exists(directory):
    """Asegura que el directorio exista; si no, lo crea."""
    if not os.path.exists(directory):
        os.makedirs(directory)

def generate_report(scan_results, report_format='txt'):
    """Genera un reporte a partir de los resultados del escaneo."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_dir = "scan_results"
    
    # Asegurar que el directorio existe
    ensure_directory_exists(report_dir)
    
    if report_format == 'txt':
        report_file = os.path.join(report_dir, f"report_{timestamp}.txt")
        try:
            with open(report_file, 'w') as file:
                file.write(f"=== Reporte de Escaneo ===\n")
                file.write(f"Fecha: {timestamp}\n\n")
                
                if not scan_results:
                    file.write("No se encontraron resultados del escaneo.\n")
                else:
                    cve_results = correlacionar_resultados_escaneo(scan_results)
                    
                    for result in scan_results:
                        file.write(f"Host: {result['host']}\n")
                        if "mac" in result:
                            file.write(f"MAC: {result['mac']}\n")
                        file.write("Puertos:\n")
                        
                        for port in result['ports']:
                            file.write(f"  - Puerto: {port['port']} Estado: {port['state']} Servicio: {port['service']} Versión: {port['version']}\n")
                            link = f"https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword={port['service']}+{port['version']}"
                            file.write(f"    Verificar CVEs: {link}\n")
                            
                            if port.get("scripts"):
                                file.write("    Scripts:\n")
                                for script in port["scripts"]:
                                    file.write(f"      - {script['name']}: {script['output']}\n")
                            
                            exploits_github = buscar_exploits_en_github(f"{port['service']} {port['version']}")
                            if exploits_github:
                                file.write("    Exploits en GitHub:\n")
                                for exploit in exploits_github:
                                    file.write(f"      - Repositorio: {exploit.get('html_url', 'URL no disponible')} ")
                            else:
                                file.write("    No se encontraron exploits en GitHub.\n")
                        
                        file.write("  CVEs encontrados:\n")
                        for cve in cve_results:
                            if cve['host'] == result['host']:
                                file.write(f"    - {cve['CVE']}: {cve['descripción']} (Gravedad: {cve['gravedad']})\n")
                        file.write("\n")

                print(f"Reporte en texto generado exitosamente en {report_file}")
        except IOError as e:
            print(f"Error al generar el reporte en texto: {e}")

    elif report_format == 'html':
        report_file = os.path.join(report_dir, f"report_{timestamp}.html")
        try:
            with open(report_file, 'w') as file:
                file.write(f"<html><head><title>Reporte de Escaneo</title></head><body>")
                file.write(f"<h1>Reporte de Escaneo</h1>")
                file.write(f"<p><strong>Fecha:</strong> {timestamp}</p><hr>")
                
                if not scan_results:
                    file.write("<p>No se encontraron resultados del escaneo.</p>")
                else:
                    cve_results = correlacionar_resultados_escaneo(scan_results)
                    
                    for result in scan_results:
                        file.write(f"<h2>Host: {result['host']}</h2>")
                        if "mac" in result:
                            file.write(f"<p><strong>MAC:</strong> {result['mac']}</p>")
                        file.write("<h3>Puertos:</h3><ul>")
                        
                        for port in result['ports']:
                            port_info = f"Puerto: {port['port']} Estado: {port['state']} Servicio: {port['service']} Versión: {port['version']}"
                            file.write(f"<li>{port_info}")
                            link = f"https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword={port['service']}+{port['version']}"
                            file.write(f" <a href='{link}'>Verificar CVEs</a>")
                            
                            if port.get("scripts"):
                                file.write("<ul><li><strong>Scripts:</strong><ul>")
                                for script in port["scripts"]:
                                    file.write(f"<li>{script['name']}: {script['output']}</li>")
                                file.write("</ul></li></ul>")
                            
                            exploits_github = buscar_exploits_en_github(f"{port['service']} {port['version']}")
                            if exploits_github:
                                file.write("<ul><li><strong>Exploits en GitHub:</strong><ul>")
                                for exploit in exploits_github:
                                    file.write(f"<li><a href='{exploit.get('html_url', '#')}'>{exploit.get('html_url', 'URL no disponible')}</a></li>")
                                file.write("</ul></li></ul>")
                            else:
                                file.write("<p>No se encontraron exploits en GitHub.</p>")
                        
                        file.write("</li></ul>")
                        file.write("<h3>CVEs encontrados:</h3><ul>")
                        for cve in cve_results:
                            if cve['host'] == result['host']:
                                file.write(f"<li>{cve['CVE']}: {cve['descripción']} (Gravedad: {cve['gravedad']})</li>")
                        file.write("</ul><hr>")

                file.write("</body></html>")
                print(f"Reporte en HTML generado exitosamente en {report_file}")
        except IOError as e:
            print(f"Error al generar el reporte en HTML: {e}")
    else:
        print(f"Formato de reporte no soportado: {report_format}")

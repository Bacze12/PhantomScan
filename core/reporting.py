import os
import datetime
from core.github import buscar_exploits_en_github

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
                    for result in scan_results:
                        file.write(f"Host: {result['host']}\n")
                        if "mac" in result:
                            file.write(f"MAC: {result['mac']}\n")
                        file.write("Puertos:\n")
                        
                        for port in result['ports']:
                            file.write(f"  - Puerto: {port['port']} Estado: {port['state']} Servicio: {port['service']} Versión: {port['version']}\n")
                            link = f"https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword={port['service']}+{port['version']}"
                            file.write(f"    Verificar CVEs: {link}\n")
                            
                            # Incluir resultados de los scripts si existen
                            if port.get("scripts"):
                                file.write("    Scripts:\n")
                                for script in port["scripts"]:
                                    file.write(f"      - {script['name']}: {script['output']}\n")
                            
                            # Añadir resultados de exploits en GitHub
                            exploits_github = buscar_exploits_en_github(f"{port['service']} {port['version']}")
                            if exploits_github:
                                file.write("    Exploits en GitHub:\n")
                                for exploit in exploits_github:
                                    file.write(f"      - Repositorio: {exploit['html_url']} - Descripción: {exploit['description']}\n")
                            else:
                                file.write("    No se encontraron exploits en GitHub.\n")
                        file.write("\n")

                print(f"Reporte generado exitosamente en {report_file}")
        except IOError as e:
            print(f"Error al generar el reporte: {e}")
    else:
        print(f"Formato de reporte no soportado: {report_format}")



import os
import datetime

def ensure_directory_exists(directory):
    """Asegura que el directorio exista; si no, lo crea."""
    if not os.path.exists(directory):
        os.makedirs(directory)

def generate_report(scan_results, report_format='txt'):
    """Genera un reporte a partir de los resultados del escaneo."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_dir = "scan_results"
    
    # Asegurarse de que el directorio existe
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
                        file.write(f"Puertos:\n")
                        for port in result['ports']:
                            file.write(f"  - Puerto: {port['port']} Estado: {port['state']} Servicio: {port['service']} Versión: {port['version']}\n")
                            link = f"https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword={port['service']}+{port['version']}"
                            file.write(f"    Verificar CVEs: {link}\n")
                        file.write("\n")

                print(f"Reporte generado exitosamente en {report_file}")
        except IOError as e:
                print(f"Error al generar el reporte: {e}")

    else:
        print(f"Formato de reporte no soportado: {report_format}")



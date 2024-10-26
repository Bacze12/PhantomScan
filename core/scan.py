import subprocess
import os

def run_nmap_scan(ip_range, output_file):
    """
    Ejecuta un escaneo Nmap en el rango IP dado y guarda los resultados en un archivo.
    """
    try:
        # Comando Nmap
        nmap_command = ['nmap', '-sS', '-sV', '-O', ip_range, '-oN', output_file]
        print(f"Ejecutando: {' '.join(nmap_command)}")
        
        # Ejecutar el escaneo
        subprocess.run(nmap_command, check=True)
        
        print(f"Resultados guardados en {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar Nmap: {e}")

import subprocess

def scan_network(subnet, scan_type="-sS", ports=None):
    """Ejecuta un escaneo en la red con el tipo de escaneo especificado."""
    try:
        nmap_command = ["nmap", scan_type, subnet, "-sV"]
        if ports:
            nmap_command.extend(["-p", ports])
        
        print(f"Ejecutando: {' '.join(nmap_command)}")
        result = subprocess.run(nmap_command, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"Error al ejecutar Nmap: {result.stderr}")
            return None
        
        return parse_nmap_output(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar Nmap: {e}")
        return None

def parse_nmap_output(output):
    """Parsea la salida de Nmap y devuelve una lista de diccionarios con la información."""
    scan_results = []
    lines = output.split("\n")
    current_host = {}
    
    for line in lines:
        if line.startswith("Nmap scan report for"):
            if current_host:
                scan_results.append(current_host)
            current_host = {"host": line.split(" ")[-1], "ports": []}
        elif "open" in line or "filtered" in line:
            parts = line.split()
            current_host["ports"].append({
                "port": parts[0],
                "state": parts[1],
                "service": parts[2],
                "version": " ".join(parts[3:]) if len(parts) > 3 else "N/A"
            })
        elif line.startswith("MAC Address"):
            current_host["mac"] = line.split(" ")[2]
    
    if current_host:
        scan_results.append(current_host)
    
    return scan_results

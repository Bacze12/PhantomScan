import subprocess

def scan_network(subnet, scan_type="-sS", ports=None, no_ping=False, detect_os=False, script_scan=False, intensity_level=2):
    """Ejecuta un escaneo en la red con el tipo de escaneo especificado."""
    try:
        # Comando base con opciones configurables
        nmap_command = ["nmap", scan_type, "-sV"]
        
        # Opciones adicionales
        if no_ping:
            nmap_command.append("-Pn")  # Sin ping
        if detect_os:
            nmap_command.append("-O")   # Detección de sistema operativo
        if script_scan:
            nmap_command.append("-sC")  # Scripts básicos
        if ports:
            nmap_command.extend(["-p", ports])
        
        # Control de intensidad
        nmap_command.append(f"-T{intensity_level}")
        
        nmap_command.append(subnet)
        
        print(f"Ejecutando: {' '.join(nmap_command)}")
        
        # Ejecutar el escaneo y capturar la salida
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
    current_port = None
    
    for line in lines:
        if line.startswith("Nmap scan report for"):
            # Agrega el host actual al resultado final si tiene datos
            if current_host:
                scan_results.append(current_host)
            current_host = {"host": line.split(" ")[-1], "ports": []}
        elif "open" in line or "filtered" in line:
            # Parsear la información del puerto
            parts = line.split()
            current_port = {
                "port": parts[0],
                "state": parts[1],
                "service": parts[2],
                "version": " ".join(parts[3:]) if len(parts) > 3 else "N/A",
                "scripts": []
            }
            current_host["ports"].append(current_port)
        elif line.startswith("MAC Address"):
            # Capturar la dirección MAC
            current_host["mac"] = line.split(" ")[2]
        elif line.startswith("|") and current_port:
            # Verificar si el ":" está presente antes de dividir la línea
            if ":" in line:
                script_name = line.split(":", 1)[0].strip("| ")
                script_output = line.split(":", 1)[1].strip()
                current_port["scripts"].append({
                    "name": script_name,
                    "output": script_output
                })
    
    # Agregar el último host si contiene información
    if current_host:
        scan_results.append(current_host)
    
    return scan_results


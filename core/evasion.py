import subprocess

def run_fragmentation_scan(ip_range, output_file):
    """
    Ejecuta un escaneo Nmap con evasión mediante fragmentación de paquetes.
    """
    try:
        # Comando Nmap con fragmentación
        fragmentation_command = ['nmap', '-sS', '-f', ip_range, '-oN', output_file]
        print(f"Ejecutando escaneo fragmentado: {' '.join(fragmentation_command)}")
        
        subprocess.run(fragmentation_command, check=True)
        
        print(f"Resultados de fragmentación guardados en {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar el escaneo de fragmentación: {e}")

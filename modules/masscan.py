import subprocess

def run_masscan(ip_range, ports):
    """Ejecuta Masscan para escanear un rango de IP y puertos."""
    masscan_command = ["masscan", "-p", ports, ip_range]
    result = subprocess.run(masscan_command, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error al ejecutar Masscan: {result.stderr}")
        return None

    return result.stdout

import subprocess
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RESET = '\033[0m'

def simulate_user_activity():
    """Simula actividad de usuario para enmascarar el tráfico de escaneo."""
    print(f"{Colors.YELLOW}Simulando actividad de usuario...{Colors.RESET}")
    try:
        # Ejecuta actividades comunes como realizar consultas DNS, abrir una sesión web, etc.
        subprocess.Popen(["ping", "-c", "3", "www.google.com"])  # Simula un ping a Google
        subprocess.Popen(["curl", "http://youtube.com"])  # Simula una consulta web
        subprocess.Popen(["nslookup", "youtube.com"])  # Simula una consulta DNS
    except subprocess.CalledProcessError as e:
        print(f"{Colors.RED}Error durante la simulación de actividad: {e}{Colors.RESET}")
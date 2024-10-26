import subprocess
import netifaces
from utils.input_validation import input_with_validation

# Colores para la terminal
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RESET = '\033[0m'

def list_network_interfaces():
    """Lista todas las interfaces de red disponibles en el sistema."""
    try:
        result = subprocess.run(['ip', 'link'], capture_output=True, text=True)
        interfaces = [line.split(": ")[1] for line in result.stdout.splitlines() if ": " in line]
        return interfaces
    except subprocess.CalledProcessError as e:
        print(f"Error al listar las interfaces de red: {e}")
        return []

def get_subnet_for_interface(interface):
    """Obtiene la subred asociada a una interfaz de red."""
    ifaddresses = netifaces.ifaddresses(interface)
    if netifaces.AF_INET in ifaddresses:
        ip_info = ifaddresses[netifaces.AF_INET][0]
        return f"{ip_info['addr']}/{ip_info['netmask']}"
    else:
        return None

def print_available_interfaces(interfaces):
    """Imprime las interfaces de red disponibles."""
    print(f"{Colors.YELLOW}Interfaces disponibles:{Colors.RESET}")
    for i, interface in enumerate(interfaces):
        print(f"{i + 1}: {interface}")

def select_interface(interfaces):
    """Permite seleccionar una interfaz de red de la lista."""
    selected_index = input_with_validation(
        "Selecciona la interfaz (número): ",
        lambda x: x.isdigit() and 1 <= int(x) <= len(interfaces),
        "Por favor, selecciona un número válido."
    )
    return interfaces[int(selected_index) - 1]

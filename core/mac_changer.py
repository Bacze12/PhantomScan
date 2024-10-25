import subprocess
import random
from utils.input_validation import input_with_validation
from utils.network_utils import *

# Colores para la terminal
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RESET = '\033[0m'

def change_mac(interface, new_mac):
    """Cambia la dirección MAC de la interfaz especificada a new_mac."""
    try:
        # Desactivar la interfaz
        subprocess.run(['sudo', 'ifconfig', interface, 'down'], check=True)
        # Cambiar la MAC
        subprocess.run(['sudo', 'ifconfig', interface, 'hw', 'ether', new_mac], check=True)
        # Activar la interfaz
        subprocess.run(['sudo', 'ifconfig', interface, 'up'], check=True)
        print(f"Dirección MAC de {interface} cambiada a {new_mac}")
    except subprocess.CalledProcessError as e:
        print(f"Error al cambiar la dirección MAC: {e}")

def get_current_mac(interface):
    """Obtiene la dirección MAC actual de la interfaz."""
    try:
        result = subprocess.run(['ifconfig', interface], capture_output=True, text=True)
        return result.stdout.split("ether")[1].split()[0]
    except Exception as e:
        print(f"Error al obtener la dirección MAC actual: {e}")

def generate_random_mac():
    """Genera una MAC aleatoria."""
    mac = [0x00, 0x16, 0x3e,
           random.randint(0x00, 0x7f),
           random.randint(0x00, 0xff),
           random.randint(0x00, 0xff)]
    return ':'.join(map(lambda x: f"{x:02x}", mac))

def get_mac_by_manufacturer(manufacturer):
    """Genera una MAC basada en el fabricante (solo ejemplos, más se pueden agregar)."""
    mac_prefixes = {
        "Cisco": "00:40:96",
        "Intel": "00:1A:2B",
        "Dell": "00:14:22",
        "Apple": "00:1C:B3"
    }
    if manufacturer in mac_prefixes:
        return mac_prefixes[manufacturer] + ":%02x:%02x:%02x" % (
            random.randint(0x00, 0xff),
            random.randint(0x00, 0xff),
            random.randint(0x00, 0xff)
        )
    else:
        raise ValueError(f"Fabricante no reconocido: {manufacturer}")

def generate_mac_address(method_choice):
    """Genera una dirección MAC según el método elegido."""
    if method_choice == '1':
        return generate_random_mac()
    else:
        manufacturer_map = {1: "Cisco", 2: "Intel", 3: "Dell", 4: "Apple"}
        print(f"{Colors.YELLOW}Selecciona un fabricante (1-4):{Colors.RESET}")
        for key, value in manufacturer_map.items():
            print(f"{key}: {value}")
        manufacturer_choice = input_with_validation(
            f"{Colors.GREEN}Tu elección: {Colors.RESET}",
            lambda x: x.isdigit() and 1 <= int(x) <= 4,
            f"{Colors.RED}Por favor, selecciona un fabricante válido (1-4).{Colors.RESET}"
        )
        return get_mac_by_manufacturer(manufacturer_map[int(manufacturer_choice)])



def change_mac_and_ip(interface_name):
    """Cambia la dirección MAC y la IP de la interfaz especificada."""
    original_mac = get_current_mac(interface_name)
    print(f"{Colors.YELLOW}Dirección MAC original de {interface_name}: {original_mac}{Colors.RESET}")
    method_choice = input_with_validation(
        "Selecciona un método para generar la MAC (1: aleatoria, 2: fabricante): ",
        lambda x: x in ['1', '2'],
        "Por favor, selecciona una opción válida."
    )
    new_mac = generate_mac_address(method_choice)
    print(f"{Colors.GREEN}MAC generada: {new_mac}{Colors.RESET}")
    try:
        change_mac(interface_name, new_mac)
        print(f"{Colors.GREEN}Dirección MAC de {interface_name} cambiada a {new_mac}{Colors.RESET}")
    except subprocess.CalledProcessError as e:
        print(f"{Colors.RED}Error al cambiar la dirección MAC: {e}{Colors.RESET}")
        return
    suggested_ip = suggest_available_ip(interface_name)
    if suggested_ip:
        print(f"{Colors.YELLOW}Sugerencia de IP no ocupada: {suggested_ip}{Colors.RESET}")
    else:
        print(f"{Colors.RED}No se pudo encontrar una IP disponible automáticamente.{Colors.RESET}")
    new_ip = input_with_validation(
        f"Introduce la nueva dirección IP (ejemplo: {suggested_ip if suggested_ip else '192.168.0.10'}): ",
        is_valid_network,
        "Por favor, introduce una dirección IP válida."
    )
    try:
        change_ip(interface_name, new_ip)
        print(f"{Colors.GREEN}Dirección IP de {interface_name} cambiada a {new_ip}{Colors.RESET}")
    except subprocess.CalledProcessError as e:
        print(f"{Colors.RED}Error al cambiar la dirección IP: {e}{Colors.RESET}")

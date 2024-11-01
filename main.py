import os
import threading
from core.mac_changer import change_mac_and_ip, restore_mac_and_ip, get_current_mac
from core.interface_selector import list_network_interfaces, select_interface, print_available_interfaces
from utils.network_utils import get_interface_ip, get_subnet
from utils.input_validation import input_with_validation
from core.scan import scan_network
from core.user_activity import simulate_user_activity
from core.reporting import generate_report

# Colores para la terminal
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RESET = '\033[0m'

def check_root():
    """Verifica si el script se está ejecutando como root."""
    return os.geteuid() == 0

def configure_scan():
    """Configura y ejecuta el escaneo de red con opciones avanzadas."""
    scan_type = input_with_validation(
        "Selecciona el tipo de escaneo (1: Ping, 2: SYN, 3: TCP completo, 4: UDP): ",
        lambda x: x in ['1', '2', '3', '4'],
        "Por favor, selecciona una opción válida (1-4)."
    )
    scan_types_map = {'1': '-sP', '2': '-sS', '3': '-sT', '4': '-sU'}
    selected_scan_type = scan_types_map.get(scan_type, '-sT')

    if scan_type == '2' and not check_root():
        print(f"{Colors.RED}No tienes permisos de root. Cambiando a escaneo TCP completo (-sT).{Colors.RESET}")
        selected_scan_type = '-sT'
    
    ports = input("Introduce el rango de puertos a escanear (ejemplo: 1-1000) o presiona Enter para escanear todos: ")
    ports = ports if ports else "1-1000"

    # Opciones avanzadas de escaneo
    config = {
        "no_ping": False,
        "detect_os": False,
        "script_scan": False,
        "intensity_level": 2
    }
    advanced_options = input_with_validation(
        "¿Deseas configurar opciones avanzadas (sí/no)? ",
        lambda x: x.lower() in ['sí', 'si', 'no'],
        "Por favor, introduce 'sí' o 'no'."
    ).lower() in ["sí", "si"]

    if advanced_options:
        config["no_ping"] = input_with_validation(
            "¿Quieres desactivar el ping (sí/no)? ",
            lambda x: x.lower() in ['sí', 'si', 'no'],
            "Por favor, introduce 'sí' o 'no'."
        ).lower() in ["sí", "si"]
        
        config["detect_os"] = input_with_validation(
            "¿Deseas activar la detección de sistema operativo (sí/no)? ",
            lambda x: x.lower() in ['sí', 'si', 'no'],
            "Por favor, introduce 'sí' o 'no'."
        ).lower() in ["sí", "si"]
        
        config["script_scan"] = input_with_validation(
            "¿Quieres ejecutar scripts básicos (-sC) (sí/no)? ",
            lambda x: x.lower() in ['sí', 'si', 'no'],
            "Por favor, introduce 'sí' o 'no'."
        ).lower() in ["sí", "si"]
        
        config["intensity_level"] = int(input_with_validation(
            "Selecciona el nivel de intensidad (1: Muy sigiloso, 2: Sigiloso, 3: Normal, 4: Rápido): ",
            lambda x: x in ['1', '2', '3', '4'],
            "Por favor, selecciona una opción válida (1-4)."
        ))

    return selected_scan_type, ports, config

def main():
    print(f"{Colors.GREEN}Bienvenido a PhantomScan\n by Bacze{Colors.RESET}")
    
    interfaces = list_network_interfaces()
    if not interfaces:
        print(f"{Colors.RED}No se encontraron interfaces de red.{Colors.RESET}")
        return

    print_available_interfaces(interfaces)
    interface_name = select_interface(interfaces)
    original_mac = get_current_mac(interface_name)  # Obtener la MAC original
    original_ip = get_interface_ip(interface_name)  # Obtener la IP original
    subnet = get_subnet(interface_name)
    
    while True:
        action = input_with_validation("Selecciona acción (Cambiar MAC/IP = 'c', Escanear red = 'e', Salir = 's'): ", 
                                       lambda x: x.lower() in ['c', 'e', 's'],
                                       "Por favor, selecciona una opción válida (c, e, s).")

        if action == 'c':
            change_mac_and_ip(interface_name)
            print(f"{Colors.GREEN}MAC e IP cambiadas con éxito.{Colors.RESET}")
        elif action == 'e':
            # Configurar escaneo de red
            scan_type, ports, config = configure_scan()
            print(f"\n{Colors.YELLOW}Iniciando el escaneo en la subred {subnet}{Colors.RESET}")

            # Iniciar actividad simulada del usuario
            activity_thread = threading.Thread(target=simulate_user_activity)
            activity_thread.start()

            # Ejecutar el escaneo de red
            scan_results = scan_network(subnet, scan_type, ports, config["no_ping"], config["detect_os"], config["script_scan"], config["intensity_level"])
            
            # Generar el reporte si hay resultados
            if scan_results:
                generate_report(scan_results, report_format='html')
            else:
                print(f"{Colors.RED}No se encontraron resultados para generar el reporte.{Colors.RESET}")

            activity_thread.join()
        elif action == 's':
            # Preguntar si restaurar la MAC y la IP
            restore = input_with_validation(
                "¿Deseas restaurar la MAC y la IP originales (sí/no)? ",
                lambda x: x.lower() in ['sí', 'si', 'no'],
                "Por favor, introduce 'sí' o 'no'."
            ).lower()

            if restore in ["sí", "si"]:
                restore_mac_and_ip(interface_name, original_mac, original_ip)  # Llamar a la función para restaurar la MAC e IP
                print(f"{Colors.GREEN}MAC e IP restauradas a las originales.{Colors.RESET}")
            else:
                print(f"{Colors.YELLOW}Las configuraciones originales no se han restaurado.{Colors.RESET}")

            print(f"{Colors.YELLOW}Cerrando PhantomScan.{Colors.RESET}")
            break  # Sale del bucle y finaliza el programa

if __name__ == "__main__":
    if not check_root():
        print(f"{Colors.RED}Este script debe ejecutarse como root.{Colors.RESET}")
        exit(1)
    main()

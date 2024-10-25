import os
import threading
from core.mac_changer import change_mac_and_ip
from core.scan import scan_network
from core.interface_selector import list_network_interfaces, select_interface, print_available_interfaces
from utils.network_utils import get_interface_ip, is_valid_network
from core.user_activity import simulate_user_activity
from utils.input_validation import input_with_validation
from core.reporting import generate_report
from core.cve import correlacionar_resultados_escaneo  # Importar la nueva función

# Colores para la terminal
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RESET = '\033[0m'

def check_root():
    """Verifica si el script se está ejecutando como root."""
    return os.geteuid() == 0

def main():
    print(f"{Colors.GREEN}Bienvenido a PhantomScan{Colors.RESET}")
    interfaces = list_network_interfaces()
    if not interfaces:
        print(f"{Colors.RED}No se encontraron interfaces de red.{Colors.RESET}")
        return

    print_available_interfaces(interfaces)
    interface_name = select_interface(interfaces)
    try:
        change_mac_and_ip(interface_name)
    except Exception as e:
        print(f"{Colors.RED}Error al cambiar la MAC y la IP: {e}{Colors.RESET}")
        return

    current_ip = get_interface_ip(interface_name)
    if current_ip:
        suggested_subnet = f"{current_ip.rsplit('.', 1)[0]}.0/24"
        print(f"{Colors.YELLOW}Subred sugerida: {suggested_subnet}{Colors.RESET}")
    else:
        print(f"{Colors.RED}No se pudo sugerir una subred automáticamente.{Colors.RESET}")

    subnet = input_with_validation(
        "Introduce la subred a escanear (ejemplo: 192.168.218.0/24): ",
        lambda x: is_valid_network(x, is_subnet=True),
        "Por favor, introduce una subred válida."
    )

    print(f"{Colors.YELLOW}Selecciona el tipo de escaneo:{Colors.RESET}")
    scan_type = input_with_validation(
        "Selecciona el tipo de escaneo (1: Ping, 2: SYN, 3: TCP completo, 4: UDP): ",
        lambda x: x in ['1', '2', '3', '4'],
        "Por favor, selecciona una opción válida (1-4)."
    )

    scan_types_map = {'1': '-sP', '2': '-sS', '3': '-sT', '4': '-sU', '5': '-sV'}
    if scan_type == '2' and not check_root():
        print(f"{Colors.RED}No tienes permisos de root. Cambiando a escaneo TCP completo (-sT).{Colors.RESET}")
        scan_type = '3'

    ports = input("Introduce el rango de puertos a escanear (1-1000) o presiona Enter para escanear todos: ")

    activity_thread = threading.Thread(target=simulate_user_activity)
    activity_thread.start()

    scan_results = scan_network(subnet, scan_types_map[scan_type], ports)
    if scan_results:
        generate_report(scan_results)
        cves_encontradas = correlacionar_resultados_escaneo(scan_results)
        print(f"\n{Colors.YELLOW}=== CVEs Encontradas ==={Colors.RESET}")
        for cve in cves_encontradas:
            print(f"Host: {cve['host']}, Servicio: {cve['servicio']}, Versión: {cve['version']}, CVE: {cve['CVE']}, Descripción: {cve['descripción']}, Gravedad: {cve['gravedad']}")
    else:
        print(f"{Colors.RED}No se encontraron resultados para generar el reporte.{Colors.RESET}")

    activity_thread.join()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Programa interrumpido. Saliendo...")


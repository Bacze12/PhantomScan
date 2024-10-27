import subprocess
import ipaddress
import socket
import fcntl
import struct
import random

def change_ip(interface, new_ip, subnet):
    """Cambia la dirección IP de la interfaz especificada."""
    if not is_valid_ip_in_subnet(new_ip, subnet):
        print(f"[!] La IP {new_ip} no es válida o no pertenece a la subred {subnet}.")
        return
    subprocess.call(["sudo", "ifconfig", interface, new_ip])

def is_valid_ip_in_subnet(ip, subnet):
    """Verifica si la IP está dentro de la subred."""
    try:
        ip_obj = ipaddress.ip_address(ip)
        subnet_obj = ipaddress.ip_network(subnet, strict=True)
        return ip_obj in subnet_obj
    except ValueError:
        return False

def get_subnet(interface):
    """Obtiene la subred asociada a una interfaz de red."""
    try:
        result = subprocess.run(['ifconfig', interface], capture_output=True, text=True)
        ip_line = [line for line in result.stdout.splitlines() if 'inet ' in line]
        if ip_line:
            ip_address = ip_line[0].split()[1]
            subnet = ipaddress.IPv4Network(ip_address + '/24', strict=False)
            return str(subnet)
    except Exception as e:
        print(f"Error al obtener la subred: {e}")
    return None

def generate_ip_suggestions(subnet, exclude_ip=None):
    """Genera direcciones IP sugeridas dentro de una subred dada."""
    network = ipaddress.ip_network(subnet)
    potential_ips = [str(ip) for ip in network.hosts() if ip != exclude_ip and ip != network.network_address + 1]
    random.shuffle(potential_ips)
    return potential_ips[:10]

def suggest_available_ips(interface_name):
    """Sugiere direcciones IP no ocupadas en la red local."""
    subnet = get_subnet(interface_name)
    current_ip = get_interface_ip(interface_name)
    if subnet:
        potential_ips = generate_ip_suggestions(subnet, exclude_ip=current_ip)
        available_ips = []
        for ip in potential_ips:
            response = subprocess.run(['ping', '-c', '1', '-W', '1', ip], capture_output=True)
            if response.returncode != 0:
                available_ips.append(ip)
                if len(available_ips) == 3:
                    break
        return available_ips, subnet
    print(f"No se pudo obtener la subred para la interfaz {interface_name}.")
    return None, None

def get_interface_ip(interface_name):
    """Obtiene la IP asignada a la interfaz seleccionada."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        return socket.inet_ntoa(fcntl.ioctl(
            sock.fileno(),
            0x8915,
            struct.pack('256s', bytes(interface_name[:15], 'utf-8'))
        )[20:24])
    except IOError:
        return None

def is_valid_network(ip, subnet):
    """
    Valida si la IP proporcionada está dentro de la subred.
    """
    try:
        ip_obj = ipaddress.ip_address(ip)
        subnet_obj = ipaddress.ip_network(subnet, strict=False)
        return ip_obj in subnet_obj
    except ValueError:
        return False

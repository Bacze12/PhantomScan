import subprocess
import ipaddress
import socket
import fcntl
import struct

def change_ip(interface, new_ip):
    """Cambia la dirección IP de la interfaz especificada."""
    subprocess.call(["sudo", "ifconfig", interface, new_ip])

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

def generate_ip_suggestions(subnet):
    """Genera 3 direcciones IP sugeridas dentro de una subred dada."""
    network = ipaddress.IPv4Network(subnet)
    return [str(ip) for ip in list(network.hosts())[10:13]]  # Tomamos 3 IPs de ejemplo a partir de la 11

def suggest_available_ips(interface_name):
    """Sugiere tres direcciones IP no ocupadas en la red local."""
    ip = get_interface_ip(interface_name)
    if ip:
        subnet = ip.rsplit('.', 1)[0]  # Ejemplo: '192.168.0'
        suggested_ips = []  # Lista para almacenar IPs sugeridas
        for i in range(2, 255):
            suggested_ip = f"{subnet}.{i}"
            try:
                # Hacer un ping a la dirección IP para verificar si está ocupada
                response = subprocess.run(['ping', '-c', '1', suggested_ip], capture_output=True)
                if response.returncode != 0:  # No hay respuesta, IP no ocupada
                    suggested_ips.append(suggested_ip)
                    if len(suggested_ips) == 3:  # Solo necesitamos 3 IPs
                        break
            except Exception as e:
                print(f"Error al verificar IP {suggested_ip}: {e}")
    return suggested_ips



def get_interface_ip(interface_name):
    """Obtiene la IP asignada a la interfaz seleccionada."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        return socket.inet_ntoa(fcntl.ioctl(
            sock.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', bytes(interface_name[:15], 'utf-8'))
        )[20:24])
    except IOError:
        return None

def is_valid_network(network, is_subnet=False):
    """Valida si la IP o subred ingresada es válida."""
    try:
        if is_subnet:
            # Valida la subred, considerando que la entrada debe ser una red CIDR
            ipaddress.ip_network(network, strict=True)  # Strict=True asegura que es una red válida
        else:
            ipaddress.ip_address(network)  # Para IPs individuales
        return True
    except ValueError:
        return False

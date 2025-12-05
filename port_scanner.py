import socket
from common_ports import ports_and_services

def get_open_ports(target, port_range, verbose=False):

    start_port, end_port = port_range

    # Función auxiliar para detectar IPs
    def looks_like_ip(value):
        parts = value.split(".")
        return len(parts) == 4 and all(p.isdigit() for p in parts)

    ip = None
    hostname = None

    # ----------------------------------------
    # 1) Resolver y validar target
    # ----------------------------------------
    if looks_like_ip(target):
        # Parece IP → Validar formato
        try:
            socket.inet_aton(target)
            ip = target
        except:
            return "Error: Invalid IP address"

        # Reverse DNS si existe
        try:
            hostname = socket.gethostbyaddr(ip)[0]
        except:
            hostname = ip

    else:
        # Es hostname → resolver
        try:
            ip = socket.gethostbyname(target)
            hostname = target
        except:
            return "Error: Invalid hostname"

    # ----------------------------------------
    # 2) Escaneo de puertos
    # ----------------------------------------
    open_ports = []

    for port in range(start_port, end_port + 1):

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)

        result = sock.connect_ex((ip, port))
        sock.close()

        if result == 0:
            open_ports.append(port)

    # ----------------------------------------
    # 3) Modo verbose
    # ----------------------------------------
    if verbose:
        lines = []

        # Si target es IP sin hostname → no usar paréntesis
        if hostname == ip:
            lines.append(f"Open ports for {ip}")
        else:
            lines.append(f"Open ports for {hostname} ({ip})")

        lines.append("PORT     SERVICE")

        for port in open_ports:
            service = ports_and_services.get(port, "unknown")
            lines.append(f"{port:<9}{service}")

        return "\n".join(lines)

    return open_ports

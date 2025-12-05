import socket
from common_ports import ports_and_services

def get_open_ports(target, port_range, verbose=False):

    start_port, end_port = port_range

    def looks_like_ip(t):
        parts = t.split(".")
        return len(parts) == 4 and all(p.isdigit() for p in parts)

    ip = None
    hostname = None

    # -----------------------------
    # Resolver IP / hostname
    # -----------------------------
    if looks_like_ip(target):
        # validar IP
        try:
            socket.inet_aton(target)
        except:
            return "Error: Invalid IP address"

        ip = target

        # intentar reverse DNS
        try:
            hostname = socket.gethostbyaddr(ip)[0]
        except:
            hostname = ip

    else:
        # resolver hostname a IP
        try:
            ip = socket.gethostbyname(target)
            hostname = target
        except:
            return "Error: Invalid hostname"

    # -----------------------------
    # Escaneo
    # -----------------------------
    open_ports = []

    for port in range(start_port, end_port + 1):

        for _ in range(3):   # reintentos para evitar bloqueos
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.05)
                result = sock.connect_ex((ip, port))
                sock.close()

                if result == 0:
                    open_ports.append(port)
                    break

            except:
                pass

    # -----------------------------
    # Verbose
    # -----------------------------
    if verbose:

        if hostname == ip:
            header = f"Open ports for {ip}"
        else:
            header = f"Open ports for {hostname} ({ip})"

        out = [header, "PORT     SERVICE"]

        for port in open_ports:
            service = ports_and_services.get(port, "unknown")
            out.append(f"{port:<9}{service}")

        return "\n".join(out)

    return open_ports

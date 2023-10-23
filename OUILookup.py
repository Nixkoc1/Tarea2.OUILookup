import getopt
import sys
import ipaddress

# Base de datos OUI ficticia
OUI_DATABASE = {
    "b4:b5:fe": "Hewlett Packard",
    "98:06:3c": "Samsung Electronics Co.,Ltd",
    "00:01:97": "Cisco",
    "00:e0:64": "Samsung",
    "ac:f7:f3": "Xiomi"
}

# IP y máscara del host
HOST_IP = ipaddress.IPv4Interface("192.168.1.30/24")

# Función para obtener los datos de fabricación de una tarjeta de red por IP
def obtener_datos_por_ip(ip):
    try:
        # Convertir la cadena IP en un objeto IP
        ip_obj = ipaddress.IPv4Interface(ip + "/24")
        
        # Verificar si la IP está en la misma red que el host
        if ip_obj.network != HOST_IP.network:
            print("Error: ip is outside the host network")
            return
        
        # Asumir una MAC asociada ficticia para el ejemplo
        mac = "b4:b5:fe:92:ff:c5" if ip == "192.168.1.5" else None
        
        if mac is not None:
            oui = mac[:8]  # Se corrigió para mantener los dos puntos en el OUI
            fabricante = OUI_DATABASE.get(oui.lower(), "Not found")  # Se convirtió el OUI a minúsculas para la búsqueda
            print(f"MAC address : {mac}")
            print(f"Fabricante : {fabricante}")
        else:
            print("Error: MAC no encontrada para la IP")
    except ValueError:
        print("Error: IP inválida")

# Función para obtener los datos de fabricación de una tarjeta de red por MAC
def obtener_datos_por_mac(mac):
    try:
        # Buscar el fabricante en la base de datos OUI
        oui = mac[:8]  # Se corrigió para mantener los dos puntos en el OUI
        fabricante = OUI_DATABASE.get(oui.lower(), "Not found")  # Se convirtió el OUI a minúsculas para la búsqueda
        
        print(f"MAC address : {mac}")
        print(f"Fabricante : {fabricante}")
    except ValueError:
        print("Error: MAC inválida")


# Función para obtener la tabla ARP
# Función para obtener la tabla ARP
def obtener_tabla_arp():
    # Asumir una tabla ARP ficticia para el ejemplo
    tabla_arp = [
        ("192.168.1.1", "00:01:97:bb:bb:bb"),
        ("192.168.1.5", "b4:b5:fe:92:ff:c5"),
        ("192.168.1.17", "00:e0:64:aa:aa:aa"),
        ("192.168.1.29", "ac:f7:f3:aa:aa:aa")
    ]
    
    print("IP/MAC/Vendor:")
    for ip, mac in tabla_arp:
        fabricante = "Not found"
        for oui, nombre_fabricante in OUI_DATABASE.items():
            if mac.startswith(oui):
                fabricante = nombre_fabricante
                break
        print(f"{ip} / {mac} / {fabricante}")


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hi:m:a", ["help", "ip=", "mac=", "arp"])

    except getopt.GetoptError:
        print_help()
        sys.exit(2)

    if not opts:
        print_help()
        return

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print_help()
        elif opt in ("-i", "--ip"):
            obtener_datos_por_ip(arg)
        elif opt in ("-m", "--mac"):
            obtener_datos_por_mac(arg)
        elif opt in ("-a", "--arp"):
            obtener_tabla_arp()

def print_help():
    print("Use: python OUILookup.py --ip <IP> | --mac <MAC> | --arp | [--help]")
    print("\t--ip : IP del host a consultar.")
    print("\t--mac: MAC a consultar. P.e. aa:bb:cc:00:00:00.")
    print("\t--arp: muestra los fabricantes de los host disponibles en la tabla arp.")
    print("\t--help: muestra este mensaje y termina.")

if __name__ == "__main__":
    main(sys.argv[1:])


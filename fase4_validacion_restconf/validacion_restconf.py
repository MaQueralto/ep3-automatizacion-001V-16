import requests
import yaml
import json
import socket
from datetime import datetime
from requests.adapters import HTTPAdapter

# Deshabilitar warnings SSL
requests.packages.urllib3.disable_warnings()

# Metadatos
print("=" * 50)
print("Script  : validacion_restconf.py")
print(f"Fecha   : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Host    : {socket.gethostname()}")
print("=" * 50)

# Cargar variables
with open("../vars/vars_001V-16.yaml") as f:
    vars = yaml.safe_load(f)

base_url = f"https://{vars['router']['ip']}/restconf/data"
auth = (vars["router"]["usuario"], vars["router"]["password"])
headers = {
    "Accept": "application/yang-data+json",
    "Content-Type": "application/yang-data+json"
}

session = requests.Session()
session.verify = False
session.auth = auth
session.headers.update(headers)

def get_endpoint(url, filename):
    r = session.get(url, timeout=30)
    data = r.json()
    with open(f"evidencias/responses/{filename}", "w") as f:
        json.dump(data, f, indent=2)
    return data

# Consultas
print("\nConsultando endpoints RESTCONF...")

h = get_endpoint(f"{base_url}/Cisco-IOS-XE-native:native/hostname", "get_hostname.json")
l = get_endpoint(f"{base_url}/ietf-interfaces:interfaces/interface=Loopback16", "get_loopback.json")
i = get_endpoint(f"{base_url}/ietf-interfaces:interfaces/interface=GigabitEthernet1", "get_interfaces.json")
n = get_endpoint(f"{base_url}/Cisco-IOS-XE-native:native/ntp", "get_ntp.json")

# Extraer valores
hostname = h.get("Cisco-IOS-XE-native:hostname", "")

loopback_data = l.get("ietf-interfaces:interface", {})
ipv4_addr = loopback_data.get("ietf-ip:ipv4", {}).get("address", [{}])[0]
loopback_ip = ipv4_addr.get("ip", "")

interface_data = i.get("ietf-interfaces:interface", {})
desc_wan = interface_data.get("description", "")

ntp_data = n.get("Cisco-IOS-XE-native:ntp", {})
ntp_servers = ntp_data.get("Cisco-IOS-XE-ntp:server", {}).get("server-list", [{}])
ntp_ip = ntp_servers[0].get("ip-address", "") if ntp_servers else ""

# Comparar
expected = {
    "hostname": vars["cliente"]["hostname"],
    "loopback_ip": vars["router"]["loopback_ip"],
    "descripcion_wan": vars["router"]["descripcion_wan"],
    "ntp_server": vars["router"]["ntp_server"]
}

got = {
    "hostname": hostname,
    "loopback_ip": loopback_ip,
    "descripcion_wan": desc_wan,
    "ntp_server": ntp_ip
}

print("\n--- REPORTE DE VALIDACION RESTCONF ---")
ok_count = 0
for key in expected:
    status = "[OK]" if got[key] == expected[key] else "[FAIL]"
    if got[key] == expected[key]:
        ok_count += 1
    print(f"{status} {key}: obtenido='{got[key]}' esperado='{expected[key]}'")

print(f"\nResultado: {ok_count}/4 criterios conformes")
print("CONFORME" if ok_count == 4 else "NO CONFORME")

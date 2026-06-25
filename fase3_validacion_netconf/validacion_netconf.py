import sys
import yaml
from datetime import datetime
from ncclient import manager
from lxml import etree

# Metadatos
print("=" * 50)
print("Script  : validacion_netconf.py")
print(f"Fecha   : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
import socket
print(f"Host    : {socket.gethostname()}")
print("=" * 50)

# Cargar variables
with open("../vars/vars_001V-16.yaml") as f:
    vars = yaml.safe_load(f)

# Valores esperados
expected = {
    "hostname": vars["cliente"]["hostname"],
    "loopback_ip": vars["router"]["loopback_ip"],
    "loopback_mask": vars["router"]["loopback_mask"],
    "descripcion_wan": vars["router"]["descripcion_wan"],
    "ntp_server": vars["router"]["ntp_server"]
}

# Filtro NETCONF
filter_xml = """
<filter>
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    <hostname/>
    <interface>
      <GigabitEthernet>
        <name>1</name>
        <description/>
      </GigabitEthernet>
      <Loopback>
        <name>16</name>
        <ip/>
      </Loopback>
    </interface>
    <ntp>
      <server xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-ntp">
        <server-list/>
      </server>
    </ntp>
  </native>
</filter>
"""

# Conectar
with manager.connect(
    host=vars["router"]["ip"],
    port=830,
    username=vars["router"]["usuario"],
    password=vars["router"]["password"],
    hostkey_verify=False,
    allow_agent=False,
    look_for_keys=False
) as m:
    response = m.get_config(source="running", filter=filter_xml)
    raw_xml = response.xml

    # Guardar XML crudo
    with open("evidencias/rpc_reply_raw.xml", "w") as f:
        f.write(raw_xml)
    print("XML guardado en evidencias/rpc_reply_raw.xml")

    # Parsear
    root = etree.fromstring(raw_xml.encode())
    ns = {"ios": "http://cisco.com/ns/yang/Cisco-IOS-XE-native",
          "ntp": "http://cisco.com/ns/yang/Cisco-IOS-XE-ntp"}

    def get_text(xpath):
        r = root.find(xpath, ns)
        return r.text if r is not None else None

    hostname = get_text(".//ios:native/ios:hostname")
    loopback_ip = get_text(".//ios:Loopback/ios:ip/ios:address/ios:primary/ios:address")
    loopback_mask = get_text(".//ios:Loopback/ios:ip/ios:address/ios:primary/ios:mask")
    desc_wan = get_text(".//ios:GigabitEthernet/ios:description")
    ntp = get_text(".//ntp:server-list/ntp:ip-address")

    # Comparar
    results = {
        "hostname": (hostname, expected["hostname"]),
        "loopback_ip": (loopback_ip, expected["loopback_ip"]),
        "loopback_mask": (loopback_mask, expected["loopback_mask"]),
        "descripcion_wan": (desc_wan, expected["descripcion_wan"]),
        "ntp_server": (ntp, expected["ntp_server"])
    }

    print("\n--- REPORTE DE VALIDACION NETCONF ---")
    ok_count = 0
    for key, (got, exp) in results.items():
        status = "[OK]" if got == exp else "[FAIL]"
        if got == exp:
            ok_count += 1
        print(f"{status} {key}: obtenido='{got}' esperado='{exp}'")

    print(f"\nResultado: {ok_count}/5 criterios conformes")
    print("CONFORME" if ok_count == 5 else "NO CONFORME")

import yaml
from datetime import datetime

with open("../vars/vars_001V-16.yaml") as f:
    vars = yaml.safe_load(f)

netconf_ok = False
restconf_ok = False

try:
    with open("../fase3_validacion_netconf/evidencias/output_validacion_netconf.txt") as f:
        content = f.read()
        netconf_ok = "CONFORME" in content and "5/5" in content
except:
    pass

try:
    with open("../fase4_validacion_restconf/evidencias/output_validacion_restconf.txt") as f:
        content = f.read()
        restconf_ok = "CONFORME" in content and "4/4" in content
except:
    pass

resultado = "CONFORME" if (netconf_ok and restconf_ok) else "NO CONFORME"

cert = f"""
==================================================
   CERTIFICADO DE COMPLIANCE — EP3
==================================================
Alumno  : {vars['alumno']['nombre']}
Codigo  : {vars['alumno']['codigo']}
Empresa : {vars['cliente']['empresa']}
Router  : {vars['cliente']['hostname']}
Fecha   : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
==================================================
VALIDACION NETCONF  : {"CONFORME" if netconf_ok else "NO CONFORME"}
VALIDACION RESTCONF : {"CONFORME" if restconf_ok else "NO CONFORME"}
--------------------------------------------------
RESULTADO GLOBAL    : {resultado}
==================================================
El equipo {vars['cliente']['hostname']} ha sido configurado
y validado exitosamente para {vars['cliente']['empresa']}.
Listo para operar en produccion.
==================================================
"""

print(cert)

with open(f"evidencias/certificado_compliance_001V-16.txt", "w") as f:
    f.write(cert)

print("Certificado guardado en evidencias/certificado_compliance_001V-16.txt")

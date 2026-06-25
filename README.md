# EP3 — Automatización de Red con Compliance Auditado

**Alumno:** Matias Queralto | **Código:** 001V-16  
**Empresa cliente:** Infraestructura Vial SpA  
**Router:** RTR-INFVIAL

---

## 1. Objetivo del proyecto

Se implementó la automatización completa de incorporación del router RTR-INFVIAL a la red corporativa de Infraestructura Vial SpA. El objetivo fue ejecutar el ciclo completo de aprovisionamiento automatizado, validación independiente y generación de un certificado de compliance que certifique que el equipo está listo para operar.

## 2. Alcance

Se configuró hostname corporativo, interfaz Loopback de gestión, descripción WAN, banner de acceso, servidor NTP, y se habilitaron los servicios NETCONF y RESTCONF. No se configuraron protocolos de enrutamiento dinámico ni políticas de seguridad avanzadas. Las herramientas utilizadas fueron pyATS/Genie, Ansible, ncclient y requests sobre la VM DEVASC conectada al CSR1kv.

## 3. Infraestructura utilizada

| Componente | Detalle |
|---|---|
| Estación de trabajo | DEVASC VM — Ubuntu, hostname labvm |
| Router | Cisco CSR1000V — IOS XE 16.9.5 |
| IP de gestión | 192.168.56.101 |
| Loopback | 10.1.16.1/24 |
| Hypervisor | Oracle VirtualBox |

## 4. Tecnologías empleadas y justificación

- **pyATS/Genie:** Usado en Fase 1 y 5 para capturar el estado del router antes y después del aprovisionamiento, permitiendo comparación objetiva del cambio.
- **Ansible:** Usado en Fase 2 por su capacidad de aplicar configuración de forma idempotente y reproducible usando playbooks declarativos.
- **NETCONF (ncclient):** Usado en Fase 3 para validación independiente vía protocolo estándar XML/YANG, accediendo al árbol completo de configuración.
- **RESTCONF (requests):** Usado en Fase 4 para validación mediante consultas HTTP/JSON a recursos específicos, complementando la validación NETCONF.

## 5. Configuración aplicada

| Parámetro | Valor |
|---|---|
| Hostname | RTR-INFVIAL |
| Loopback IP | 10.1.16.1 |
| Máscara Loopback | 255.255.255.0 |
| Descripción WAN | Enlace-WAN-Punta-Arenas |
| Banner | ACCESO RESTRINGIDO - INFVIAL |
| NTP Server | 208.67.222.222 |
| NETCONF | Habilitado (puerto 830) |
| RESTCONF | Habilitado (HTTPS) |

## 6. Resultados de validación

| Criterio | NETCONF | RESTCONF |
|---|---|---|
| Hostname | CONFORME | CONFORME |
| IP Loopback | CONFORME | CONFORME |
| Descripción WAN | CONFORME | CONFORME |
| Servidor NTP | CONFORME | CONFORME |
| Máscara Loopback | CONFORME | — |

## 7. Conclusiones

El router RTR-INFVIAL fue incorporado exitosamente a la red corporativa de Infraestructura Vial SpA. Los 5 criterios NETCONF y 4 criterios RESTCONF resultaron CONFORMES. El equipo fue entregado a operaciones con toda la configuración corporativa aplicada y verificada de forma independiente mediante dos protocolos distintos.

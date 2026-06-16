## Prefacio

### Confidencialidad, Copyright y Responsabilidad
Este documento contiene información confidencial que es para uso exclusivo de Red Hat ©, Inc y {{ client }}, copyright 2025 Red Hat, Inc. Todos los derechos reservados; y no debe compartirse con  personas que no pertenezcan a estas dos empresas. Este documento y cualquier parte del mismo no pueden copiarse, reproducirse, fotocopiarse, almacenarse electrónicamente en un sistema de recuperación, o transmitido de otro modo sin el consentimiento expreso por escrito de Red Hat. Red Hat no garantiza que este documento esté libre de errores u omisiones. Red Hat se reserva el derecho de realizar correcciones, actualizaciones, revisiones o cambios a la información aquí contenida.

### Introducción
El Launch Team es un equipo de expertos dedicados a la adopción de Red Hat Cloud Services. Compuesto por profesionales conocidos como Specialist Adoption Architects (SAA), este equipo está disponible para clientes estratégicos y seleccionados en América Latina. Nuestra misión es acelerar la adopción de servicios administrados de Red Hat como ARO, ROSA y OSD, garantizando que los clientes que sean elegibles y que ya hayan optado por estas tecnologías, cuenten con todo el apoyo necesario. El SAA será responsable de maximizar el valor de estas soluciones, proporcionando un proceso de adopción ágil, eficiente y sin complicaciones. El soporte ofrecido va desde recomendar arquitecturas de referencia hasta indicar la mejores prácticas y otras orientaciones estratégicas, garantizando que los clientes aprovechen al máximo los beneficios de Servicios administrados de Red Hat

### Sobre este documento
El propósito de este documento es informar los resultados de la ejecución del chequeo de salud realizado en la plataforma instalada de {{ client }}.

### Audiencia
Este documento está dirigido a administradores de sistemas, arquitectos y desarrolladores de {{ client }}.

### Nomenclatura de Checklist
| Imagen | Explicación |
|-------|-------------|
| :white_check_mark: | Pasa la revisión, no existen comentarios |
| :warning: | Existen comentarios sobre los resultados obtenidos |
| :negative_squared_cross_mark:{ .color_red }  | No pasa la revisión, se entregan recomendaciones  |

### Terminología
| Sigla | Significado |
|-------|-------------|
| SAA | Specialist Adoption Architect |
| OCP | Openshift Container Platform |
| ACS | Advanced Cluster Security  |
| ACM | Advanced Cluster Management  |
| ARO | Azure RedHat Openshift  |
| ROSA | Red Hat OpenShift on AWS |
| OSD | OpenShift Dedicated |
| DNS | Domain Name System |
| API | Application Programming Interface |
| DHCP | Dynamic Host Configuration Protocol |
| FQDN | Fully Qualified Domain Name |
| PV | Persistent Volume |
| PVC | Persistent Volume Claim |
| AZ | Availability Zone |
| CAS | Cluster Auto Scaling |
| HPA | Horizontal Pod Autoscaling |
| VPA | Vertical Pod Autoscaling |

### Análisis y Recomendaciones de Arquitectura
![current architecture](img/architecture.png)
# ISW2_Proyecto_Asistencias

## Problema a resolver

El sistema actual de marcaje y registro de horas trabajadas presenta múltiples problemas, especialmente en cuanto a la precisión del registro de turnos y horas trabajadas a lo largo del mes. Estos errores se ven amplificados por el gran volumen de trabajadores, lo que complica aún más el proceso de depuración de los datos de asistencia. Actualmente, esta depuración se realiza manualmente por el personal del área de Gestión de Personas, lo que supone una significativa inversión de tiempo.

## Propuesta

Se plantea una propuesta de software para optimizar el proceso de registro de asistencia que permita una integración eficiente con el Sistema de Información de Recursos Humanos (SIRH), reduciendo así errores y mejorando la eficiencia operativa. 
Detectando el mismo día del registro los marcajes duplicados, falta de marcaje de salida, entre otros.

---
### Carpetas:

* Documentación: Historial de propuestas, respuestas de clientes, diagramas, definiciones, y cartas Gantt de desarrollo y entregas en forma de PDF's.
* Templates: archivos HTML de las distintas páginas.
* static: Imagenes/iconos/logos.
* temp: Se usa durante el funcionamiento del sistema para guardar archivos temporales. Son eliminados al terminar la ejecución.
* horario_mensual: Directorio con volumen declarado en docker-compose. Se usa para guardar las reglas de horarios creados. Se actualiza cada mes.

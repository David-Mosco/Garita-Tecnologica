# Documento del Proyecto

## Introducción
El Sistema de Control de Ingreso para Garita Tecnológica Residencial digitaliza el registro de visitantes, vehículos, viviendas y vecinos. El sistema mejora la trazabilidad, reduce registros manuales y permite notificar por correo electrónico al vecino cuando llega una visita.

## Problema
En muchas garitas residenciales el control se lleva en papel, lo que provoca poca trazabilidad, errores al asociar visitas con viviendas y falta de notificación oportuna al vecino.

## Objetivo general
Desarrollar una aplicación web con FastAPI, PostgreSQL y frontend web para registrar visitantes, notificar al vecino por correo y gestionar accesos mediante código único o código QR.

## Objetivos específicos
- Registrar visitantes y vehículos.
- Asociar cada visita a una vivienda y vecino.
- Generar código único por vecino.
- Permitir prerregistro con QR.
- Consultar placas vehiculares.
- Mantener historial de entradas y salidas.
- Aplicar roles de seguridad.

## Requerimientos funcionales cubiertos
1. Login por rol.
2. Registro de vecinos.
3. Código único generado automáticamente.
4. Registro de viviendas.
5. Registro de visitantes.
6. Ingreso sin prerregistro.
7. Prerregistro con QR.
8. Validación de QR.
9. Almacenamiento en PostgreSQL.
10. Envío o simulación correcta de correo.
11. Consulta de placas.
12. Historial de entradas y salidas.
13. Roles: administrador, agente y vecino.
14. Dashboard y auditoría como extras.

## Reglas de negocio
- Cada vecino tiene un código único irrepetible.
- No se registra visita sin vivienda o código válido.
- El QR solo funciona dentro de su rango de vigencia.
- Toda visita genera notificación al vecino.
- Toda salida queda registrada.
- El agente no elimina historial.
- El administrador consulta todo el historial.

## Casos de uso
- Registrar visita normal.
- Registrar visita con QR.
- Generar prerregistro.
- Recibir notificación.
- Consultar placa.
- Registrar salida.

## Diagrama de base de datos
Ver `docs/diagrama_bd_mermaid.md`.

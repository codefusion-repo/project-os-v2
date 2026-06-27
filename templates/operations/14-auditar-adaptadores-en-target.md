# Auditar Adaptadores en Target

## Objetivo de la Operación
Inspeccionar las plantillas y archivos del kernel en un proyecto target para asegurar que no han sufrido 'drift' o modificaciones invasivas.

## Detalle de Comportamiento
- **Qué fuentes lee en vivo**: Directorio .github/, AGENTS.md, docs de adopción en target.
- **Qué compara/decide**: Adaptador actual vs modelo canónico de este repositorio.
- **Qué entrega (Output)**: Reporte descriptivo de drift y fallos estructurales (read-only).
- **Qué NO debe hacer (Límites)**: No aplica arreglos por sí mismo. (Eso sería upgrade).

## Propiedad de Superficie (Surface)
**Primaria: `terminal_agent` (ejecutando script de auditoría read-only).**

## Configuración Canónica (Kernel)
- **Workflow**: `workflow.review_only`
- **Execution Mode**: `mode.review_only`
- **Output Contract**: `output.status_result`
- **Evidence Required**: `evidence.repo_state`

## Variables PM
- **Requeridas**: `TARGET_REPOSITORY`
- **Opcionales**: `Ninguna`
- **Inferidas (Contexto)**: Estado del adaptador

## Placeholders PM (para templates de uso manual)
- <TARGET_REPOSITORY>

## Ejemplo de Invocación
```
14-auditar-adaptadores-en-target.md
TARGET_REPOSITORY=VALOR_AQUI
```

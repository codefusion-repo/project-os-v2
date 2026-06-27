# Verificar Adopción en Repositorio Target

## Objetivo de la Operación
Auditar un repositorio para confirmar que las reglas de Project OS están correctamente instaladas y referencian al kernel actual.

## Detalle de Comportamiento
- **Qué fuentes lee en vivo**: Archivos del target (AGENTS.md, etc.)
- **Qué compara/decide**: Busca desviaciones entre el adaptador del target y el kernel canónico.
- **Qué entrega (Output)**: Reporte de hallazgos y estado de la adopción.
- **Qué NO debe hacer (Límites)**: No aplica mutaciones al target. Es solo lectura.

## Propiedad de Superficie (Surface)
**Primaria: `browser_chat` o `terminal_agent` (read-only audit).**

## Configuración Canónica (Kernel)
- **Workflow**: `workflow.target_adoption`
- **Execution Mode**: `mode.review_only`
- **Output Contract**: `output.status_result`
- **Evidence Required**: `evidence.target_adoption`

## Variables PM
- **Requeridas**: `TARGET_REPOSITORY`
- **Opcionales**: `Ninguna`
- **Inferidas (Contexto)**: Estado del código en target

## Placeholders PM (para templates de uso manual)
- <TARGET_REPOSITORY>

## Ejemplo de Invocación
```
03-verificar-adopcion-en-repositorio-target.md
TARGET_REPOSITORY=VALOR_AQUI
```

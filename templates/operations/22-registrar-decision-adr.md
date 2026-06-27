# Registrar Decisión Arquitectural (ADR)

## Objetivo de la Operación
Generar y proponer formalmente la inclusión de un Architecture Decision Record cuando una elección trasciende el alcance de un issue efímero.

## Detalle de Comportamiento
- **Qué fuentes lee en vivo**: El debate del issue y la DECISION técnica tomada por el PM o equipo.
- **Qué compara/decide**: Formaliza el contexto, alternativas y la justificación final de la solución elegida.
- **Qué entrega (Output)**: Ejecución o borrador del archivo `decisiones ADR`.
- **Qué NO debe hacer (Límites)**: No se usa para guardar 'estado vivo' de qué issues están abiertos. Solo decisiones perennes de diseño.

## Propiedad de Superficie (Surface)
**Primaria: `terminal_agent` (crea PR con ADR si se delega) o `browser_chat` (draftea contenido).**

## Configuración Canónica (Kernel)
- **Workflow**: `workflow.pm_intake`
- **Execution Mode**: `mode.delegated_commit_pr`
- **Output Contract**: `output.execution_report`
- **Evidence Required**: `evidence.repo_state`

## Variables PM
- **Requeridas**: `DECISION`
- **Opcionales**: `Ninguna`
- **Inferidas (Contexto)**: Template estándar de ADR

## Placeholders PM (para templates de uso manual)
- <DECISION>

## Ejemplo de Invocación
```
22-registrar-decision-adr.md
DECISION=VALOR_AQUI
```

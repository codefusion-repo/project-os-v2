# Registrar Decisión Arquitectural (ADR)

## Objetivo de la Operación
Generar y proponer formalmente la inclusión de un Architecture Decision Record cuando una elección trasciende el alcance de un issue efímero.

## Detalle de Comportamiento
- **Qué fuentes lee en vivo**: El debate del issue y la DECISION técnica tomada por el PM o equipo.
- **Qué compara/decide**: Formaliza el contexto, alternativas y la justificación final de la solución elegida.
- **Qué entrega (Output)**: El contenido del ADR drafteado y, si el PM decide escribir el archivo, un `output.route_prompt` que delega la creación del archivo ADR a un terminal agent. El browser chat no escribe archivos.
- **Qué NO debe hacer (Límites)**: No se usa para guardar 'estado vivo' de qué issues están abiertos; solo decisiones perennes de diseño. La escritura del archivo ADR requiere route-prompt + `mode.delegated_commit_pr` + aprobación PM exacta. El terminal agent no tiene autoridad de planeación/review más allá del route-prompt scoped.

## Propiedad de Superficie (Surface)
**Primaria: `browser_chat` (draftea el contenido del ADR y, si se debe escribir el archivo, el route-prompt). Secundaria: `terminal_agent` (ejecutor del archivo ADR solo bajo route-prompt + `mode.delegated_commit_pr` + aprobación PM exacta).**

## Configuración Canónica (Kernel)
- **Workflow**: `workflow.pm_intake`
- **Execution Mode**: `mode.review_only`
- **Output Contract**: `output.route_prompt`
- **Evidence Required**: `evidence.source_basis`

## Variables PM
- **Requeridas**: `DECISION`
- **Opcionales**: `Ninguna`
- **Inferidas (Contexto)**: Template estándar de ADR (`templates/artifacts.md`)

## Placeholders PM (para templates de uso manual)
- <DECISION>

## Ejemplo de Invocación
```
22-registrar-decision-adr.md
DECISION=VALOR_AQUI
```

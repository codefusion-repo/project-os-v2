# Draftear Comando Crear Follow Up desde Review

## Objetivo de la Operación
Extraer findings menores no bloqueantes encontrados durante un review de PR, para aislarlos en un nuevo issue a resolver luego.

## Detalle de Comportamiento
- **Qué fuentes lee en vivo**: Findings, reviews incompletos, notas de out-of-scope.
- **Qué compara/decide**: Diferencia un issue bloqueante (corrección inmediata) de uno diferido (follow-up).
- **Qué entrega (Output)**: PM command bundle para generar el nuevo issue, sin detener el merge actual.
- **Qué NO debe hacer (Límites)**: No asume que se deben ignorar problemas de seguridad.

## Propiedad de Superficie (Surface)
**Primaria: `browser_chat` (draftea bundle).**

## Configuración Canónica (Kernel)
- **Workflow**: `workflow.pm_intake`
- **Execution Mode**: `mode.review_only`
- **Output Contract**: `output.pm_command_bundle`
- **Evidence Required**: `evidence.source_basis`

## Variables PM
- **Requeridas**: `PR_NUMBER`
- **Opcionales**: `Ninguna`
- **Inferidas (Contexto)**: Comentarios de review

## Placeholders PM (para templates de uso manual)
- <PR_NUMBER>

## Ejemplo de Invocación
```
21-draftear-comando-crear-follow-up-desde-review.md
PR_NUMBER=VALOR_AQUI
```

# Solicitar Revisión de Seguridad OWASP

## Objetivo de la Operación
Crear un prompt o instrucción para someter cambios sensibles (auth, roles) a un chequeo de un auditor de seguridad o agente dedicado a OWASP.

## Detalle de Comportamiento
- **Qué fuentes lee en vivo**: Diff de PR_NUMBER con componentes sensibles.
- **Qué compara/decide**: Detecta zonas de riesgo, inyecciones y validación de entrada.
- **Qué entrega (Output)**: Prompt de auditoría formal (`output.security_review_prompt`).
- **Qué NO debe hacer (Límites)**: No expone secretos reales; exige redacción (redaction). No aprueba código inseguro.

## Propiedad de Superficie (Surface)
**Primaria: `browser_chat` (draftea revisión experta).**

## Configuración Canónica (Kernel)
- **Workflow**: `workflow.pm_intake`
- **Execution Mode**: `mode.review_only`
- **Output Contract**: `output.security_review_prompt`
- **Evidence Required**: `evidence.repo_state`

## Variables PM
- **Requeridas**: `PR_NUMBER`
- **Opcionales**: `Ninguna`
- **Inferidas (Contexto)**: Áreas críticas del código

## Placeholders PM (para templates de uso manual)
- <PR_NUMBER>

## Ejemplo de Invocación
```
20-solicitar-revision-de-seguridad-owasp.md
PR_NUMBER=VALOR_AQUI
```

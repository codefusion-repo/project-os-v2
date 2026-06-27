# Solicitar Assets de Diseño Externos

## Objetivo de la Operación
Draftear una solicitud de especificaciones, mocks o imágenes a un destinatario humano de diseño, en base a lo requerido en una feature.

## Detalle de Comportamiento
- **Qué fuentes lee en vivo**: DESCRIPTION de la característica de UI.
- **Qué compara/decide**: Determina qué medidas, formatos y resoluciones son necesarios para la UI.
- **Qué entrega (Output)**: Output prompt o correo/mensaje estructurado.
- **Qué NO debe hacer (Límites)**: No asume la creación autónoma de imágenes si no está el tool adecuado. Es comunicación externa.

## Propiedad de Superficie (Surface)
**Primaria: `browser_chat` (draftea). Destinatario: Diseño externo.**

## Configuración Canónica (Kernel)
- **Workflow**: `workflow.pm_intake`
- **Execution Mode**: `mode.review_only`
- **Output Contract**: `output.asset_prompt`
- **Evidence Required**: `evidence.repo_state`

## Variables PM
- **Requeridas**: `DESCRIPTION`
- **Opcionales**: `Ninguna`
- **Inferidas (Contexto)**: Restricciones de UI del repositorio

## Placeholders PM (para templates de uso manual)
- <DESCRIPTION>

## Ejemplo de Invocación
```
19-solicitar-assets-de-diseno-externos.md
DESCRIPTION=VALOR_AQUI
```

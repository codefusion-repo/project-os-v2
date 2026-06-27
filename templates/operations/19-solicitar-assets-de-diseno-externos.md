# Solicitar Assets de Diseño Externos

## Objetivo de la Operación
Draftear una solicitud de especificaciones, mocks o imágenes a un destinatario humano de diseño, en base a lo requerido en una feature.

## Detalle de Comportamiento
- **Qué fuentes lee en vivo**: DESCRIPTION de la característica de UI.
- **Qué compara/decide**: Determina qué medidas, formatos y resoluciones son necesarios para la UI.
- **Qué entrega (Output)**: Un `output.asset_prompt`: prompt/instrucciones compactas para un destinatario real de diseño.
- **Qué NO debe hacer (Límites)**: No genera imágenes ni crea archivos de asset; la verdad de producto/diseño permanece en el repositorio target o en la evidencia provista por el PM. Redacta cualquier valor sensible como `[REDACTED]`. Es comunicación externa a un destinatario de diseño, que NO es un actor.

## Propiedad de Superficie (Surface)
**Primaria: `browser_chat` (draftea el prompt). Destinatario: especialista de diseño externo (recipiente, no actor).**

## Configuración Canónica (Kernel)
- **Workflow**: `workflow.design_asset`
- **Execution Mode**: `mode.review_only`
- **Output Contract**: `output.asset_prompt`
- **Evidence Required**: `evidence.repo_state, evidence.source_basis`

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

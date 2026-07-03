# ADR 0001 — Fase 5 deploy execution: local/staging applied, production fail-closed

- Estado: Aceptado (resuelve el issue #376; MOSDLC.6a).
- Alcance: MOS-5.11 execute-local-deploy, MOS-5.13 execute-staging-deploy,
  MOS-5.15 execute-production-deploy.
- Base fuente: roadmap #274; issue #374 y PR #375 (migración MOSDLC.6 de Fase 5);
  `docs/MOSDLC_OPERATION_MAP.md` sección "Candidatos de cambio de kernel";
  `kernel/*.json`.
- No-autorización: este ADR documenta una decisión durable; no otorga permiso de
  escritura, deploy, merge, cierre ni settings (`boundary.output_not_permission`).
  La autoridad viene solo de aprobación PM exacta más los gates del kernel.

## Contexto

La migración de Fase 5 (issue #374 / PR #375) preservó MOS-5.11, MOS-5.13 y
MOS-5.15 como candidatos `kernel:candidate` de ejecución de despliegue por
terminal agent, sin comportamiento de deploy, ids de kernel ni autoridad. El
mapa registró tres candidatos de cambio de kernel diferidos. El issue #376 pide
resolverlos antes de Fase 6. La dirección PM fue agregar el soporte de kernel,
no diferirlo, con producción reservada al Humano PM.

## Decisión

Se agregan tres ids de kernel mínimos, con gap estricto probado y aprobación PM
exacta, y se aplican solo a ejecución interna local y staging por terminal
agent:

- `workflow.deployment`: workflow de ejecución de despliegue interno para un
  entorno aprobado (local o staging), que corre solo comandos target-owned,
  falla cerrado y verifica post-deploy.
- `mode.delegated_deploy_execution`: execution mode write-capable, terminal-only,
  que ejecuta solo comandos target-owned del entorno aprobado; nunca edita repo,
  hace commit/push/PR, inventa comandos, expone o pide secretos, ni corre
  broad environment/config dumps.
- `evidence.deployment_readiness`: evidencia de readiness de entorno que falla
  cerrado a `status.blocked` cuando faltan comandos target-owned, alcance de
  entorno, readiness o secret-safety.

Aplicación por fila:

- MOS-5.11 (local) y MOS-5.13 (staging): ejecutables por terminal agent bajo
  `workflow.deployment` + `mode.delegated_deploy_execution`, internal-only.
- MOS-5.15 (producción): NO ejecutada por agente. Producción queda con el
  Humano PM por defecto; `mode.delegated_deploy_execution` prohíbe la ejecución
  de producción. Es la fila más estricta.

## Modelo de seguridad

- Internal-only y nunca public-safe por defecto; convertir/ocultar/remover antes
  de un release público (`pre-release:convert`).
- Requiere aprobación PM exacta por target repository, entorno y acción; nunca
  implícita.
- Solo comandos target-owned documentados en las `Project-specific notes` del
  target; nunca se inventan comandos.
- Falla cerrado cuando faltan comandos target-owned, alcance de entorno,
  aprobación exacta, `evidence.deployment_readiness`, `evidence.target_adoption`,
  `evidence.validation_output` o secret-safety.
- Producción es más estricta que local/staging y queda con el Humano PM por
  defecto; una ruta de producción por agente requeriría un gate más estricto,
  aprobado y testeado por separado, y no existe aún.
- Este issue no ejecutó ningún comando de despliegue al resolverse.

## Secret-safety

Nunca se solicitan ni imprimen valores secretos: `.env`, tokens, credenciales,
cookies, JWTs, database URLs, CI secrets, private keys, production credentials,
payment-provider keys ni OAuth/client secrets. Los valores sensibles se redactan
como `[REDACTED]` y solo se reportan nombres de variable, nombres de comando,
rutas de archivo y tipos de riesgo. No se ejecutan broad environment/config
dumps como `env`, `printenv`, `set`, framework config dumps ni CI
secret-context dumps.

## Operaciones seguras siguientes

- Draftear comandos target-owned para ejecución Human PM: MOS-5.10 (local),
  MOS-5.12 (staging), MOS-5.14 (production), como `output.pm_command_bundle`.
- Ejecutar local/staging por agente con aprobación exacta: MOS-5.11, MOS-5.13.
- Verificar estado post-deploy: MOS-R.13. Corregir o continuar: MOS-R.3.

## Consecuencias

- MOS-5.11/5.13 dejan de ser candidatos ambiguos: son operaciones reales,
  gated, internal-only y target-owned. MOS-5.15 queda resuelta como fail-closed
  Human-PM por defecto.
- El kernel crece en tres ids mínimos, validados por `tools.validate_kernel` y
  cubiertos por tests estrictos; el resolver los pone solo al alcance del
  terminal agent.
- Rollback: revertir el PR quita los tres ids y regresa las tres filas a la
  postura de candidato previa sin pérdida de ejecución.

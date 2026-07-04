# 05 — Salidas y estados

Responsabilidad: definir forma de respuesta y resultado de resolucion. Fuentes
canonicas: `kernel/outputs.json` y `kernel/statuses.json`.

Un output define estructura, no permiso.

## Outputs de ejecucion y planes

- `output.execution_report`: reporte de implementacion con issue/PR, repo,
  rama, evidencia, archivos cambiados, disciplina, validacion, riesgos,
  commit/PR y remaining work.
- `output.manual_implementation_plan`: instrucciones humano-ejecutables con
  objetivo, archivos, cambios por ancla, razonamiento, validacion, QA manual,
  riesgos, rollback, siguiente operacion y declaracion no-write.

## Outputs de revision y cierre

- `output.review_result`: hallazgos de review/analisis con scope, evidencia,
  comparacion contra issue, findings por archivo/linea cuando aplique,
  veredicto, riesgos y no revisado.
- `output.closure_comment`: paquete de cierre con completion evidence,
  validacion real, excepciones aceptadas, limites preservados, friction note y
  referencias commit/PR. Se drafta solo tras review con evidencia de codigo.

## Outputs PM-facing

- `output.draft_issue`: issue draft con why, objetivo, source basis, scope,
  out of scope, acceptance criteria, validacion, riesgos y rollback.
- `output.route_prompt`: prompt de ruteo con bloque de variables,
  instruccion referida al issue, esfuerzo recomendado y nota de
  no-autorizacion.
- `output.pm_command_bundle`: bundle copy-safe con scope, comandos exactos,
  verificacion esperada, riesgo y rollback.
- `output.handoff_packet`: estado transferible con links vivos, verificado vs
  asumido, siguientes pasos, decisiones PM y limites activos.

## Outputs especializados

- `output.asset_prompt`: prompt para destinatario grafico/diseno.
- `output.security_review_prompt`: prompt OWASP con redaccion de secretos.
- `output.adoption_packet`: paquete para adopcion de target.
- `output.status_result`: estado no resuelto con que falta/bloquea, fuente o
  decisor, y siguiente paso seguro.

## Estados

Gana el estado mas estricto:

1. `status.blocked`: un limite, autoridad, seguridad, aprobacion o validacion
   impide actuar.
2. `status.needs_pm_decision`: falta decision material del PM sobre scope,
   prioridad, conflicto, riesgo, actor, tipo de escritura o suficiencia de
   evidencia.
3. `status.needs_context`: falta contexto/evidencia obtenible como kernel,
   issue, branch preflight o validacion.
4. `status.resolved`: actor, modo, workflow, limites, evidencia y output estan
   resueltos, sin gate bloqueante. No agrega permisos.

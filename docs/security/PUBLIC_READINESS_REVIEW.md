# Revisión de public-readiness — Stage 0 (ADR 0004)

- Fecha de revisión: 2026-07-11
- Commit base revisado: `f21654971fb050ef923af18eed68802763909375` (`main`)
- Alcance: gate Stage 0 de
  [ADR 0004](../decisions/0004-public-presentation-and-packaging.md) — árbol
  actual, exposición del historial, licenciamiento/procedencia, readiness de
  seguridad/soporte/contribuciones y postura de publicación.
- Veredicto: **`GO_WITH_BLOCKERS`** (ver [Veredicto](#veredicto)).
- Este documento no autoriza publicación ni cambio de visibilidad. Cualquier
  transición posterior requiere aprobación PM exacta y separada.

## Alcance revisado y no revisado

Revisado:

- Árbol rastreado completo en el commit base (349 archivos).
- Historial git completo alcanzable desde todas las refs locales y remotas,
  incluyendo los 154 PR heads de GitHub (`refs/pull/*/head`): 455 commits en
  total (384 alcanzables desde refs locales + 71 solo alcanzables desde PR
  heads de PRs cerrados, abandonados o rebasados, que seguirían accesibles al
  publicar el repositorio).
- Los 9 tags existentes (serie `project-os-lab-v*`, baselines de dogfood).
- Configuración de CI ([validate.yml](../../.github/workflows/validate.yml)),
  [.gitignore](../../.gitignore), metadata del repositorio en GitHub
  (lectura), adapters, templates, operaciones, docs, tests y tooling.
- Dependencias declaradas por import en `tools/` y `tests/`.

No revisado (evidencia no disponible en este gate):

- **Issues, pull requests, comentarios, reviews y descripciones en GitHub.**
  No forman parte del repositorio git, pero se vuelven públicos al cambiar la
  visibilidad. Quedan fuera del scope de #417 (árbol e historial) y no fueron
  auditados. Es una brecha material que el PM debe resolver antes de publicar
  (auditoría separada o aceptación explícita).
- Objetos git inalcanzables desde refs publicables (no se clonan al publicar;
  riesgo residual bajo: GitHub puede servir blobs por SHA a quien conozca el
  hash).
- Revisión legal especializada (este documento no es asesoría legal).

## Metodología y herramientas

- Barrido por clases de patrones con `git grep -E` sobre el árbol rastreado y
  con `git log --all -p` sobre el historial completo (dos pasadas: refs
  locales; luego refs locales + 154 PR heads). Clases: tokens GitHub
  (`ghp_/gho_/ghu_/ghs_/ghr_/github_pat_`), claves AWS (`AKIA/ASIA`), claves
  privadas PEM/OpenSSH, claves `sk-*` (OpenAI/Anthropic), tokens Slack
  (`xox*`), claves Google (`AIza*`), JWTs, webhooks (Slack/Discord), URLs con
  credenciales embebidas, URLs firmadas (`X-Amz-Signature`, etc.), cabeceras
  `Authorization`/`Bearer`, asignaciones genéricas de credenciales
  (`password/api_key/client_secret/private_key/access_token`), emails,
  direcciones IP, rutas locales absolutas y nombres de usuario de máquina.
- Inventario de nombres de archivo sensibles (`.env`, `.pem`, `.key`,
  `credential`, `token`, `backup`, `dump`, `.db`, etc.) en árbol y en los
  1.200 paths eliminados del historial.
- Inventario de binarios (`file --mime` sobre todos los archivos rastreados).
- Inventario de dominios externos y referencias `org/repo` en todo el
  historial.
- Revisión manual dirigida: `README.md`, ADR 0003/0004, adapters raíz,
  workflow de CI, shims `CLAUDE.md`/`GEMINI.md`, fixture histórico con forma
  de secreto (clasificado solo por metadatos derivados, sin imprimir el
  valor).
- Herramientas: `git` (grep/log/show/for-each-ref), `gh` (lectura), `grep`,
  `file`, Python 3 (clasificación redactada). No había scanner dedicado
  (gitleaks/trufflehog) disponible en el entorno; se compensó con clases
  múltiples de patrones y doble universo (árbol + historial + PR heads).
- Toda la evidencia se manejó redactada: ningún valor sensible o con forma de
  secreto fue impreso, copiado ni incluido aquí.

## Inventario resumido de superficies

| Superficie | Contenido | Observación |
| --- | --- | --- |
| `project-os-es/`, `project-os-en/` | Kernel JSON, operaciones, templates, adapters, docs (solo texto) | Sin valores sensibles; adapters usan `{{PLACEHOLDERS}}` |
| `tools/`, `tests/` | Resolver, validadores, wizard y guards en Python | Solo stdlib + deps opcionales; sin credenciales ni endpoints |
| `docs/decisions/` | ADR 0003 y 0004 | Citas externas con atribución y link |
| `.github/workflows/validate.yml` | CI de validación | `permissions: contents: read`; no consume secretos; no hace writes |
| Raíz (`README.md`, `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.gitignore`) | Bootloaders y docs | Ver F-07 (ruta local en `AGENTS.md`) |
| Binarios | Ninguno (único hit: `tools/__init__.py`, archivo vacío) | Sin imágenes, dumps ni assets |

## Findings

Severidad: alta / media / baja / informativa. Ningún finding contiene valores;
cuando aplica, el valor queda como `[REDACTED]`.

| ID | Sev. | Clase | Ubicación / referencia | Detalle y remediación |
| --- | --- | --- | --- | --- |
| F-01 | Alta | Licenciamiento | Raíz del repo (sin `LICENSE`) | No existe licencia. Publicar así deja el contenido "todos los derechos reservados": la adopción copy-based del Stage 1 sería legalmente inviable. Remediación: decisión PM de licencia + issue separado que la añada. **Blocker B1.** |
| F-02 | Media | Gobernanza de seguridad | Sin `SECURITY.md` ni política de reporte | No hay canal ni política de reporte responsable de vulnerabilidades. Remediación: issue separado; requiere decisión PM sobre canal de contacto (un email de contacto expone esa dirección). **Blocker B2.** |
| F-03 | Media | Gobernanza de contribución/soporte | Sin `CONTRIBUTING.md`, política de soporte, expectativas para issues/PRs externos ni código de conducta | El contenido mínimo es derivable del estado actual (soporte best-effort, sin SLA), pero aceptar o no contribuciones, el mantenimiento bilingüe ES/EN y el código de conducta son decisiones de producto. **Blocker B3.** |
| F-04 | Informativa | Secreto sintético en historial | Histórico: `tests/test_validators.py`; añadido en `79655b2` (2026-06-07), eliminado en `4d63724` (2026-06-09) | Valor `[REDACTED]` con forma de token GitHub (`ghp_…`) en el fixture negativo `secret_value_violation`, junto a SHA y string de entropía deliberadamente falsos. Verificado sintético por contexto y forma, sin imprimir el valor. No es credencial real: no requiere rotación ni rewrite. Riesgo: ruido de secret scanning al publicar; conservar este registro para el triage de alertas. |
| F-05 | Baja | Nombre de proyecto interno en historial | Histórico: ~40 líneas; commits `21a5943`, `078f098`, `be6d6a4` y merges asociados | El nombre del repo interno `codefusion-repo/project-os-console` queda expuesto al publicar el historial. Solo divulgación de nombre; sin URLs privadas ni credenciales. Remediación: aceptación PM explícita (una reescritura sería desproporcionada). |
| F-06 | Baja | Datos personales en metadata de commits | Todo el historial (455 commits) | La autoría publica nombre real y dos emails personales (clase: direcciones personales; valores en `git log`, no repetidos aquí). Solo metadata: cero apariciones en contenido de diffs. Inevitable al publicar historial sin reescribir. Remediación: aceptación PM explícita; la alternativa es un repo público nuevo con historial reducido. |
| F-07 | Informativa | Divulgación de entorno local | [`AGENTS.md`](../../AGENTS.md) (identidad del repositorio) | Publica la ruta local `$HOME/projects/personal/project-os-v2/` (layout de máquina, sin username). Opcional Stage 1: generalizar como placeholder. |
| F-08 | Informativa | Metadata del repositorio | Settings de GitHub (description) | La descripción actual menciona "roles" y no refleja el modelo vigente ni el positioning de ADR 0004. Cambio de settings: requiere aprobación PM exacta (Stage 1). |
| F-09 | Baja | Hardening de CI | [`validate.yml`](../../.github/workflows/validate.yml) | Actions pineadas por tag mayor (`checkout@v4`, `setup-python@v5`), no por SHA. Para un repo público con PRs externos se recomienda pin por SHA. El workflow ya es mínimo: `contents: read`, sin secretos, sin writes. |
| F-10 | Informativa | Tags internos | 9 tags (`project-os-lab-v*`, dogfood baselines) | Se publican junto con el repositorio. ADR 0004 ya lo contempla; el primer tag público de release es un issue separado. |

## Evaluación del árbol actual

Limpio. Sobre los 349 archivos rastreados en `f2165497`:

- Cero coincidencias en todas las clases de secretos, credenciales, JWTs,
  webhooks, URLs firmadas o con credenciales, cabeceras de autorización y
  asignaciones genéricas de credenciales.
- Cero emails, IPs, rutas absolutas locales o usernames de máquina en
  contenido (única referencia de entorno: F-07).
- Sin `.env`, claves, certificados, logs, dumps, backups, bases de datos ni
  fixtures inapropiados; sin binarios.
- Adapters y templates usan `{{PLACEHOLDERS}}` y ejemplos ficticios
  (`codefusion-repo/otro`, `org/repo`, `acme/widgets`, `test@example.com`).
- CI no consume secretos, declara `permissions: contents: read` y no ejecuta
  writes; el tooling local es read-only frente a GitHub salvo los modos
  delegados gobernados por el kernel.
- Docs y operaciones enseñan prácticas fail-closed y redacción de secretos;
  no se identificó documentación que enseñe prácticas inseguras.

## Evaluación del historial

Publicable tal cual según la evidencia disponible; ningún blocker proviene
del historial, pero tres exposiciones requieren aceptación PM explícita
(F-04, F-05, F-06).

- Universo auditado: 455 commits (todas las refs + 154 PR heads), 2026-05-19
  a 2026-07-11, ~119 KiB de pack.
- Único hit con forma de secreto en todo el universo: el fixture sintético
  F-04. Sin claves reales, sin `.env` históricos, sin rutas locales, sin IPs,
  sin URLs con credenciales.
- 1.200 paths eliminados inventariados (superficies retiradas: contract-graph
  `contracts/` con 803 archivos, `legacy-project-os/`, `schemas/`,
  `project_os_v2/`, ADRs 0001–0002, `fuentes/` con notas de modelado):
  contenido **obsoleto, no inseguro**. Nombres sensibles-aparentes revisados
  uno a uno (regla de seguridad, operación MOS-R.18 y fixtures de
  validadores): todos son artefactos de política o de test.
- No se requiere reescritura de historial ni repo nuevo por motivos de
  seguridad. La opción de historial reducido solo aplica si el PM no acepta
  F-05/F-06.
- No se ejecutó (out of scope): reescritura, force-push, rotación de
  secretos.

## Postura de licenciamiento y procedencia

- **Código propio:** sin licencia (F-01). Es el blocker principal.
- **Dependencias:** runtime solo stdlib de Python. `pytest` (MIT) solo en
  test/CI; `prompt_toolkit` (BSD-3-Clause) es un enhancement opcional con
  import protegido (el wizard y los tests degradan sin él). Ninguna se
  vendoriza ni redistribuye: no generan obligaciones de atribución en el
  árbol.
- **Terceros en docs:** ADR 0004 cita documentación oficial de OpenAI,
  LangChain y Microsoft con frases breves entrecomilladas, atribución y link;
  uso de cita razonable. Sin snippets de código de terceros identificados.
- **Assets:** no hay imágenes, iconos, diagramas binarios, audio ni video en
  el árbol; nada que licenciar ni atribuir.
- **Procedencia:** el historial completo muestra autoría única consistente
  (dos identidades del mismo autor + co-autoría de agentes declarada en
  trailers). No se encontró contenido de procedencia no demostrable.
- **Postura recomendada:** licencia permisiva única para todo el repositorio
  (docs + kernel JSON + tooling). Candidatas: **Apache-2.0** (concesión
  explícita de patentes, patrón NOTICE, más protector para adopción por
  terceros) o **MIT** (máxima simplicidad). La selección es decisión PM y no
  se ejecuta en este issue. Esto no es asesoría legal; si el PM prevé usos
  corporativos sensibles, solicitar revisión legal antes del primer release
  público.

## Postura de seguridad, soporte y contribuciones

| Documento | Estado | ¿Derivable hoy? | Decisión requerida |
| --- | --- | --- | --- |
| `SECURITY.md` (reporte responsable) | Ausente | Sí, salvo el canal de contacto | PM: canal (email/advisories de GitHub) |
| Política de soporte / mantenimiento | Ausente | Sí (best-effort, sin SLA, versiones: solo superficie activa) | PM: confirmar postura |
| `CONTRIBUTING.md` + expectativas de issues/PRs externos | Ausente | Parcialmente (el modelo de trabajo ya está en `project-os-es/docs/reglas.md`) | PM: ¿acepta contribuciones externas? ¿en qué idioma(s)? |
| Código de conducta | Ausente | Plantillas estándar disponibles | PM: ¿corresponde adoptarlo? |
| Ownership / actualización de docs y comparaciones fechadas | Parcial (ADR 0004 exige re-verificación periódica de la matriz comparativa) | Sí | PM: cadencia de re-verificación |
| Mantenimiento bilingüe ES/EN | Guardas de paridad existentes (`tests/test_project_os_bilingual_parity.py`) | Sí | PM: compromiso público de paridad |

## Postura de publicación (claims)

Verificado contra ADR 0004 en las superficies públicas actuales (`README.md`,
docs ES/EN, adapters):

- Cero coincidencias de lenguaje de autonomía, ejecución automática, runtime,
  ahorro universal de tokens/costos, precios, o reemplazo de OpenAI Agents
  SDK / LangGraph / Deep Agents / AutoGen / Claude Code / Codex / GitHub.
- La palabra "harness" aparece solo dentro de ADR 0004, definiendo la regla
  de uso cualificado; ninguna superficie pública la usa a secas.
- El README describe el producto real (kernel resoluble + estado vivo en
  GitHub + no-autorización) y coincide con el pitch canónico de ADR 0004.
- Nada en el árbol promete CLI, API, bridge, MCP, GPT action, SLA ni
  soporte comprometido.
- Pendiente de Stage 1 (no blockers de este gate): descripción del repo en
  GitHub desactualizada (F-08) y benchmark de contexto reproducible aún no
  publicado (ADR 0004 lo exige para los docs de Stage 1, no para este gate).

## Blockers

Finitos y accionables; cada remediación es una unidad separada (no creada
aquí):

- **B1 (F-01):** decisión PM de licencia + issue que la añada. Sin licencia
  no debe considerarse ninguna publicación.
- **B2 (F-02):** issue para `SECURITY.md` con canal de reporte decidido por
  el PM.
- **B3 (F-03):** issue para `CONTRIBUTING.md` + política de soporte (+ código
  de conducta si el PM lo decide).
- **B4 (cobertura):** decisión PM sobre las superficies no auditadas que la
  publicación expondría — issues/PRs/comentarios de GitHub — mediante
  auditoría separada o aceptación explícita del riesgo.

## Riesgos aceptables (si el PM los acepta explícitamente)

- F-04: ruido potencial de secret scanning por el fixture sintético
  histórico.
- F-05: divulgación del nombre `project-os-console`.
- F-06: nombre y emails personales en metadata de autoría.
- F-07: ruta `$HOME` genérica en `AGENTS.md`.
- F-09: pin de actions por tag (hardening opcional antes de publicar).
- F-10: tags internos visibles.
- Contenido obsoleto (no inseguro) recuperable desde el historial.

## Decisiones abiertas para el PM

1. Licencia concreta (Apache-2.0 vs MIT vs otra) — B1.
2. Canal de reporte de vulnerabilidades — B2.
3. Postura de contribuciones, soporte, idiomas y código de conducta — B3.
4. Aceptación de exposición del historial tal cual (F-04, F-05, F-06) o repo
   público nuevo con historial reducido.
5. Tratamiento de issues/PRs de GitHub ante un cambio de visibilidad — B4.
6. Cadencia de re-verificación de comparaciones fechadas (ADR 0004).

## Veredicto

**`GO_WITH_BLOCKERS`.**

- El árbol actual está limpio y el historial no contiene credenciales reales:
  no hay blockers de secretos.
- Los blockers son de gobernanza y cobertura: B1 (licencia), B2 (seguridad),
  B3 (contribución/soporte), B4 (superficies GitHub no auditadas).
- `NO_GO` no aplica: no se encontró evidencia que obligue a permanecer
  internal-only. `GO` no aplica: sin licencia ni políticas mínimas, la
  publicación no puede considerarse.

## Condiciones exactas para considerar Stage 0 completado

1. El PM revisa este artefacto y registra su decisión sobre cada blocker
   (B1–B4) y cada riesgo aceptable (F-04–F-07, F-09, F-10).
2. B1–B3 quedan convertidos en issues separados (o B2/B3 explícitamente
   diferidos por decisión PM registrada; B1 no es diferible para publicar).
3. B4 queda resuelto por auditoría separada o aceptación PM explícita.
4. Con eso, Stage 0 queda completado **como gate de evidencia**. Incluso
   entonces, ningún cambio de visibilidad, tag, release o publicación queda
   autorizado: cada uno requiere aprobación PM exacta posterior y separada,
   como exige ADR 0004.

## Follow-up issues recomendados (no creados aquí)

1. `legal: seleccionar y añadir la licencia pública del repositorio` —
   bloqueante; ejecuta la decisión PM de B1.
2. `docs: añadir SECURITY.md, CONTRIBUTING.md y política de soporte` —
   bloqueante; ejecuta B2/B3 según decisiones PM.
3. `security: auditar issues, PRs y comentarios de GitHub antes del cambio de
   visibilidad` — ejecuta B4 si el PM elige auditar en vez de aceptar.
4. `chore: endurecer CI para exposición pública (pin de actions por SHA)` —
   opcional, recomendado antes de publicar (F-09).
5. Stage 1 (`docs: implementar presentación pública y onboarding visual`) ya
   está definido por ADR 0004; ahí corresponden F-07 y F-08.

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
| F-01 | Alta | Licenciamiento | Raíz del repo (sin `LICENSE`) | No existe licencia. Publicar así deja el contenido "todos los derechos reservados": la adopción copy-based del Stage 1 sería legalmente inviable. Remediación: decisión PM de licencia + issue separado que la añada. **Blocker B1 — resuelto por #419** (ver [Actualización de B1](#actualización-de-b1--licencia-pública-añadida-2026-07-13)). |
| F-02 | Media | Gobernanza de seguridad | Sin `SECURITY.md` ni política de reporte | No hay canal ni política de reporte responsable de vulnerabilidades. Remediación: issue separado; requiere decisión PM sobre canal de contacto (un email de contacto expone esa dirección). **Blocker B2 — resuelto por #421** (ver [Actualización de B2/B3](#actualización-de-b2b3--políticas-de-seguridad-contribución-y-soporte-añadidas-2026-07-13)). |
| F-03 | Media | Gobernanza de contribución/soporte | Sin `CONTRIBUTING.md`, política de soporte, expectativas para issues/PRs externos ni código de conducta | El contenido mínimo es derivable del estado actual (soporte best-effort, sin SLA), pero aceptar o no contribuciones, el mantenimiento bilingüe ES/EN y el código de conducta son decisiones de producto. **Blocker B3 — resuelto por #421** (ver [Actualización de B2/B3](#actualización-de-b2b3--políticas-de-seguridad-contribución-y-soporte-añadidas-2026-07-13)). |
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

- **Código propio:** sin licencia (F-01) al momento de esta revisión; era el
  blocker principal. Resuelto después por #419 con Apache-2.0 (ver
  [Actualización de B1](#actualización-de-b1--licencia-pública-añadida-2026-07-13)).
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
  no debe considerarse ninguna publicación. **Resuelto** por #419: decisión
  PM exacta (Apache-2.0) y `LICENSE` añadido (ver
  [Actualización de B1](#actualización-de-b1--licencia-pública-añadida-2026-07-13)).
- **B2 (F-02):** issue para `SECURITY.md` con canal de reporte decidido por
  el PM. **Resuelto** por #421: decisiones PM exactas registradas y
  `SECURITY.md` añadido (ver
  [Actualización de B2/B3](#actualización-de-b2b3--políticas-de-seguridad-contribución-y-soporte-añadidas-2026-07-13)).
- **B3 (F-03):** issue para `CONTRIBUTING.md` + política de soporte (+ código
  de conducta si el PM lo decide). **Resuelto** por #421: `CONTRIBUTING.md`,
  `SUPPORT.md` y `CODE_OF_CONDUCT.md` añadidos (ver
  [Actualización de B2/B3](#actualización-de-b2b3--políticas-de-seguridad-contribución-y-soporte-añadidas-2026-07-13)).
- **B4 (cobertura):** decisión PM sobre las superficies no auditadas que la
  publicación expondría — issues/PRs/comentarios de GitHub — mediante
  auditoría separada o aceptación explícita del riesgo. **Resuelto** por
  #422: decisión de arquitectura registrada en ADR 0005 — este repositorio
  no se publica y sus superficies GitHub no migran a la futura superficie
  pública (ver
  [Actualización de B4](#actualización-de-b4--estrategia-de-repositorio-separado-2026-07-13)).

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

1. Licencia concreta (Apache-2.0 vs MIT vs otra) — B1. **Decidida y
   ejecutada en #419: Apache-2.0.**
2. Canal de reporte de vulnerabilidades — B2. **Decidida y ejecutada en
   #421: `support@codefusion.cl` privado hoy; private vulnerability reporting
   como canal estructurado recomendado futuro, sin habilitar settings.**
3. Postura de contribuciones, soporte, idiomas y código de conducta — B3.
   **Decidida y ejecutada en #421: contribuciones aceptadas issue-first,
   soporte best-effort sin SLA, español/inglés y Contributor Covenant 3.0.**
4. Aceptación de exposición del historial tal cual (F-04, F-05, F-06) o repo
   público nuevo con historial reducido. **Decidida en #422: el repositorio
   nuevo conserva la base git auditada y el PM acepta explícitamente F-04,
   F-05 y F-06; este repositorio no se publica.**
5. Tratamiento de issues/PRs de GitHub ante un cambio de visibilidad — B4.
   **Decidida en #422: no se migran ni publican; la futura superficie
   pública es un repositorio nuevo con su propio gate (ADR 0005).**
6. Cadencia de re-verificación de comparaciones fechadas (ADR 0004).

## Resultado de la revisión PM (2026-07-11)

Primera revisión PM de este artefacto, registrada en PR #418. Clasificación:
**decisión exacta** / **dirección PM definida** / **propuesta downstream
pendiente de diseño** / **trabajo expresamente no autorizado**. Esta sección
solo registra el resultado: no implementa nada, no cierra ningún blocker y no
altera el veredicto ni los findings técnicos.

### B1 — Licencia: decisión exacta pendiente

Intención PM registrada:

- proyecto open source;
- libre uso, modificación y redistribución;
- conservación de atribución y derechos del autor;
- permitir que cada usuario adapte el kernel y el futuro CLI.

Recomendación inicial para la decisión posterior: **Apache-2.0** — permite
usar, modificar y distribuir; concesión expresa de patentes; exige conservar
los avisos aplicables e indicar archivos modificados; no obliga a publicar
las modificaciones como open source. Aclaración: "atribución" significa
conservar licencia, copyright y avisos en las distribuciones; Apache-2.0 no
obliga a mostrar branding de CodeFusion en la interfaz de ningún producto.
MIT cubre la misma intención con un texto más breve, pero sin la concesión
expresa de patentes. MPL-2.0 solo sería candidata si se quisiera copyleft a
nivel de archivo, obligación que no aparece en la intención PM actual.

La selección exacta sigue pendiente y nada de esto autoriza crear `LICENSE`.
B1 permanece abierto.

Actualización: la decisión exacta quedó registrada en #419 y B1 fue resuelto
(ver [Actualización de B1](#actualización-de-b1--licencia-pública-añadida-2026-07-13)).

### B2 — Seguridad: dirección PM definida; implementación pendiente

- Canal de contacto: `support@codefusion.cl`.
- Los reportes no deben incluir datos sensibles.
- Cuando exista el repositorio público, el canal estructurado principal
  recomendado es el private vulnerability reporting de GitHub, con el email
  como canal secundario; habilitarlo es un cambio de settings separado.

B2 permanece abierto hasta que `SECURITY.md` exista (issue separado).

### B3 — Contribuciones y soporte: dirección PM parcialmente definida

- Se aceptarán contribuciones de la comunidad.
- Soporte best-effort y sin SLA, salvo decisión posterior.
- `CONTRIBUTING.md` deberá definir el proceso gobernado por issues, PRs,
  validación y review-before-close.
- Decisiones exactas pendientes: idiomas aceptados, código de conducta e
  inbound licensing.

La visión de un panel interactivo que asuma parte de la experiencia de
browser chat queda como idea downstream: no pertenece a #417, a Stage 0 ni
al follow-up documental de `CONTRIBUTING.md`. B3 permanece abierto.

### B4 — Superficies GitHub: dirección estratégica candidata, no decisión cerrada

Propuesta PM registrada:

- preservar este repositorio como baseline interno/pre-CLI;
- crear posteriormente un repositorio público nuevo con historial limpio;
- usar el desarrollo del CLI como dogfood de instalación sobre un proyecto
  separado;
- evitar publicar issues, PRs, comentarios, emails y exposiciones históricas
  de este repositorio.

Esta dirección reduciría sustancialmente B4 (y las exposiciones F-04, F-05 y
F-06 dejarían de publicarse), pero modifica el mecanismo de Stage 1 de
ADR 0004 — que hoy plantea publicar el repositorio existente — y por eso
requiere una decisión ADR/follow-up separada que defina: cuál repositorio es
la fuente de verdad; la relación entre repositorio interno y público; la
sincronización de kernel y superficies ES/EN; el ownership de tags y
releases; la política de historial y procedencia; y cómo evitar forks
divergentes o duplicación manual permanente. Ningún repositorio se crea,
taggea, transfiere ni publica dentro de esta corrección. B4 permanece
abierto.

Actualización: la decisión de arquitectura quedó registrada en #422 /
ADR 0005 y B4 fue resuelto (ver
[Actualización de B4](#actualización-de-b4--estrategia-de-repositorio-separado-2026-07-13)).

### Propuestas downstream expresamente no autorizadas

`project-os-init` (CLI de adopción), el concepto `os-git` (capa de
integración sobre una sesión GitHub existente, sin secret store propio y sin
copiar ni almacenar tokens) y el panel interactivo pertenecen a una revisión
de idea/arquitectura posterior. ADR 0004 mantiene el tooling de Stage 2 sin
autorización actual; ninguna de estas propuestas forma parte de Stage 0 ni
de sus follow-ups.

## Actualización de B1 — licencia pública añadida (2026-07-13)

Ejecutada por issue #419 con decisión PM exacta registrada como comentario en
ese issue (2026-07-12). No altera la revisión original ni el resto de
findings; solo registra la resolución de B1.

- **Licencia seleccionada:** Apache License 2.0 (SPDX: `Apache-2.0`).
- **Titular del copyright:** CodeFusion SpA. **Año:** 2026. Ambos confirmados
  por el PM en #419, no inferidos.
- **`LICENSE`:** texto oficial completo descargado de
  `https://www.apache.org/licenses/LICENSE-2.0.txt`, sin modificaciones ni
  cláusulas personalizadas (el appendix conserva sus placeholders, como exige
  el scope de #419); el aviso de copyright vive en la sección de licencia del
  `README.md`.
- **`NOTICE`:** no se crea, por decisión PM; solo se añadiría después si
  existiera una atribución concreta que deba propagarse.
- **Alcance:** la licencia cubre código, kernel JSON, templates, operaciones
  y documentación del árbol.
- **Contribuciones futuras:** inbound = outbound bajo Apache-2.0 salvo
  acuerdo escrito separado; ningún CLA o DCO se adopta en #419 y cualquier
  política adicional se decide en B3.
- **Alternativas descartadas:** MIT (cubre la intención pero sin concesión
  expresa de patentes) y MPL-2.0 (copyleft a nivel de archivo que no aparece
  en la intención PM).
- **Procedencia y titularidad:** verificadas contra la sección
  [Postura de licenciamiento y procedencia](#postura-de-licenciamiento-y-procedencia):
  autoría única consistente, dependencias no vendorizadas (`pytest` MIT solo
  test/CI; `prompt_toolkit` BSD-3-Clause opcional), citas de terceros con
  atribución y sin assets; nada requiere exclusiones ni tratamiento separado
  bajo Apache-2.0.
- **PR que la incorpora:** PR #420, desde `work/419-public-license`.
- **Limitaciones:** esto no es asesoría legal. B1 resuelto no completa
  Stage 0 ni autoriza publicación, cambio de visibilidad, tags, releases,
  B2–B4, Stage 1 ni tooling downstream.

## Actualización de B2/B3 — políticas de seguridad, contribución y soporte añadidas (2026-07-13)

Ejecutada por issue #421 con las seis decisiones PM exactas registradas como
comentario en ese issue (2026-07-13): idiomas, código de conducta, versiones
y superficies soportadas, expectativas de respuesta, CLA/DCO y ownership. No
altera la revisión original ni el resto de findings; solo registra la
resolución de B2 y B3.

- **`SECURITY.md`:** reporte responsable privado a `support@codefusion.cl`;
  prohibición de publicar secretos, datos personales o detalles explotables;
  private vulnerability reporting de GitHub como canal estructurado
  recomendado futuro (habilitarlo sigue siendo un cambio de settings separado
  y no ejecutado); acuse best-effort objetivo de cinco días hábiles, sin SLA.
- **`CONTRIBUTING.md`:** contribución issue-first con ramas `work/*`,
  validación proporcional, draft PR y review-before-close; español o inglés
  con paridad semántica ES/EN cuando aplique; inbound=outbound bajo
  Apache-2.0; sin CLA ni DCO salvo decisión PM posterior y separada.
- **`SUPPORT.md`:** soporte best-effort sin SLA; canales, versiones y
  superficies cubiertas según la decisión PM; fuera de alcance el tooling
  inexistente (CLI, API, bridge, MCP, GPT action); distinción explícita entre
  soporte, seguridad y conducta.
- **`CODE_OF_CONDUCT.md`:** traducción oficial al español de Contributor
  Covenant 3.0 (CC BY-SA 4.0, atribución conservada), adoptada como texto
  normativo por decisión PM, con solo los dos placeholders de
  reporting/enforcement completados según la decisión PM: reportes privados a
  `support@codefusion.cl` con asunto `[Project OS Conduct]`, confidenciales y
  con medidas proporcionales; CodeFusion SpA responsable de la aplicación.
- **README:** sección de links a las cuatro políticas.
- **Ownership:** CodeFusion SpA propietaria y responsable final; revisión
  antes de cada release público, ante cambios de canales o superficies y al
  menos una vez al año.
- **Alcance preservado:** ningún setting, visibilidad, tag, release, SLA,
  CLA/DCO ni publicación fue modificado o prometido. **B4 permanece abierto**
  y el veredicto sigue siendo `GO_WITH_BLOCKERS`.
- **PR que las incorpora:** PR #425, desde
  `work/421-security-contributing-support`.

## Actualización de B4 — estrategia de repositorio separado (2026-07-13)

Ejecutada por issue #422 con decisión PM exacta registrada como comentario en
ese issue y como decisión de arquitectura durable en
[ADR 0005](../decisions/0005-public-repository-strategy.md), que enmienda el
mecanismo de Stage 1 de ADR 0004. No altera la revisión original ni el resto
de findings; solo registra la resolución de B4 y sus consecuencias sobre este
gate.

- **Decisión:** `codefusion-repo/project-os-v2` permanece privado e
  internal-only y no será publicado. La futura superficie pública de
  Project OS y su CLI será un repositorio nuevo (`agent-os-cli`), creado
  posteriormente como privado, que será fuente de verdad tras una transición
  única y sin sincronización bidireccional ni backports.
- **Resolución de B4:** las superficies GitHub no auditadas de este
  repositorio (issues, PRs, comentarios, reviews, descripciones y metadata)
  no se publican ni migran al repositorio nuevo; por eso B4 queda resuelto
  para este repositorio sin auditoría adicional. Ninguna superficie no
  auditada queda expuesta por esta decisión.
- **F-04, F-05, F-06:** el repositorio nuevo conservará la base git y de
  contenido auditada, y el PM acepta explícitamente esos tres riesgos
  históricos documentados. Al no publicarse este repositorio, esas
  exposiciones no se materializan aquí; viajan con la base git al
  repositorio nuevo y quedan cubiertas por su gate propio.
- **F-07, F-09, F-10:** dejan de ser exposiciones de este gate porque este
  repositorio no se publica; cualquier equivalente se evalúa en la auditoría
  de public-readiness propia del repositorio nuevo antes de su cambio de
  visibilidad.
- **Gates posteriores preservados:** el repositorio nuevo tendrá su propia
  auditoría de public-readiness antes de cambiar visibilidad; la publicación
  sigue bloqueada además por la confirmación PM del dogfood; y crear el
  repositorio, transferir contenido, cambiar visibilidad o settings y crear
  tags o releases siguen requiriendo aprobación PM exacta y separada.
- **Stage 1, #423 y #424:** Stage 1 conserva su contenido docs-first pero su
  mecanismo de publicación deja de ser este repositorio; #423 prepara
  documentación y onboarding reutilizables por la futura superficie pública;
  #424 queda como gate de readiness y handoff sin crear tag ni release en
  este repositorio — el tag y release públicos efectivos se ejecutan después
  en el repositorio nuevo con aprobación PM separada. La secuencia PM vigente
  es `#422 → #423 → #424 → cierre del roadmap #274 → comienzo del nuevo
  repositorio y desarrollo del CLI`.
- **Alcance preservado:** ningún repositorio fue creado, transferido,
  copiado o publicado; ningún setting, visibilidad, tag o release cambió;
  el CLI no se implementa y los proyectos demo no se modifican.
- **Efecto sobre el veredicto:** `GO_WITH_BLOCKERS` se conserva como
  registro histórico de la revisión original. Con B1–B4 resueltos ya no
  queda ningún blocker abierto de este gate, pero de eso no se deriva ningún
  `GO` de publicación para este repositorio: por ADR 0005 su publicación
  dejó de considerarse y el estado internal-only es su estado final. La
  aceptación de Stage 0 como gate de evidencia y cualquier transición
  posterior siguen siendo decisiones PM separadas.
- **ADR que la registra:** ADR 0005, desde `work/422-public-repository-strategy`.

## Veredicto

**Veredicto histórico de la revisión original (2026-07-11):
`GO_WITH_BLOCKERS`.**

- El árbol actual estaba limpio y el historial no contenía credenciales
  reales: no había blockers de secretos.
- Los blockers eran de gobernanza y cobertura: B1 (licencia), B2 (seguridad),
  B3 (contribución/soporte) y B4 (superficies GitHub no auditadas).
- En el momento de esa revisión, `NO_GO` no aplicaba porque la evidencia
  técnica no obligaba por sí sola a descartar la publicación, y `GO` no
  aplicaba porque los blockers B1–B4 seguían abiertos.

**Estado posterior a ADR 0005 (2026-07-13):** los cuatro blockers están
resueltos — B1 por #419, B2 y B3 por #421, y B4 por #422 / ADR 0005 (ver
[Actualización de B4](#actualización-de-b4--estrategia-de-repositorio-separado-2026-07-13)).
El veredicto histórico `GO_WITH_BLOCKERS` se conserva como registro de la
revisión original y no se recalcula: por decisión de arquitectura
(ADR 0005), la publicación de este repositorio dejó de considerarse y su
estado final es internal-only, de modo que de la resolución de los blockers
no se deriva ningún `GO`. Este documento sigue sin autorizar publicación,
cambio de visibilidad ni transición alguna; la aceptación de Stage 0 como
gate de evidencia y cualquier transición posterior siguen siendo decisiones
PM separadas.

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
   bloqueante; ejecuta la decisión PM de B1. **Creado y ejecutado como
   #419.**
2. `docs: añadir SECURITY.md, CONTRIBUTING.md y política de soporte` —
   bloqueante; ejecuta B2/B3 según decisiones PM. **Creado y ejecutado como
   #421.**
3. `security: auditar issues, PRs y comentarios de GitHub antes del cambio de
   visibilidad` — ejecuta B4 si el PM elige auditar en vez de aceptar.
   **Ya no aplica a este repositorio:** #422 / ADR 0005 resolvió B4 con la
   estrategia de repositorio separado, sin publicar estas superficies; el
   repositorio nuevo tendrá su propia auditoría de public-readiness.
4. `chore: endurecer CI para exposición pública (pin de actions por SHA)` —
   opcional, recomendado antes de publicar (F-09).
5. Stage 1 (`docs: implementar presentación pública y onboarding visual`) ya
   está definido por ADR 0004; ahí corresponden F-07 y F-08.

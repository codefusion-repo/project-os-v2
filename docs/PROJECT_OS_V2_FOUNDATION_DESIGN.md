# Project OS v2 Foundation Design

## 1. Objective

Define the initial Project OS v2 foundation design as a human design/reference document, including the architectural pattern, stack direction, normalized entity model, relationship model, `Resolver`, AI read flow, workflow lifecycle direction, boundaries, and future phases.

This document is based on the PM-provided source files:

- `fuentes/Modelo-de-entidades-base.txt`
- `fuentes/Modelo-base-con-definiciones-y-atributos-normalizados.txt`
- `fuentes/Relaciones-principales-y-cardinalidad.txt`

This issue creates documentation only. It does not create JSON contracts, schemas, validators, runtime behavior, parser behavior, automation, panels, context packs, target-project artifacts, release behavior, or write authorization behavior.

## 2. Problem Statement

Project OS v2 needs a stable model that lets humans and AI agents reason about project behavior without loading every possible rule, workflow, role, source, and artifact at once. The model must support highly normalized contracts, explicit relationships, evidence-based decisions, and GitHub traceability while keeping static documentation separate from live operational state.

The core problem is not how to execute the system yet. The core problem is defining the entities, attributes, relationships, and read path that later implementations can validate, project, and execute without duplicating concepts across contracts.

## 3. Architectural Pattern

Project OS v2 is designed as a:

- normalized JSON-contract system
- resolver-first system
- relation-driven system
- schema-validatable system
- workflow lifecycle oriented system
- evidence-driven system
- GitHub-traceability based system
- AI-readable system that does not require the AI to load the entire system

The AI should not read all Project OS contracts.

The intended pattern is:

1. User input arrives.
2. The AI builds or simulates `ResolverInput`.
3. The AI enters through `Resolver`.
4. `Resolver` reads only the minimal manifest, policy, indexes, and selectors needed to route the request.
5. `Resolver` selects applicable contracts.
6. `Resolver` loads related entities and relationships.
7. `Resolver` returns `ResolverOutput`.
8. The AI responds from the selected `Estado` and `Plantilla`.
9. GitHub remains the live evidence layer for issue, PR, commit, review, tag, and validation state.

## 4. Recommended Stack Direction

This stack is a design direction only, not an implementation commitment for this issue.

- JSON contracts are the canonical stable structure for entities and relationships.
- JSON Schema should validate contract shape later.
- Semantic validators should be added later, likely in Python, to validate cross-contract rules and relationships.
- An optional generated read model may be created later for faster lookup and AI retrieval.
- SQLite, PostgreSQL, or a graph database may later be used as a projection, not as the source of truth.
- Markdown is only for human design/reference.
- GitHub issues, PRs, commits, comments, reviews, tags, and validation outputs are live evidence.

The source of truth direction is: JSON contracts first, live GitHub evidence for operational traceability, Markdown for explanation, and database/read-model projections only as generated views.

## 5. Normalization Principles

Project OS v2 preserves maximum normalization.

Required rule: entities store their own attributes. Compatibility, permission, requirement, dependency, sequencing, and restriction live in `Relación`.

Normalization boundaries:

- Do not duplicate permissions inside `Actor` if they are expressed by `Límite` or `Relación`.
- Do not duplicate required evidence inside `Workflow` if it is expressed by `Relación`.
- Do not duplicate execution behavior inside `Workflow` or `WorkflowStep` if it is resolved through `Actor`, `Rol`, `Acción`, `Fuente`, `Evidencia`, `Límite`, `Regla`, and `Relación`.
- Do not create prompt and response as separate entities when `Plantilla` covers both.
- Do not create approval as a separate entity when it is `Evidencia`.
- Do not create context as a separate entity when it belongs to `Rol` or `Plantilla`.
- Do not create environment as a separate entity when `Actor` covers execution surface.
- Do not create policy as a separate entity when `Límite` and `Regla` cover constraints and behavior.

The design favors small contracts with explicit links over large contracts that embed adjacent concepts.

Execution behavior is resolved from `Actor` + `Rol` + `Acción` + `Límite` + `Regla` + `Fuente` + `Evidencia` through `Relación`. `Workflow` defines process order and lifecycle progression. `WorkflowStep` defines step order, objective, Actor/Rol delegation, transition logic, and expected artifacts. `Resolver` composes relationships and determines `Estado`.

## 6. Entity Model

The PM-provided base entity model is preserved exactly:

1. `Resolver`
2. `Actor`
3. `Rol`
4. `Workflow`
5. `WorkflowStep`
6. `Acción`
7. `Recurso`
8. `Scope`
9. `Fuente`
10. `Evidencia`
11. `Estado`
12. `Límite`
13. `Regla`
14. `Variable`
15. `Plantilla`
16. `Artefacto`
17. `Relación`
18. `Contrato`

Each base entity should become a versionable JSON contract later. This document does not create those contracts.

## 7. Entity Attributes

| Entity | Definition | Owns | Normalized attributes | Must not own | Examples |
| --- | --- | --- | --- | --- | --- |
| `Resolver` | Entrada única para resolver qué contratos aplican a una solicitud. | Resolver identity, version, manifest reference, policy reference, input/output schema references, fallback state reference. | `id`, `nombre`, `descripción`, `versión`, `manifest_ref`, `policy_ref`, `input_schema_ref`, `output_schema_ref`, `fallback_estado_id` | Full workflows, actor permissions, evidence bodies, GitHub state snapshots, target-project artifacts, or duplicated relationship decisions. | A future resolver contract that composes relationships and routes an AI request to the minimal applicable contracts. |
| `Actor` | Superficie desde donde se ejecuta una acción y sus capacidades base. | Execution surface identity and base capability description. | `id`, `nombre`, `descripción`, `superficie_capacidad` | Permissions, workflow membership, role behavior, policy, or live environment state; these belong in `Límite`, `Regla`, and `Relación`. | A future actor contract representing an execution surface. |
| `Rol` | Lente profesional aplicado a una tarea. | Professional lens and role description used to interpret a task. | `id`, `nombre`, `descripción`, `lente_profesional` | Actor identity, permissions, evidence, workflow order, or prompt text that belongs to `Plantilla`. | A future role contract representing a professional review lens with related rules and templates. |
| `Workflow` | Proceso iterable que define orden de proceso y etapa del ciclo de vida. | Workflow identity, lifecycle stage, and workflow order. | `id`, `nombre`, `descripción`, `etapa_ciclo_vida`, `orden` | Actor/role execution behavior, direct actions, direct evidence, direct limits, direct rules, or resolver-derived state. | A future workflow contract for one lifecycle process and its ordered step sequence. |
| `WorkflowStep` | Paso ordenado con objetivo, delegación Actor/Rol y lógica de transición. | Step identity, order, objective, and advance/repeat/block conditions. | `id`, `nombre`, `descripción`, `orden`, `objetivo`, `condición_avance`, `condición_repetición`, `condición_bloqueo` | Direct action execution, evidence ownership, direct limits, direct rules, actor capability, role rules, produced artifact content, or next-step embedding. | A future step contract for one ordered stage that delegates to `Actor` and `Rol` through relationships. |
| `Acción` | Operación concreta que se quiere realizar. | Action identity and action type. | `id`, `nombre`, `descripción`, `tipo` | Actor identity, resource details, scope, evidence, or execution result. | A future action contract for a concrete operation such as inspect, create, validate, or review. |
| `Recurso` | Objeto sobre el que actúa una acción. | Resource identity, type, name, and location. | `id`, `tipo`, `nombre`, `ubicación` | Action semantics, scope membership, evidence verification state, or artifact generation rules. | A future resource contract pointing to a file path, issue, PR, commit, tag, or external reference. |
| `Scope` | Alcance permitido de una tarea. | Scope identity and allowed task boundary description. | `id`, `nombre`, `descripción` | Resources by value, action permissions, actor capability, or workflow order. | A future scope contract representing the allowed boundary of a task. |
| `Fuente` | Origen de autoridad o verdad. | Source identity, type, location, authority level, and freshness requirement. | `id`, `tipo`, `nombre`, `ubicación`, `nivel_autoridad`, `frescura_requerida` | Evidence observations, verification state, resource ownership, or workflow decisions. | A future source contract for an authoritative origin such as a PM file or live GitHub object category. |
| `Evidencia` | Información verificable usada para decidir o validar. | Evidence identity, type, reference, verification state, and observation timestamp. | `id`, `tipo`, `referencia`, `estado_verificación`, `observado_en` | Source authority, workflow policy, approval as an entity, or static copies of mutable GitHub state. | A future evidence contract/reference for an observed issue, PR, commit, review, validation output, or source file observation. |
| `Estado` | Resultado de resolución o ejecución. | State identity and meaning. | `id`, `nombre`, `descripción` | The rules that cause the state, the evidence that proves it, or generated response text. | A future state contract such as applicable, blocked, needs-evidence, validated, or ready-for-review. |
| `Límite` | Restricción obligatoria que no debe romperse. | Limit identity, type, severity, and constraint description. | `id`, `nombre`, `descripción`, `tipo`, `severidad` | Actor permissions by embedding, workflow membership, rule behavior, or failure evidence. | A future limit contract defining a hard boundary. |
| `Regla` | Norma que guía conducta o decisión. | Rule identity, condition, and expected behavior. | `id`, `nombre`, `descripción`, `condición`, `comportamiento_esperado` | Limit severity, actor identity, workflow order, evidence payloads, or static GitHub traceability. | A future rule contract defining expected behavior under a condition. |
| `Variable` | Dato dinámico configurable. | Variable identity, type, default value, and allowed values. | `id`, `nombre`, `tipo`, `valor_default`, `valores_permitidos` | Template bodies, workflow definitions, live runtime values, or validator behavior. | A future variable contract parameterizing a template or workflow. |
| `Plantilla` | Estructura reusable para generar prompts, respuestas, reportes o bodies. | Template identity, type, format, and required sections. | `id`, `nombre`, `tipo`, `formato`, `secciones_requeridas` | Variable definitions, workflow eligibility, live evidence state, or separate prompt/response entities. | A future template contract for a response, prompt, report, or PR body structure. |
| `Artefacto` | Resultado referenciable esperado por un paso o producido por acción/plantilla. | Artifact identity, type, name, and reference. | `id`, `tipo`, `nombre`, `referencia` | Producing step logic, template definition, resource definition, or validation state. | A future artifact contract/reference for a design document, generated report, PR body, or validation result. |
| `Relación` | Vínculo formal entre entidades para compatibility, permission, requirement, dependency, sequencing, or restriction semantics. | Relationship identity, endpoints, relationship type, cardinality, required flag, and order. | `id`, `origen_entidad`, `origen_id`, `destino_entidad`, `destino_id`, `tipo_relación`, `cardinalidad`, `requerido`, `orden` | Duplicated attributes from either endpoint or embedded copies of related contracts. | A future relationship contract connecting `WorkflowStep` to delegated `Actor`/`Rol`, expected `Artefacto`, or next `WorkflowStep`. |
| `Contrato` | Especificación formal/versionable de una entidad o relación. | Contract identity, entity type, version, schema reference, and state. | `id`, `nombre`, `entidad_tipo`, `versión`, `schema_ref`, `estado` | Entity-specific attributes not belonging to the contract wrapper, live GitHub evidence, or generated database rows. | A future contract file that formalizes one entity or relationship version. |

## 8. Relationship Model

`Relación` is the normal form for cross-entity behavior. Any compatibility, permission, requirement, dependency, sequencing, restriction, reuse, or output link should be represented as a relationship instead of duplicated into entity contracts.

The main relationship model is:

| Relationship | Cardinality | Description |
| --- | ---: | --- |
| Resolver carga Contrato | 1:N | Un resolver usa varios contratos para resolver una solicitud. |
| Resolver usa Relación | 1:N | Un resolver compone relaciones para seleccionar contexto mínimo aplicable. |
| Resolver determina Estado | 1:N | Un resolver devuelve estados derivados de relaciones, evidencia y límites. |
| Contrato formaliza Entidad | 1:N | Una entidad puede tener múltiples versiones de contrato. |
| Contrato formaliza Relación | 1:N | Una relación puede tener múltiples versiones de contrato. |
| Workflow contiene WorkflowStep | 1:N | Un workflow agrupa uno o más pasos ordenados. |
| Workflow ordena WorkflowStep | 1:N | Un workflow define el orden del proceso entre sus pasos. |
| Workflow avanza a Workflow | N:M | Un workflow puede habilitar otro workflow dentro del ciclo de vida. |
| Workflow usa Plantilla | N:M | Un workflow puede usar plantillas para salidas o reportes de proceso. |
| WorkflowStep pertenece a Workflow | N:1 | Un paso pertenece a un workflow que lo contiene y ordena. |
| WorkflowStep delega Actor | N:M | Un paso delega ejecución a actores sin copiar sus capacidades. |
| WorkflowStep delega Rol | N:M | Un paso delega lente profesional a roles sin copiar sus reglas. |
| WorkflowStep avanza a WorkflowStep | N:M | Un paso puede tener siguiente paso, bifurcaciones o repetición. |
| WorkflowStep avanza a Workflow | N:M | Un paso final puede habilitar otro workflow. |
| WorkflowStep espera Artefacto | N:M | Un paso declara artefactos esperados sin producirlos directamente. |
| Rol aplica Regla | N:M | Un rol puede tener reglas de conducta o criterio profesional. |
| Rol usa Plantilla | N:M | Un rol puede usar plantillas adecuadas a su lente profesional. |
| Rol es compatible con Actor | N:M | Un rol puede ser compatible con varios actores y superficies. |
| Actor ejecuta Acción | N:M | Un actor puede ejecutar varias acciones si sus límites lo permiten. |
| Actor tiene Límite | N:M | Los límites del actor definen capacidad real. |
| Actor usa Fuente | N:M | Un actor puede consultar fuentes permitidas por sus relaciones y límites. |
| Acción actúa sobre Recurso | N:M | Una acción puede operar sobre varios tipos de recurso. |
| Acción ocurre dentro de Scope | N:M | Una acción solo es válida dentro de un alcance. |
| Acción produce Artefacto | N:M | Una acción puede producir artefactos como resultado de ejecución. |
| Scope incluye Recurso | N:M | Un scope define qué recursos entran o quedan fuera. |
| Fuente provee Evidencia | 1:N | Una fuente puede producir muchas evidencias. |
| Evidencia refiere Recurso | N:M | Una evidencia puede apuntar a uno o más recursos. |
| Límite falla en Estado | N:1 | Si un límite se rompe, lleva a un estado como blocked. |
| Regla falla en Estado | N:1 | Si una regla no se cumple, lleva a un estado definido. |
| Variable parametriza Plantilla | N:M | Variables rellenan o modifican plantillas. |
| Variable parametriza Workflow | N:M | Variables pueden afectar idioma, repo, branch pattern, etc. |
| Variable parametriza Contrato | N:M | Variables pueden parametrizar contratos sin duplicar su estructura. |
| Plantilla genera Artefacto | 1:N | Una plantilla puede generar muchos artefactos. |
| Artefacto se asocia a Recurso | N:M | Un artefacto puede documentar o modificar recursos. |

## Relationship Normalization Correction

This correction removes direct process-to-execution ownership from the model.

- Workflow does not own actor/role execution behavior.
- Workflow does not own limits/rules directly.
- WorkflowStep does not execute actions directly.
- WorkflowStep does not own evidence directly.
- WorkflowStep delegates Actor and Rol.
- WorkflowStep controls ordering, transitions, repeat/block/advance conditions, and expected artifacts.
- Actor relationships define execution surface, available actions, limits, and sources.
- Rol relationships define professional lens, rules, compatible actors, and templates.
- Resolver composes relationships to determine applicable action, evidence, limits, rules, state, and output.

The rationale is that `Workflow` and `WorkflowStep` define process order, lifecycle sequencing, delegation, and transition. `Actor` and `Rol`, plus their related entities, define how work is executed. This keeps the model reusable, scalable, normalized, and maintainable.

## 9. Cardinality Model

Cardinality defines the allowed relationship shape, not embedded ownership.

- `1:N` means one source can point to many targets, while each relationship instance still remains explicit.
- `N:1` means many sources can reuse or converge on one target.
- `N:M` means both sides can participate in many relationships, and the relationship contract carries the meaning, requirement flag, and order.

The cardinality model keeps reusable concepts reusable. For example, a `Regla` can be applied to multiple `Rol` contracts; a `Límite` can be shared by multiple actors; a `Fuente` can provide many `Evidencia` references; a `Plantilla` can generate multiple `Artefacto` records; and a `WorkflowStep` can delegate multiple actors or roles, expect multiple artifacts, and advance to multiple next steps or workflows when branching or repetition is allowed.

## 10. Resolver as Single AI Read Entrypoint

The Resolver is the single read entrypoint for Project OS v2 behavior.

The `Resolver` is responsible for deciding which contracts apply to a request. AI agents should enter Project OS v2 through `Resolver`, not by scanning the entire contract library.

The `Resolver` should eventually load:

- a manifest or equivalent contract inventory
- policy/index references needed for routing
- selector definitions
- the applicable `Contrato` records
- applicable `Relación` records
- related `Actor`, `Rol`, `Workflow`, `WorkflowStep`, `Límite`, `Regla`, `Plantilla`, `Variable`, `Fuente`, and `Evidencia` contracts
- related `Acción`, `Recurso`, `Scope`, and `Artefacto` contracts when required by the selected relationships

The result is `ResolverOutput`: a minimal selected context that tells the AI what state applies, what workflow or step is active, what actor/role delegation applies, what action is available, what evidence is required or available through sources, what limits/rules bind the response, and which template should structure the answer.

## 11. Selector / Routing Concept

Selectors are conceptual routing aids that help `Resolver` select applicable contracts. They are not implemented in this issue.

Selectors may later route by:

- request type
- repository or project scope
- lifecycle stage
- target resource type
- actor surface
- requested role lens
- available or missing evidence
- blocking limits or rules
- output/template need

Selectors should point to contracts and relationships. They should not become a second source of truth for entity attributes.

## 12. Workflow and WorkflowStep Model

`Workflow` is an iterable software lifecycle process. It owns lifecycle stage, process order, and ordered `WorkflowStep` membership. It does not own execution behavior; execution is resolved by `Resolver` through step delegation and related actors, roles, actions, sources, evidence, limits, rules, templates, artifacts, and states.

`WorkflowStep` is explicitly modeled as the ordered unit of workflow progression. A step must be able to describe:

- ordered step
- objective
- delegated `Actor`
- delegated `Rol`
- expected artifacts
- condition to advance
- condition to repeat
- condition to block
- next `WorkflowStep`
- next `Workflow`

`WorkflowStep` owns only its normalized step attributes: identity, order, objective, and transition conditions. It delegates `Actor` and `Rol` through `Relación`. It does not embed action execution, evidence ownership, limits, rules, artifact content, next step, or next workflow. Those are linked by `Relación` and composed by `Resolver`.

This makes a workflow iterable: a step can advance, repeat, block, branch to another step, or enable another workflow based on resolver-composed evidence, limits, rules, and state.

## 13. Software Lifecycle Workflow Direction

Project OS v2 workflows should model the software lifecycle as evidence-driven iteration.

- Design creates base source-of-truth documents for the target project.
- Planning converts those source documents into GitHub live traceability through issues.
- Implementation executes GitHub issues.
- Validation checks target evidence.
- Review decides readiness using evidence.
- Release/production only happens with explicit evidence and PM approval.

This lifecycle direction is conceptual in this issue. No workflow contracts, runners, automation, release behavior, or write authorization behavior are created here.

## 14. AI Read Flow

The intended AI read flow is:

1. User input arrives.
2. AI builds or simulates `ResolverInput`.
3. AI enters through `Resolver`.
4. `Resolver` reads manifest/policy/indexes/selectors.
5. `Resolver` selects only applicable contracts.
6. `Resolver` loads applicable `Relación` contracts and related `Actor`, `Rol`, `Workflow`, `WorkflowStep`, `Acción`, `Recurso`, `Scope`, `Límite`, `Regla`, `Plantilla`, `Variable`, `Fuente`, `Evidencia`, and `Artefacto` contracts.
7. `Resolver` returns `ResolverOutput`.
8. AI responds using the selected `Estado` and `Plantilla`.
9. GitHub remains live evidence for issue/PR/commit/review/tag/validation state.

The AI should use selected contracts and relationships as the active context. It should not infer missing permissions, skipped evidence, or lifecycle advancement from static Markdown alone.

## 15. Contract Loading Strategy

Contract loading should be minimal, layered, and relationship-aware.

Recommended later loading order:

1. Load the `Resolver` contract.
2. Load a manifest/index of available `Contrato` records.
3. Load selector/policy references needed to classify the request.
4. Select candidate contracts by request type, scope, actor surface, role lens, lifecycle stage, and resource type.
5. Expand through required `Relación` records.
6. Load only the related entity contracts needed for the selected path.
7. Resolve execution behavior through delegated `Actor`, `Rol`, available `Acción`, permitted `Fuente`, referenced `Evidencia`, applicable `Límite`, and applicable `Regla`.
8. Determine `Estado` from the composed relationship set.
9. Select `Plantilla` and `Variable` contracts needed for output.
10. Return a compact `ResolverOutput`.

The loading strategy should support generated indexes later, but the canonical information should remain in JSON contracts.

## 16. What Belongs in JSON Contracts

JSON contracts should contain stable, versionable structure:

- normalized entity attributes from the base model
- relationship endpoints and cardinality
- normalized delegation, compatibility, requirement, dependency, sequencing, and restriction relationships
- schema references
- lifecycle definitions at the contract level
- reusable limits and rules
- template structure and required sections
- source definitions and evidence reference shape
- state definitions
- contract version and status metadata

JSON contracts should be the canonical stable structure for Project OS v2.

## 17. What Does Not Belong in JSON Contracts

JSON contracts should not contain:

- live GitHub issue state copied as static data
- live PR state copied as static data
- commit review status copied as static data
- validation output bodies copied as canonical facts
- generated database projection rows
- runtime cache data
- parser output
- automation execution logs
- panel/UI state
- target-project generated artifacts
- write authorization decisions
- direct workflow or step copies of actor/role execution behavior
- duplicated permissions, requirements, dependencies, sequencing, or restrictions that belong in `Relación`

Contracts should reference evidence and sources where appropriate, but live state should remain live.

## 18. What Belongs in GitHub Live Evidence

GitHub live evidence includes mutable operational traceability:

- issues and issue state
- PRs and PR state
- commits
- comments
- reviews
- tags
- validation outputs
- references to changed files or generated artifacts

GitHub should remain the live evidence layer for execution, review, readiness, release, and validation state. Static docs should not encode live GitHub traceability as if it were canonical system state.

## 19. What Belongs in Markdown Docs

Markdown belongs to human design/reference.

Markdown may describe:

- architectural pattern
- entity model
- relationship model
- normalization rules
- AI read flow
- workflow lifecycle direction
- stack direction
- risks and open questions

Markdown should not become a second contract system. It should not duplicate live evidence, encode runtime behavior, or act as the source of truth for actors, roles, workflows, limits, or rules once JSON contracts exist.

## 20. Future Database / Read-Model Direction

A database or read model may later be generated to speed up lookup and AI retrieval.

Acceptable projection targets may include:

- SQLite for local generated indexes
- PostgreSQL for shared/queryable projection
- graph database storage for relationship traversal
- vector/search indexes for retrieval support

These are projections only. The source of truth remains JSON contracts plus GitHub live evidence for operational state. Any database/read-model projection should be reproducible from contracts and live evidence references.

## 21. Future Implementation Phases

Potential future phases:

1. Define JSON contract directory layout and naming conventions.
2. Create JSON Schema files for contract shape validation.
3. Create initial entity and relationship contracts from approved model decisions.
4. Add semantic validators for cross-contract consistency.
5. Add resolver manifest/index/selector contracts.
6. Add generated read model or database projection.
7. Add controlled runtime behavior only after contract and validation foundations are approved.
8. Add panel, automation, runners, context packs, or write authorization only as explicitly scoped future work.

None of these phases are implemented in this issue.

## 22. Risks and Open Questions

Risks:

- Overloading `Workflow` with embedded behavior would weaken normalization.
- Reintroducing direct workflow or step ownership of execution behavior would duplicate Actor/Rol/Acción/Fuente/Evidencia/Límite/Regla relationships.
- Treating Markdown as contract data would create multiple human documentation surfaces and competing sources of truth.
- Copying GitHub live evidence into static contracts or docs would make traceability stale.
- Creating database state too early could invert the intended source-of-truth model.
- Under-specifying selectors could force AI agents to load too many contracts.
- Over-specifying selectors before implementation could prematurely lock in runtime behavior.
- Ambiguous boundaries between `Límite` and `Regla` could cause constraints and guidance to drift.

Open questions:

- What exact contract directory structure should be used when JSON contracts are introduced?
- How should `ResolverInput` and `ResolverOutput` be shaped when schemas are created?
- Which selector dimensions should be mandatory versus optional?
- What minimum evidence references should `Resolver` require through sources before a `WorkflowStep` can advance?
- How should PM approval be represented as `Evidencia` without becoming a separate approval entity?
- Which generated read model, if any, should be introduced first?
- What semantic validator language and execution environment should be approved?

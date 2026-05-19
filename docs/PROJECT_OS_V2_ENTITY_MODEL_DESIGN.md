# Project OS v2 Entity Model Design

## 1. Objective

Define the initial normalized Project OS v2 entity model and AI read flow as a human design/reference document.

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
- Do not create prompt and response as separate entities when `Plantilla` covers both.
- Do not create approval as a separate entity when it is `Evidencia`.
- Do not create context as a separate entity when it belongs to `Rol` or `Plantilla`.
- Do not create environment as a separate entity when `Actor` covers execution surface.
- Do not create policy as a separate entity when `Límite` and `Regla` cover constraints and behavior.

The design favors small contracts with explicit links over large contracts that embed adjacent concepts.

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
| `Resolver` | Entrada única para resolver qué contratos aplican a una solicitud. | Resolver identity, version, manifest reference, policy reference, input/output schema references, fallback state reference. | `id`, `nombre`, `descripción`, `versión`, `manifest_ref`, `policy_ref`, `input_schema_ref`, `output_schema_ref`, `fallback_estado_id` | Full workflows, actor permissions, evidence bodies, GitHub state snapshots, target-project artifacts. | A future resolver contract that routes an AI request to the minimal applicable contracts. |
| `Actor` | Superficie desde donde se ejecuta una acción y sus capacidades base. | Execution surface identity and base capability description. | `id`, `nombre`, `descripción`, `superficie_capacidad` | Permissions, workflow membership, role behavior, policy, or live environment state; these belong in `Límite`, `Regla`, and `Relación`. | A future actor contract representing an execution surface. |
| `Rol` | Lente profesional aplicado a una tarea. | Professional lens and role description used to interpret a task. | `id`, `nombre`, `descripción`, `lente_profesional` | Actor identity, permissions, evidence, workflow order, or prompt text that belongs to `Plantilla`. | A future role contract representing a professional review lens. |
| `Workflow` | Proceso iterable que coordina pasos, actores, roles, acciones, evidencia y estados. | Workflow identity, lifecycle stage, and workflow order. | `id`, `nombre`, `descripción`, `etapa_ciclo_vida`, `orden` | Embedded steps, required evidence, permissions, rules, limits, and output bodies; those are linked through `Relación`. | A future workflow contract for one lifecycle process. |
| `WorkflowStep` | Paso ordenado dentro de un workflow. | Step identity, order, objective, and advance/repeat/block conditions. | `id`, `nombre`, `descripción`, `orden`, `objetivo`, `condición_avance`, `condición_repetición`, `condición_bloqueo` | Workflow-level policy, actor permissions, evidence content, produced artifact content, or next-step embedding; these are related by `Relación`. | A future step contract for one ordered stage inside a workflow. |
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
| `Artefacto` | Resultado producido por una acción o workflow. | Artifact identity, type, name, and reference. | `id`, `tipo`, `nombre`, `referencia` | Producing step logic, template definition, resource definition, or validation state. | A future artifact contract/reference for a design document, generated report, PR body, or validation result. |
| `Relación` | Vínculo formal entre entidades. | Relationship identity, endpoints, relationship type, cardinality, required flag, and order. | `id`, `origen_entidad`, `origen_id`, `destino_entidad`, `destino_id`, `tipo_relación`, `cardinalidad`, `requerido`, `orden` | Duplicated attributes from either endpoint or embedded copies of related contracts. | A future relationship contract connecting a `WorkflowStep` to required `Evidencia` or next `WorkflowStep`. |
| `Contrato` | Especificación formal/versionable de una entidad o relación. | Contract identity, entity type, version, schema reference, and state. | `id`, `nombre`, `entidad_tipo`, `versión`, `schema_ref`, `estado` | Entity-specific attributes not belonging to the contract wrapper, live GitHub evidence, or generated database rows. | A future contract file that formalizes one entity or relationship version. |

## 8. Relationship Model

`Relación` is the normal form for cross-entity behavior. Any compatibility, permission, requirement, dependency, sequencing, restriction, reuse, or output link should be represented as a relationship instead of duplicated into entity contracts.

The main relationship model is:

| Relationship | Cardinality | Description |
| --- | ---: | --- |
| `Resolver` carga `Contrato` | 1:N | Un resolver usa varios contratos para resolver una solicitud. |
| `Resolver` determina `Estado` | 1:N | Un resolver puede devolver distintos estados según evidencia y límites. |
| `Contrato` formaliza Entidad | 1:N | Una entidad puede tener múltiples versiones de contrato. |
| `Workflow` contiene `WorkflowStep` | 1:N | Un workflow tiene uno o más pasos ordenados. |
| `Workflow` permite `Actor` | N:M | Varios actores pueden participar en varios workflows. |
| `Workflow` permite `Rol` | N:M | Varios roles pueden aplicar en varios workflows. |
| `Workflow` aplica `Límite` | N:M | Un workflow puede tener múltiples límites, y un límite puede reutilizarse. |
| `Workflow` aplica `Regla` | N:M | Un workflow puede usar múltiples reglas, y una regla puede reutilizarse. |
| `Workflow` produce `Estado` | N:M | Un workflow puede terminar en varios estados posibles. |
| `Workflow` usa `Plantilla` | N:M | Un workflow puede usar varias plantillas de salida. |
| `WorkflowStep` ejecuta `Acción` | N:1 | Muchos pasos pueden reutilizar una misma acción. |
| `WorkflowStep` requiere `Evidencia` | N:M | Un paso puede requerir varias evidencias. |
| `WorkflowStep` aplica `Límite` | N:M | Un paso puede tener límites propios o heredados. |
| `WorkflowStep` aplica `Regla` | N:M | Un paso puede tener reglas propias o heredadas. |
| `WorkflowStep` produce `Artefacto` | N:M | Un paso puede producir uno o más artefactos. |
| `WorkflowStep` avanza a `WorkflowStep` | N:M | Un paso puede tener siguiente paso, bifurcaciones o repetición. |
| `WorkflowStep` avanza a `Workflow` | N:M | Un paso final puede habilitar otro workflow. |
| `Actor` ejecuta `Acción` | N:M | Un actor puede ejecutar varias acciones si sus límites lo permiten. |
| `Actor` tiene `Límite` | N:M | Los límites del actor definen capacidad real. |
| `Rol` aplica `Regla` | N:M | Un rol puede tener reglas de conducta o criterio profesional. |
| `Acción` actúa sobre `Recurso` | N:M | Una acción puede operar sobre varios tipos de recurso. |
| `Acción` ocurre dentro de `Scope` | N:M | Una acción solo es válida dentro de un alcance. |
| `Scope` incluye `Recurso` | N:M | Un scope define qué recursos entran o quedan fuera. |
| `Fuente` provee `Evidencia` | 1:N | Una fuente puede producir muchas evidencias. |
| `Evidencia` refiere `Recurso` | N:M | Una evidencia puede apuntar a uno o más recursos. |
| `Límite` falla en `Estado` | N:1 | Si un límite se rompe, lleva a un estado como blocked. |
| `Regla` falla en `Estado` | N:1 | Si una regla no se cumple, lleva a un estado definido. |
| `Variable` parametriza `Plantilla` | N:M | Variables rellenan o modifican plantillas. |
| `Variable` parametriza `Workflow` | N:M | Variables pueden afectar idioma, repo, branch pattern, etc. |
| `Plantilla` genera `Artefacto` | 1:N | Una plantilla puede generar muchos artefactos. |
| `Artefacto` se asocia a `Recurso` | N:M | Un artefacto puede documentar o modificar recursos. |

## 9. Cardinality Model

Cardinality defines the allowed relationship shape, not embedded ownership.

- `1:N` means one source can point to many targets, while each relationship instance still remains explicit.
- `N:1` means many sources can reuse or converge on one target.
- `N:M` means both sides can participate in many relationships, and the relationship contract carries the meaning, requirement flag, and order.

The cardinality model keeps reusable concepts reusable. For example, a `Regla` can be applied to multiple `Workflow` and `WorkflowStep` contracts; a `Límite` can be shared by multiple actors or workflows; a `Plantilla` can generate multiple `Artefacto` records; and a `WorkflowStep` can advance to multiple next steps or workflows when branching or repetition is allowed.

## 10. Resolver as Single AI Read Entrypoint

The Resolver is the single read entrypoint for Project OS v2 behavior.

The `Resolver` is responsible for deciding which contracts apply to a request. AI agents should enter Project OS v2 through `Resolver`, not by scanning the entire contract library.

The `Resolver` should eventually load:

- a manifest or equivalent contract inventory
- policy/index references needed for routing
- selector definitions
- the applicable `Contrato` records
- related `Actor`, `Rol`, `Workflow`, `WorkflowStep`, `Límite`, `Regla`, `Plantilla`, `Variable`, `Fuente`, and `Evidencia` contracts
- relationship contracts needed to connect the selected set

The result is `ResolverOutput`: a minimal selected context that tells the AI what state applies, what workflow or step is active, what evidence is required or available, what limits/rules bind the response, and which template should structure the answer.

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

`Workflow` is an iterable software lifecycle process. It coordinates steps, actors, roles, actions, evidence, limits, rules, artifacts, templates, and states through relationships.

`WorkflowStep` is explicitly modeled as the ordered unit of workflow execution. A step must be able to describe:

- ordered step
- objective
- action
- required evidence
- limits
- rules
- produced artifacts
- condition to advance
- condition to repeat
- condition to block
- next `WorkflowStep`
- next `Workflow`

`WorkflowStep` owns only its normalized step attributes. It does not embed the action, evidence, limits, rules, artifacts, next step, or next workflow. Those are linked by `Relación`.

This makes a workflow iterable: a step can advance, repeat, block, branch to another step, or enable another workflow based on evidence, limits, rules, and state.

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
6. `Resolver` loads related `Actor`, `Rol`, `Workflow`, `WorkflowStep`, `Límite`, `Regla`, `Plantilla`, `Variable`, `Fuente`, and `Evidencia` contracts.
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
7. Resolve state through `Estado`, `Límite`, `Regla`, `Fuente`, and `Evidencia`.
8. Select `Plantilla` and `Variable` contracts needed for output.
9. Return a compact `ResolverOutput`.

The loading strategy should support generated indexes later, but the canonical information should remain in JSON contracts.

## 16. What Belongs in JSON Contracts

JSON contracts should contain stable, versionable structure:

- normalized entity attributes from the base model
- relationship endpoints and cardinality
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
- What minimum evidence references should be required before a `WorkflowStep` can advance?
- How should PM approval be represented as `Evidencia` without becoming a separate approval entity?
- Which generated read model, if any, should be introduced first?
- What semantic validator language and execution environment should be approved?

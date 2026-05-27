# Project OS v2 Foundation Design

## 1. Objective

Define the Project OS v2 foundation design as a human design/reference document for the active fixed roadmap. Project OS v2 is a contract-first operational coordination system that represents actors, roles, workflows, actions, resources, scopes, sources, evidence, states, limits, rules, variables, templates, artifacts, relationships, contracts, and Resolver entrypoints as normalized, versioned, inspectable contracts.

Project OS v2 coordinates operational work through contracts before runtime. It keeps one canonical owner per operational fact, derives effective context deterministically through Resolver inheritance, reduces AI context surface by selecting only applicable contracts and relationships, keeps GitHub as live evidence for issues, PRs, commits, reviews, validation, branch, and roadmap state, migrates proven Project OS behavior by normalization rather than copy-paste, certifies Project OS v2 Base v0.1 before dogfooding, and uses Base v0.1 to coordinate Project OS v2 work only after that certification.

This document is based on the PM-provided source files:

- `fuentes/Modelo-de-entidades-base.txt`
- `fuentes/Modelo-base-con-definiciones-y-atributos-normalizados.txt`
- `fuentes/Relaciones-principales-y-cardinalidad.txt`

## R0.01 Roadmap Rebaseline

The active fixed roadmap source is GitHub issue #92. Issue #47 is historical/provenance for the earlier fixed roadmap, issue #91 is completed roadmap rebaseline evidence, and issue #90 is open/paused tooling-readiness evidence. Future agents must not treat #47 as the active roadmap. GitHub remains live evidence, so issue, PR, branch, commit, review, validation, and roadmap state must be checked live when needed.

Current roadmap vocabulary:

- Bootstrap: Project OS v2 is still being built with guidance from `project-os` and PM/browser/terminal workflows.
- Migration: Project OS behavior is inventoried and mapped into normalized Project OS v2 families.
- Baseline population: Project OS v2 contracts are populated from approved migration mappings.
- Base v0.1: the first certified read-only Project OS v2 base that can coordinate Project OS v2 development itself.
- Dogfood: begins only after Project OS v2 Base v0.1 is certified dogfood-ready.
- Panel: a post-Base-v0.1 candidate surface, not part of the current fixed execution backlog.

Until Base v0.1 is certified dogfood-ready, Project OS v2 is still being built through project-os-supported bootstrap and migration. Migration, import, and baseline population issues must not be labeled as dogfood. Panel planning and implementation are intentionally excluded from the fixed backlog until Base v0.1 certification and dogfood pilot evidence justify them.

Stage-scoped permissions replace earlier ambiguous wording such as "do not create JSON contracts," "future contracts," or "no JSON yet":

- Planning issues do not create contracts.
- Docs issues may modify only approved docs.
- Contract population issues may create or update contracts only when explicitly scoped.
- Schema issues may create schemas only after schema strategy approval.
- Validator issues may create validators only after schema implementation.
- Loader, Resolver, runtime, panel, and write authorization remain blocked until their explicit roadmap IDs or later PM-approved roadmap amendments.

This R0.01 issue creates documentation only. It does not create contracts, schemas, validators, runtime behavior, parser behavior, automation, APIs, panels, runners, context packs, target-project artifacts, database/read-model direction, release behavior, template rendering behavior, variable interpolation behavior, generated-output behavior, body-file generation behavior, command execution behavior, or write authorization behavior.

## Current Fixed Roadmap Order

The fixed roadmap order from #92 is:

1. R0.01 docs rebaseline.
2. R0.02 roadmap hygiene.
3. R1 normalization audit, ownership policy, corrections, schemas, validators, and pre-migration validation readiness.
4. R2 project-os inventory, mapping, and migration plan.
5. R3 baseline limits, rules, states, and actor boundary relations.
6. R4 baseline roles, review/PM rules, evidence, and sources.
7. R5 baseline workflows, workflow steps, workflow composition, and terminal-agent workflow.
8. R6 baseline actions, resources, scopes, and action/resource/scope/evidence relations.
9. R7 baseline artifacts, templates, heredoc/body-file templates, variables, and template relations.
10. R10 post-migration baseline validation review and read-only loader.
11. R11 read-only Resolver.
12. R12 Base v0.1 dogfood-ready certification.
13. R13 dogfood pilot and pilot review.
14. R14 runtime/write-gate/automation planning only if PM approves.

Schemas and validators happen after normalization and before Project OS inventory, mapping, and migration. Migrated baseline contracts are reviewed with schemas and validators before loader or Resolver work. Panel work is not part of this fixed execution backlog and must not start before Base v0.1 certification and dogfood pilot evidence justify later PM approval.

## 2. Problem Statement

Project OS v2 needs a stable model that lets humans and AI agents reason about project behavior without loading every possible rule, workflow, role, source, and artifact at once. The model must support highly normalized contracts, explicit relationships, evidence-based decisions, and GitHub traceability while keeping static documentation separate from live operational state.

The core problem is not how to execute the system yet. The core problem is defining the entities, attributes, relationships, and read path that later implementations can validate, project, and execute without duplicating concepts across contracts.

## Operational Design Principles

Project OS v2 treats project work as a complex operation that must be organized from a normalized base structure. Its design starts by organizing complex project operations through explicit entities and relationships, anticipating logistical problems before execution instead of discovering every dependency inside runtime code.

The system assigns execution surfaces, professional lenses, resources, limits, rules, and workflows with precision through `Actor`, `Rol`, `Recurso`, `Límite`, `Regla`, `Workflow`, and `Relación`. It coordinates reusable `WorkflowStep` components across different project environments by composing them through `Relación`, so steps can be reused without copying workflow-specific order, delegation, evidence, or constraints into the step itself.

Execution plans should remain flexible when real evidence differs from the plan. Project OS v2 adapts through `Resolver`, `Estado`, `Evidencia`, and `Relación`, not through hardcoded behavior. This is an operational design principle, not a new model entity.

The immediate implementation direction is the #92 staged roadmap: docs rebaseline, roadmap hygiene, normalization audit and ownership policy, schema and validator readiness, then Project OS inventory/mapping/migration. Runtime behavior, parser behavior, automation, APIs, panels, context packs, target-project artifacts, database/read-model direction, write authorization behavior, loader work, and Resolver behavior remain blocked until their explicit roadmap IDs or later PM-approved roadmap amendments.

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

- JSON contracts are the canonical stable structure for entities and relationships once contract population issues explicitly scope them.
- The immediate next direction is R0.02 roadmap hygiene, then R1 normalization audit, ownership policy, corrections, schemas, validators, and pre-migration validation readiness.
- JSON Schema work happens only after schema strategy approval and after normalization decisions are ready to validate.
- Semantic validators happen only after schema implementation and within explicitly scoped validator issues.
- Runtime behavior, parser behavior, automation, APIs, panels, runners, context packs, target-project artifacts, database/read-model direction, loader work, Resolver behavior, and write authorization behavior are blocked until their explicit roadmap IDs or later PM-approved roadmap amendments.
- Markdown is only for human design/reference.
- GitHub issues, PRs, commits, comments, reviews, tags, and validation outputs are live evidence.

The source of truth direction is: normalized contracts for stable operational structure once explicitly populated, live GitHub evidence for operational traceability, and Markdown for explanation. Storage and execution implementation concerns are outside this foundational design issue.

## 5. Normalization Principles

Project OS v2 preserves maximum normalization.

Required rule: entities store their own attributes. Compatibility, permission, requirement, dependency, sequencing, and restriction live in `Relación`.

Normalization model:

- 1NF: payloads are atomic enough for machine reading.
- 2NF: each family owns only its own facts.
- 3NF: no duplicated transitive facts.
- Canonical ownership: every operational fact has exactly one canonical owner.
- Relationship ownership: `Relación` owns cross-entity graph semantics.
- Actor boundary rule: actor-level limits must not be duplicated into workflows, actions, templates, artifacts, or roles.
- Role lens rule: `Rol` is a professional lens only and never grants write permission.
- Template authority rule: `Plantilla` owns output shape, format, and body conventions, not permission.
- Durable evidence rule: durable JSON must not store mutable GitHub truth.

Normalization boundaries:

- Do not duplicate permissions inside `Actor` if they are expressed by `Límite` or `Relación`.
- Do not duplicate required evidence inside `Workflow` if it is expressed by `Relación`.
- Do not duplicate execution behavior inside `Workflow` or `WorkflowStep` if it is resolved through `Actor`, `Rol`, `Acción`, `Fuente`, `Evidencia`, `Límite`, `Regla`, and `Relación`.
- Do not duplicate actor-level limits inside `Workflow`, `Acción`, `Plantilla`, `Artefacto`, or `Rol`.
- Do not create prompt and response as separate entities when `Plantilla` covers both.
- Do not create approval as a separate entity when it is `Evidencia`.
- Do not create context as a separate entity when it belongs to `Rol` or `Plantilla`.
- Do not create environment as a separate entity when `Actor` covers execution surface.
- Do not create policy as a separate entity when `Límite` and `Regla` cover constraints and behavior.

The design favors small contracts with explicit links over large contracts that embed adjacent concepts.

Execution behavior is resolved from `Actor` + `Rol` + `Acción` + `Límite` + `Regla` + `Fuente` + `Evidencia` through `Relación`. `Workflow` defines lifecycle/process composition. `WorkflowStep` defines reusable step identity, objective, base conditions, Actor/Rol delegation, transition logic, and expected artifacts. `Resolver` composes relationships and determines `Estado`.

If an `Actor` has a `Límite`, and a `Workflow` uses that `Actor`, the `Workflow` must not duplicate that actor-level `Límite`. The `Resolver` derives it from the selected actor and relationship graph.

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

Each base entity should become a versionable JSON contract only when a later contract population issue explicitly scopes that work. This document does not create those contracts.

## Canonical Ownership by Family

Canonical ownership for the 18 base entity families:

| Family | Canonical ownership |
| --- | --- |
| `Resolver` | Single AI read entrypoint identity, selected-context resolution boundary, manifest/policy/schema reference pointers, and fallback state reference. |
| `Actor` | Execution surface identity and base capability description. Actor hard limits are linked through `Relación` to `Límite` and must not be copied into workflows, actions, templates, artifacts, or roles. |
| `Rol` | Professional lens and review/interpretation perspective. A role never grants write permission. |
| `Workflow` | Lifecycle/process identity and composition boundary. It does not own actor limits, role permissions, action execution, evidence bodies, or template output shape. |
| `WorkflowStep` | Reusable process-block identity, objective, and base advance/repeat/block conditions. Workflow-specific order, required state, delegated actor/role, expected artifacts, and next-step links live in `Relación`. |
| `Acción` | Concrete operation identity and action type. Execution authority comes from selected actor limits, scope, resource, evidence, and relationships. |
| `Recurso` | Object being acted on, including resource type, name, and stable location/reference. |
| `Scope` | Permitted task boundary. Scope does not grant actor permission by itself. |
| `Fuente` | Authority/source category, location, authority level, and freshness requirement. It does not store mutable evidence observations. |
| `Evidencia` | Evidence reference shape and verification metadata. Durable evidence contracts must not store mutable GitHub truth. |
| `Estado` | State identity and meaning. Rules, limits, and evidence that cause a state remain separate. |
| `Límite` | Mandatory boundary, type, and severity. Actor-level limits are inherited by Resolver and are not duplicated into lower layers. |
| `Regla` | Conditional guidance and expected behavior. Rules do not replace hard limits or permissions. |
| `Variable` | Configurable data shape, defaults, and allowed values for templates or workflows. Variables do not perform interpolation. |
| `Plantilla` | Output shape, format, required sections, and body conventions. A template does not grant permission and does not implement rendering. |
| `Artefacto` | Expected or produced artifact identity, type, name, and reference. Artifact contracts do not own template definitions or producing logic. |
| `Relación` | Cross-entity graph semantics: compatibility, permission, requirement, dependency, sequencing, restriction, delegation, composition, and output links. |
| `Contrato` | Formal/versionable wrapper identity for an entity or relationship contract, including version, schema reference, and lifecycle state. |

Policy, manifest, index, and selector are non-entity static support bundles. They are not members of the 18 base entity families. They support Resolver discovery/reference behavior and must not implement runtime behavior, selector runtime, contract loader behavior, write authorization, or duplicated entity facts.

## 7. Entity Attributes

| Entity | Definition | Owns | Normalized attributes | Must not own | Examples |
| --- | --- | --- | --- | --- | --- |
| `Resolver` | Entrada única para resolver qué contratos aplican a una solicitud. | Resolver identity, version, manifest reference, policy reference, input/output schema references, fallback state reference. | `id`, `nombre`, `descripción`, `versión`, `manifest_ref`, `policy_ref`, `input_schema_ref`, `output_schema_ref`, `fallback_estado_id` | Full workflows, actor permissions, evidence bodies, GitHub state snapshots, target-project artifacts, or duplicated relationship decisions. | A future resolver contract that composes relationships and routes an AI request to the minimal applicable contracts. |
| `Actor` | Superficie desde donde se ejecuta una acción y sus capacidades base. | Execution surface identity and base capability description. | `id`, `nombre`, `descripción`, `superficie_capacidad` | Permissions, workflow membership, role behavior, policy, or live environment state; these belong in `Límite`, `Regla`, and `Relación`. | A future actor contract representing an execution surface. |
| `Rol` | Lente profesional aplicado a una tarea. | Professional lens and role description used to interpret a task. | `id`, `nombre`, `descripción`, `lente_profesional` | Actor identity, permissions, evidence, workflow order, or prompt text that belongs to `Plantilla`. | A future role contract representing a professional review lens with related rules and templates. |
| `Workflow` | Proceso iterable que define orden de proceso y etapa del ciclo de vida. | Workflow identity, lifecycle stage, and process composition. | `id`, `nombre`, `descripción`, `etapa_ciclo_vida`, `orden` | Actor/role execution behavior, direct actions, direct evidence, direct limits, direct rules, or resolver-derived state. | A future workflow contract for one lifecycle process assembled from reusable steps. |
| `WorkflowStep` | Bloque reutilizable de proceso usado dentro de workflows. | Reusable step identity, objective, and base advance/repeat/block conditions. | `id`, `nombre`, `descripción`, `objetivo`, `condición_base_avance`, `condición_base_repetición`, `condición_base_bloqueo` | Direct action execution, evidence ownership, direct limits, direct rules, actor capability, role rules, produced artifact content, or workflow-specific sequencing values. | A future reusable process block that delegates to `Actor` and `Rol` through relationships. |
| `Acción` | Operación concreta que se quiere realizar. | Action identity and action type. | `id`, `nombre`, `descripción`, `tipo` | Actor identity, resource details, scope, evidence, or execution result. | A future action contract for a concrete operation such as inspect, create, validate, or review. |
| `Recurso` | Objeto sobre el que actúa una acción. | Resource identity, type, name, and location. | `id`, `tipo`, `nombre`, `ubicación` | Action semantics, scope membership, evidence verification state, or artifact composition rules. | A future resource contract pointing to a file path, issue, PR, commit, tag, or external reference. |
| `Scope` | Alcance permitido de una tarea. | Scope identity and allowed task boundary description. | `id`, `nombre`, `descripción` | Resources by value, action permissions, actor capability, or workflow order. | A future scope contract representing the allowed boundary of a task. |
| `Fuente` | Origen de autoridad o verdad. | Source identity, type, location, authority level, and freshness requirement. | `id`, `tipo`, `nombre`, `ubicación`, `nivel_autoridad`, `frescura_requerida` | Evidence observations, verification state, resource ownership, or workflow decisions. | A future source contract for an authoritative origin such as a PM file or live GitHub object category. |
| `Evidencia` | Información verificable usada para decidir o validar. | Evidence identity, type, reference, verification state, and observation timestamp. | `id`, `tipo`, `referencia`, `estado_verificación`, `observado_en` | Source authority, workflow policy, approval as an entity, or static copies of mutable GitHub state. | A future evidence contract/reference for an observed issue, PR, commit, review, validation output, or source file observation. |
| `Estado` | Resultado de resolución o ejecución. | State identity and meaning. | `id`, `nombre`, `descripción` | The rules that cause the state, the evidence that proves it, or generated response text. | A future state contract such as applicable, blocked, needs-evidence, validated, or ready-for-review. |
| `Límite` | Restricción obligatoria que no debe romperse. | Limit identity, type, severity, and constraint description. | `id`, `nombre`, `descripción`, `tipo`, `severidad` | Actor permissions by embedding, workflow membership, rule behavior, or failure evidence. | A future limit contract defining a hard boundary. |
| `Regla` | Norma que guía conducta o decisión. | Rule identity, condition, and expected behavior. | `id`, `nombre`, `descripción`, `condición`, `comportamiento_esperado` | Limit severity, actor identity, workflow order, evidence payloads, or static GitHub traceability. | A future rule contract defining expected behavior under a condition. |
| `Variable` | Dato dinámico configurable. | Variable identity, type, default value, and allowed values. | `id`, `nombre`, `tipo`, `valor_default`, `valores_permitidos` | Template bodies, workflow definitions, live runtime values, or validator behavior. | A future variable contract parameterizing a template or workflow. |
| `Plantilla` | Estructura reusable para componer prompts, respuestas, reportes o bodies como formato esperado. | Template identity, type, format, required sections, and body conventions. | `id`, `nombre`, `tipo`, `formato`, `secciones_requeridas` | Variable definitions, workflow eligibility, live evidence state, permission, runtime rendering, interpolation, or separate prompt/response entities. | A future template contract for a response, prompt, report, or PR body structure. |
| `Artefacto` | Resultado referenciable esperado por un paso o asociado a una acción/plantilla. | Artifact identity, type, name, and reference. | `id`, `tipo`, `nombre`, `referencia` | Producing step logic, template definition, resource definition, rendering behavior, or validation state. | A future artifact contract/reference for a design document, report, PR body, or validation result. |
| `Relación` | Vínculo formal entre entidades para compatibility, permission, requirement, dependency, sequencing, or restriction semantics. | Relationship identity, endpoints, relationship type, cardinality, required flag, and order. | `id`, `origen_entidad`, `origen_id`, `destino_entidad`, `destino_id`, `tipo_relación`, `cardinalidad`, `requerido`, `orden` | Duplicated attributes from either endpoint or embedded copies of related contracts. | A future relationship contract that composes workflow steps, delegates `Actor`/`Rol`, expects `Artefacto`, or points to the next step. |
| `Contrato` | Especificación formal/versionable de una entidad o relación. | Contract identity, entity type, version, schema reference, and state. | `id`, `nombre`, `entidad_tipo`, `versión`, `schema_ref`, `estado` | Entity-specific attributes not belonging to the contract wrapper, live GitHub evidence, or generated implementation state. | A future contract file that formalizes one entity or relationship version. |

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
| Workflow compone WorkflowStep | N:M | Un workflow compone bloques reutilizables de proceso. |
| Workflow ordena WorkflowStep | N:M | Un workflow ubica sus pasos mediante relación. |
| Workflow avanza a Workflow | N:M | Un workflow puede habilitar otro workflow dentro del ciclo de vida. |
| Workflow usa Plantilla | N:M | Un workflow puede usar plantillas para salidas o reportes de proceso. |
| WorkflowStep participa en Workflow | N:M | Un bloque reutilizable puede participar en varios workflows. |
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
| Plantilla compone Artefacto | 1:N | Una plantilla puede definir la forma de muchos artefactos sin implementar generación, rendering, interpolation, body-file generation, or generated-output behavior. |
| Artefacto se asocia a Recurso | N:M | Un artefacto puede documentar o modificar recursos. |

Current Project OS v2 semantics use `plantilla compone artefacto`. Old `plantilla genera artefacto` language is historical/provenance or reserved legacy wording only; it must not be read as runtime generation, template rendering, variable interpolation, body-file generation, generated-output behavior, or permission.

## Relationship Normalization Correction

This correction removes direct process-to-execution ownership from the model.

- Workflow does not own actor/role execution behavior.
- Workflow does not own limits/rules directly.
- WorkflowStep does not execute actions directly.
- WorkflowStep does not own evidence directly.
- WorkflowStep delegates Actor and Rol.
- WorkflowStep owns reusable objective and base repeat/block/advance conditions.
- Actor relationships define execution surface, available actions, limits, and sources.
- Rol relationships define professional lens, rules, compatible actors, and templates.
- Resolver composes relationships to determine applicable action, evidence, limits, rules, state, and output.

The rationale is that `Workflow` defines lifecycle sequencing and composition while reusable step blocks define objective and base transition semantics. `Actor` and `Rol`, plus their related entities, define how work is executed. This keeps the model reusable, scalable, normalized, and maintainable.

## Reusable WorkflowStep Composition

WorkflowStep is a reusable process block.

- WorkflowStep can be used by multiple Workflows.
- Workflow composes WorkflowSteps through Relación.
- The order of a WorkflowStep inside a Workflow is not owned by WorkflowStep.
- The order is stored in Relación.orden.
- El orden específico del workflow vive en Relación.orden.
- WorkflowStep delegates Actor and Rol.
- A WorkflowStep can be reused with different order, required flag, delegated Actor, delegated Rol, expected Artefacto, and transition conditions depending on the Workflow.
- WorkflowStep is analogous to a reusable puzzle piece.
- Workflow is the assembled puzzle for a specific software lifecycle process.

Workflow is lifecycle/process composition. WorkflowStep is the reusable process block being composed. Workflow-specific order lives in Relación, not in WorkflowStep. Workflow-specific required/optional state lives in `Relación.requerido`. Workflow-specific transition order lives in `Relación` between `Workflow`, `WorkflowStep`, and the next `WorkflowStep`. Workflow-specific Actor/Rol delegation can also be represented through `Relación`. Base conditions on WorkflowStep are generic defaults, not workflow-specific truth.

Conceptual example:

`workflow.design` may compose:

- `workflow_step.preflight`
- `workflow_step.investigation`
- `workflow_step.base_design`
- `workflow_step.human_qa_checklist`

`workflow.implementation` may compose:

- `workflow_step.preflight`
- `workflow_step.implementation`
- `workflow_step.validation`
- `workflow_step.review_before_close`

The same `workflow_step.preflight` can be reused in both workflows with different order and delegated Actor/Rol through Relación.

## 9. Cardinality Model

Cardinality defines the allowed relationship shape, not embedded ownership.

- `1:N` means one source can point to many targets, while each relationship instance still remains explicit.
- `N:1` means many sources can reuse or converge on one target.
- `N:M` means both sides can participate in many relationships, and the relationship contract carries the meaning, requirement flag, and order.

The cardinality model keeps reusable concepts reusable. For example, a `Regla` can be applied to multiple `Rol` contracts; a `Límite` can be shared by multiple actors; a `Fuente` can provide many `Evidencia` references; a `Plantilla` can compose the expected shape of multiple `Artefacto` records; and a `WorkflowStep` can delegate multiple actors or roles, expect multiple artifacts, and advance to multiple next steps or workflows when branching or repetition is allowed.

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

Deterministic Resolver inheritance order:

1. Actor hard limits.
2. Actor output boundaries.
3. Role lens constraints.
4. Workflow requirements.
5. WorkflowStep requirements.
6. Action/resource/scope requirements.
7. Evidence/source requirements.
8. Template/artifact output shape.
9. State/failure rules.

No lower layer may weaken an Actor hard limit. `ResolverOutput` materializes effective inherited context and should include source/provenance refs for effective facts. Future panel surfaces, if approved later, must consume `ResolverOutput`/effective context and must not reconstruct scattered rules from duplicated fields.

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

`Workflow` is an iterable software lifecycle process. It owns lifecycle stage and process composition. It does not own execution behavior; execution is resolved by `Resolver` through reusable step composition, delegation, and related actors, roles, actions, sources, evidence, limits, rules, templates, artifacts, and states.

`WorkflowStep` is explicitly modeled as a reusable process block. A step must be able to describe:

- objective
- base condition to advance
- base condition to repeat
- base condition to block
- delegated `Actor`
- delegated `Rol`
- expected artifacts
- next `WorkflowStep`
- next `Workflow`

`WorkflowStep` owns only its normalized reusable attributes: identity, objective, and base transition conditions. It delegates `Actor` and `Rol` through `Relación`. It does not embed action execution, evidence ownership, limits, rules, artifact content, next step, next workflow, or workflow-specific sequencing. Those are linked by `Relación` and composed by `Resolver`.

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

## Base v0.1 Definition

Base v0.1 is the first certified read-only Project OS v2 base usable to coordinate Project OS v2 development itself. It is not dogfood until certification is complete.

Base v0.1 includes:

- normalized contracts
- canonical ownership
- deterministic Resolver inheritance
- migrated operational behavior from `project-os` as normalized contract data
- reference validation
- schema coverage for contract shapes
- validator coverage for schema, reference, and ownership checks
- read-only contract loader
- read-only `ResolverOutput` / effective context
- prompt, command, review, and PM decision drafting support

Base v0.1 excludes:

- autonomous writes
- merge automation
- issue closure automation
- destructive panel actions
- target-project automation
- write authorization runtime
- direct Project OS copy-paste imports
- panel implementation

Dogfood begins only after Project OS v2 Base v0.1 is certified dogfood-ready. Project OS v2 Base v0.1 may coordinate Project OS v2 work using Project OS v2 itself only after certification.

## Project OS to Project OS v2 Migration Policy

Project OS behavior is source evidence, not structure to copy directly. Migration must happen in granular clusters, and each behavior must map to exactly one canonical owner.

Migration ownership rules:

- Actor-level behavior stays actor-level.
- Browser-chat no-write/copy-safe behavior belongs to Actor/Límite or Actor/Regla relations, not workflows, actions, or templates.
- Heredoc and multiline body conventions belong to Plantilla/Formato and do not grant permission.
- Branch preflight belongs to workflow/evidence/status gates.
- Review quality belongs to role/workflow/evidence/output contracts.
- Source authority belongs to Fuente/Evidencia.
- Output shape belongs to Plantilla/Artefacto/Variable as applicable.

Direct Project OS copy-paste imports are excluded from Base v0.1. Proven behavior must be normalized into the Project OS v2 ownership and relationship model before baseline population.

## 15. Contract Loading Strategy

Contract loading should be minimal, layered, and relationship-aware when read-only loader work is explicitly scoped. This section is conceptual design only; it does not create contract loader behavior, Resolver behavior, generated indexes, selector runtime, parser behavior, runtime behavior, or write authorization.

Conceptual later reference flow:

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

The loading strategy may support generated indexes only if a later roadmap item explicitly scopes that work, but canonical information should remain in JSON contracts.

## 16. What Belongs in JSON Contracts

JSON contracts should contain stable, versionable structure:

- normalized entity attributes from the base model
- relationship endpoints and cardinality
- normalized delegation, compatibility, requirement, dependency, sequencing, and restriction relationships
- schema references after schema strategy approval
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
- live branch state copied as static data
- live roadmap state copied as static data
- commit review status copied as static data
- validation output bodies copied as canonical facts
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
- branches and branch state
- roadmap state
- references to changed files or generated artifacts

GitHub should remain the live evidence layer for execution, review, readiness, release, validation, branch, and roadmap state. Static docs and durable JSON should not encode live GitHub traceability as if it were canonical system state. `Fuente` and `Evidencia` contracts are stable references/categories, not live snapshots; issue, PR, branch, commit, review, validation, and roadmap state must be checked live when needed.

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

## 20. Roadmap Execution Boundary

The active fixed roadmap is #92, not #47. The next roadmap item after R0.01 is R0.02 roadmap hygiene.

Roadmap execution must preserve these order constraints:

- Schemas and validators happen after normalization and before Project OS inventory, mapping, and migration.
- Project OS behavior is inventoried and mapped before baseline contracts are populated.
- Migrated baseline contracts are reviewed with schemas and validators before loader or Resolver work.
- Loader work starts at R10 only after post-migration baseline validation review.
- Resolver work starts at R11 only after read-only loader readiness.
- Base v0.1 certification is R12.
- Dogfood pilot starts at R13 only after Base v0.1 certification.
- Runtime/write-gate/automation planning is R14 only if PM approves.
- Panel is outside the fixed execution backlog and must not be implied before Base v0.1 certification.

None of that later work is implemented in this issue.

## 21. Risks and Open Questions

Risks:

- Overloading `Workflow` with embedded behavior would weaken normalization.
- Reintroducing direct workflow or step ownership of execution behavior would duplicate Actor/Rol/Acción/Fuente/Evidencia/Límite/Regla relationships.
- Treating Markdown as contract data would create multiple human documentation surfaces and competing sources of truth.
- Copying GitHub live evidence into static contracts or docs would make traceability stale.
- Under-specifying selectors could force AI agents to load too many contracts.
- Over-specifying selectors before implementation could prematurely lock in runtime behavior.
- Ambiguous boundaries between `Límite` and `Regla` could cause constraints and guidance to drift.

Open questions:

- What exact contract directory structure should be used when JSON contracts are introduced?
- How should `ResolverInput` and `ResolverOutput` be shaped when schemas are created?
- Which selector dimensions should be mandatory versus optional?
- What minimum evidence references should `Resolver` require through sources before a `WorkflowStep` can advance?
- How should PM approval be represented as `Evidencia` without becoming a separate approval entity?
- What semantic validator language and execution environment should be approved?

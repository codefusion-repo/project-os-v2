# Project OS v2 Resolver Contract Shape

## 1. Objective

Define the structure-only shape for future Project OS v2 `ResolverInput` and `ResolverOutput` contracts.

This document decides what information the future Resolver input should carry and what selected-context references the future Resolver output should return. It does not create JSON contract files, populated contract data, JSON schemas, validators, runtime behavior, parser behavior, automation, API, panel, runners, context packs, target-project artifacts, database/read-model direction, write authorization behavior, or Resolver behavior.

## 2. Scope

This issue is documentation-only and structure-only.

It defines future static shapes for:

1. `ResolverInput`
2. `ResolverOutput`
3. Resolver input classification fields
4. Resolver output selected-context fields
5. evidence requirement references
6. relationship expansion references
7. `Estado` / status reference handling
8. boundary and failure shape
9. no-runtime and no-behavior boundaries
10. relationship to the approved structure, envelope, and skeleton pattern documents

The shapes in this document are not contract instances. They are field-group decisions that later issues may convert into reviewed contract skeletons or schema references only after that work is explicitly scoped.

## 3. Relationship to foundation / structure / envelope / skeleton docs

This document depends on and preserves:

- `docs/PROJECT_OS_V2_FOUNDATION_DESIGN.md`
- `docs/PROJECT_OS_V2_CONTRACT_STRUCTURE.md`
- `docs/PROJECT_OS_V2_CONTRACT_ENVELOPE.md`
- `docs/PROJECT_OS_V2_CONTRACT_SKELETON_PATTERNS.md`
- `fuentes/Modelo-de-entidades-base.txt`
- `fuentes/Modelo-base-con-definiciones-y-atributos-normalizados.txt`
- `fuentes/Relaciones-principales-y-cardinalidad.txt`

Foundation decisions preserved here:

- `Resolver` is the future single AI read entrypoint.
- `ResolverInput` is the request classification shape used before selected contracts are known.
- `ResolverOutput` is the minimal selected context returned after future contract selection.
- `Relación` owns compatibility, permission, requirement, dependency, sequencing, and restriction.
- `Estado` represents the result of resolution or execution.
- `Evidencia` stores evidence references and verification shape, not copied mutable GitHub state.
- GitHub remains live evidence for issues, PRs, commits, comments, reviews, tags, and validation outputs.
- Markdown remains human design/reference until equivalent reviewed contracts exist.

Structure decisions preserved here:

- Future contract root remains `contracts/`.
- Future file shape remains `contracts/<entity_family>/<contract_id>.json`.
- Future ID shape remains `<entity_family>.<slug>.v<major>`.
- Future relationship contracts remain under `contracts/relacion/`.
- Future `Estado` contracts remain under `contracts/estado/`.
- Future `Evidencia` contracts remain under `contracts/evidencia/`.
- This document does not define manifest shape, index shape, selector shape, or contract loader behavior.

Envelope decisions preserved here:

- Future contracts use the common envelope fields `id`, `entity_family`, `contract_kind`, `version`, `status`, `schema_ref`, `descripcion`, `source_refs`, and `payload`.
- Envelope metadata and payload data must not duplicate each other.
- Entity-owned attributes live in `payload`.
- Relationship endpoints and relationship semantics live in `payload`.
- `schema_ref` remains a reference only until schemas are explicitly approved.

Skeleton decisions preserved here:

- Future skeleton values must be placeholder-safe.
- Future skeleton examples must be non-canonical.
- `version` uses object form such as `{ "major": 1 }` when actual skeletons are approved.
- Envelope `descripcion` owns contract-level description.
- Markdown design docs are scaffolding until reviewed JSON contracts exist.

## 4. Resolver contract shape purpose

The Resolver contract shape defines the boundary between an incoming request and the minimal selected context needed to answer it.

`ResolverInput` should carry enough classification information for a future Resolver to select the minimum required contracts later. It should not carry the whole target project, copied GitHub evidence, full issue bodies, full PR bodies, implementation logs, or inferred permissions.

`ResolverOutput` should return selected references only. It should tell the AI which selected contracts and relationships apply, which evidence references are required or missing, which boundary notes apply, and which output or response shape should be used. It should not embed full entity contracts, relationship bodies, live evidence bodies, or execution behavior.

This document defines shape only. It does not define a parser, selector algorithm, loading order, routing implementation, scoring model, execution rule, or response-generation behavior.

## 5. ResolverInput shape

`ResolverInput` is the future request classification shape. It should be small, explicit, and reference-oriented.

The field groups below are recommended structural groups. Field names are shape candidates, not populated data and not final JSON contract content.

| Field group | Candidate fields | Purpose | Boundary |
| --- | --- | --- | --- |
| request identity | `resolver_input_id`, `request_ref`, `correlation_ref` | Identify the input record or live request reference. | Do not encode mutable branch state, timestamps, issue state, or copied request bodies as static contract data. |
| current actor surface | `current_actor_ref`, `current_actor_surface_token` | Describe the actor surface currently making or carrying the request. | This is classification context only; it does not grant permission and does not hardcode a real Actor. |
| requested intent | `requested_intent_ref`, `requested_action_hint`, `lifecycle_hint` | Classify what the request is asking for so a future Resolver can select candidate contracts. | Hints do not execute actions, choose workflows, or bypass limits. |
| target repository or project reference | `target_project_ref`, `repository_ref`, `branch_ref` | Point to the target project or repository context when needed. | Keep GitHub and branch state live; do not copy mutable repository state. |
| issue / PR / resource references | `issue_refs`, `pr_refs`, `resource_refs` | Point to live or static resources mentioned by the request. | References only; no issue body, PR body, review text, commit metadata, validation output, or file content is copied. |
| requested output shape | `requested_output_contract_ref`, `response_shape_ref`, `output_template_hint` | Tell the future Resolver what response/report/PR-body shape is requested. | This does not select a `Plantilla` by behavior; final selection stays in `ResolverOutput`. |
| available evidence references | `available_evidence_refs`, `available_source_refs` | Carry evidence references already known to the caller. | Evidence remains referenced, not embedded. GitHub remains live evidence. |
| PM-provided scope | `pm_scope_ref`, `pm_scope_boundary_refs`, `pm_scope_notes_ref` | Preserve PM-scoped boundaries or authoritative scope references. | Do not turn PM text into populated contract data or copied issue-body evidence. |
| optional target actor | `target_actor_ref` | Optional target actor only when the request explicitly routes or delegates. | Null or absent unless routing/delegating is part of the request; it is not a permission grant. |
| optional requested role | `requested_role_ref`, `requested_role_hint` | Optional requested role only as a classification hint. | A requested role is not authority, permission, or proof of compatibility. |
| language / variable hints | `language_hint`, `variable_hints` | Carry language, formatting, or variable-selection hints when needed. | Hints do not populate `Variable` contracts and do not override selected `Plantilla` references. |

`ResolverInput` classification should be explicit enough for later manifest, index, or selector shape work to use without rereading all Markdown design docs. It should remain incomplete enough to avoid hardcoding real actors, roles, workflows, rules, limits, sources, evidence, statuses, or routing behavior.

## 6. ResolverOutput shape

`ResolverOutput` is the future selected-context shape. It should return the minimum reference set needed for an AI response or next contract-aware step.

The field groups below are recommended structural groups. Field names are shape candidates, not populated data and not final JSON contract content.

| Field group | Candidate fields | Purpose | Boundary |
| --- | --- | --- | --- |
| resolver result identity | `resolver_output_id`, `resolver_input_ref`, `resolver_ref`, `resolution_ref` | Identify the output and link it back to the input and future Resolver contract. | Does not imply a runtime trace or execution log. |
| selected status / Estado | `status_token`, `estado_ref`, `fallback_estado_ref` | Carry the selected status token and future `Estado` reference. | Status token is structural and non-canonical until approved `Estado` contracts exist. |
| selected Actor references | `selected_actor_refs` | Reference selected Actor contracts. | Do not copy actor capabilities or permissions into output. |
| selected Rol references | `selected_rol_refs` | Reference selected Rol contracts. | Do not treat requested role hints as permission. |
| selected Workflow references | `selected_workflow_refs` | Reference selected Workflow contracts. | Do not flatten workflow composition or execution behavior. |
| selected WorkflowStep references | `selected_workflow_step_refs` | Reference selected reusable step contracts. | Do not copy workflow-specific order into the step reference. |
| selected Acción references | `selected_accion_refs` | Reference selected action contracts. | Do not execute the action. |
| selected Recurso references | `selected_recurso_refs` | Reference selected resource contracts or resource references. | Do not copy target file contents or live resource state. |
| selected Scope references | `selected_scope_refs` | Reference selected scope contracts. | Do not expand scope into embedded resource lists unless a later issue allows it. |
| selected Fuente references | `selected_fuente_refs` | Reference selected source contracts. | Do not copy source contents or live source state. |
| selected Evidencia references | `selected_evidencia_refs` | Reference selected evidence contracts or live evidence references. | Do not copy issue bodies, PR bodies, comments, reviews, commits, validation output, or branch state. |
| selected Límite references | `selected_limite_refs` | Reference selected limit contracts. | Do not copy limit behavior into actor, role, workflow, or step fields. |
| selected Regla references | `selected_regla_refs` | Reference selected rule contracts. | Do not execute or evaluate rules here. |
| selected Variable references | `selected_variable_refs` | Reference selected variable contracts. | Do not store live runtime variable values as static contract data. |
| selected Plantilla references | `selected_plantilla_refs` | Reference selected template contracts. | Do not copy prompt, response, report, or PR body content into ResolverOutput. |
| selected Artefacto references | `selected_artefacto_refs` | Reference selected expected or produced artifact contracts. | Do not create target-project artifacts. |
| selected Relación references | `selected_relations`, `selected_relacion_refs` | Reference selected relationship contracts used to connect selected context. | Do not embed full relationship bodies or flatten relationship semantics. |
| selected Contrato references | `selected_contrato_refs` | Reference contract records considered applicable. | Do not return every contract in the library. |
| evidence requirements | `required_evidence_refs`, `missing_evidence_refs` | Identify evidence references required for the selected state or next step and which are missing. | References only; no live evidence collection behavior. |
| boundary notes | `boundary_note_refs`, `boundary_notes` | Carry structural notes about preserved boundaries. | Notes must not authorize writes or encode runtime decisions. |
| output template reference | `output_template_ref` | Point to the output template selected for a response/report/body. | Reference only; no template expansion behavior. |
| response shape reference | `response_shape_ref` | Point to the intended response shape or output contract. | Reference only; no formatter implementation. |
| next-step recommendation | `next_step_recommendation` | Carry the next-step recommendation as data shape only. | It is not routing, automation, workflow composition, or execution. |

`ResolverOutput` should be compact. It should carry references to selected `Actor`, `Rol`, `Workflow`, `WorkflowStep`, `Acción`, `Recurso`, `Scope`, `Fuente`, `Evidencia`, `Estado`, `Límite`, `Regla`, `Variable`, `Plantilla`, `Artefacto`, `Relación`, and `Contrato` only when needed by the selected context.

## 7. Estado / status reference handling

Decision: `ResolverOutput` should carry both a small `status_token` and an `estado_ref`, with `estado_ref` treated as the future canonical reference when `Estado` contracts exist.

Rationale:

- `estado_id` / `estado_ref` alone would be too rigid before reviewed `Estado` contracts exist.
- A small status token alone would risk becoming an accidental hardcoded state system.
- Carrying both lets early shape work remain placeholder-safe while preserving the future contract reference boundary.

Rules:

- `estado_ref` points to a future `Estado` contract under `contracts/estado/`.
- `status_token` is a structural classification token only.
- `status_token` must not define real `Estado` content.
- When `estado_ref` is populated in a later approved issue, it is the authoritative selected state reference.
- If `status_token` and `estado_ref` ever conflict, a later validation or review issue must decide the correction; this document does not create validators.
- `fallback_estado_ref` may point to a future fallback `Estado` reference when selected context is incomplete.

Example status names in this document are intentionally avoided except for placeholder tokens such as `example_only_status`. Any future status examples must be explicitly non-canonical unless they are approved in a dedicated `Estado` population issue.

## 8. Relationship expansion handling

`ResolverOutput` should represent relationship expansion through references to selected `Relación` contracts.

Required handling:

- `selected_relations` / `selected_relacion_refs` returns relationship contract references only.
- `Relación` owns compatibility, permission, requirement, dependency, sequencing, and restriction.
- Relationship endpoints, `tipo_relacion`, `cardinalidad`, `requerido`, and `orden` remain in relationship contract payloads.
- `ResolverOutput` should not copy full relationship bodies unless a later issue explicitly allows it.
- `ResolverOutput` should not flatten `Actor`, `Rol`, `Workflow`, and `WorkflowStep` behavior into one large object.
- `ResolverOutput` should not copy workflow-specific order into `WorkflowStep` fields.
- `ResolverOutput` should not copy actor permissions, role rules, evidence requirements, or artifact expectations into unrelated selected entity references.

This keeps relationship expansion reference-based and preserves the approved normalized model.

## 9. Evidence reference handling

Evidence handling stays reference-based.

`ResolverInput` may carry:

- `available_evidence_refs`
- `available_source_refs`
- issue references
- PR references
- resource references
- PM scope references

`ResolverOutput` may carry:

- `selected_evidencia_refs`
- `selected_fuente_refs`
- `required_evidence_refs`
- `missing_evidence_refs`
- evidence-related `selected_relations`

Rules:

- GitHub remains live evidence.
- Static Resolver shape must not copy issue bodies, PR bodies, comments, reviews, commit metadata, validation output, or branch state.
- Static Resolver shape must not create live evidence collection behavior.
- `Evidencia` references can point to future evidence contracts or live evidence references, depending on later approved contract work.
- `Fuente` references identify authority sources; they do not replace `Evidencia`.
- Missing evidence is represented by reference shape, not by invented evidence content.

## 10. Boundary and failure shape

Boundary and failure fields should make unresolved context visible without executing behavior.

Recommended `ResolverOutput` boundary group:

| Candidate field | Purpose | Boundary |
| --- | --- | --- |
| `boundary_note_refs` | References to boundary notes or relevant rules. | References only; no write authorization behavior. |
| `boundary_notes` | Short structural notes when a reference is not available. | Notes must stay placeholder-safe and non-operational. |
| `failure_kind_token` | Structural token for failure category. | Non-canonical until future `Estado`, `Límite`, or `Regla` contracts decide exact meanings. |
| `blocking_ref` | Reference to the blocking contract, evidence, or resource when known. | Reference only; no copied body or runtime trace. |
| `missing_evidence_refs` | References required but not available. | Does not collect evidence. |
| `violated_limite_refs` | References to selected limits relevant to a failure. | Does not evaluate limits. |
| `violated_regla_refs` | References to selected rules relevant to a failure. | Does not evaluate rules. |
| `unresolved_relation_refs` | References to relationships that could not be satisfied. | Does not expand or populate relationships. |
| `fallback_estado_ref` | Future fallback `Estado` reference. | Reference only; no hardcoded fallback behavior. |
| `next_step_recommendation` | Data shape for a proposed next step. | Recommendation only; no automation or routing execution. |

The failure shape should support unresolved inputs such as missing issue references, missing evidence references, incompatible actor/role references, unavailable template references, or boundary conflicts. It must not implement how those failures are detected.

## 11. Placeholder-safe examples policy

Examples are allowed only inside documentation.

Examples must be:

- placeholder-safe
- explicitly non-canonical
- visibly artificial
- not copied as real future contract content
- not populated operational data
- limited to explaining `ResolverInput`, `ResolverOutput`, selected references, evidence references, boundary shape, and status/reference handling

Examples must not define real Project OS v2 actors, roles, workflows, WorkflowSteps, actions, resources, scopes, sources, evidence, states, limits, rules, variables, templates, artifacts, relationships, contracts, Resolver behavior, operational decisions, live GitHub evidence, target-project artifacts, or populated contract data.

If an example needs a token, use visibly artificial placeholders such as `placeholder_input_ref`, `placeholder_actor_ref`, `placeholder_relation_ref`, or `example_only_status`. These tokens are not reserved IDs and must not be copied as future contract content.

## 12. Markdown scaffolding lifecycle

Markdown design documents are temporary scaffolding for contract design.

Current role:

- Markdown explains the ResolverInput and ResolverOutput shape for human review.
- Markdown records why Resolver output should remain reference-based.
- Markdown preserves the no-population and no-behavior boundaries before JSON contracts exist.

Later role, after equivalent JSON contracts exist and are reviewed:

- `contracts/**` becomes the canonical stable structure for entity and relationship contracts.
- AI should read the future `Resolver` and selected contracts/relationships, not Markdown docs, as the operational source.
- Markdown remains human reference and historical design context.
- Markdown must not become a parallel contract system.
- Markdown must not duplicate live operational evidence or contract data.

This issue does not create archive behavior, migration behavior, loaders, or archival rules.

## 13. No-population rule

The no-population rule is mandatory.

This document does not populate real values for:

- `Resolver`
- `Actor`
- `Rol`
- `Workflow`
- `WorkflowStep`
- `Acción`
- `Recurso`
- `Scope`
- `Fuente`
- `Evidencia`
- `Estado`
- `Límite`
- `Regla`
- `Variable`
- `Plantilla`
- `Artefacto`
- `Relación`
- `Contrato`

No real selected values are created for `ResolverInput` or `ResolverOutput`. No actual selected actors, roles, workflows, WorkflowSteps, actions, resources, scopes, sources, evidence, states, limits, rules, variables, templates, artifacts, relationships, or contracts are populated by this document.

## 14. Explicit non-implementation boundaries

This issue explicitly does not create or implement:

- JSON contract files
- populated contract data
- JSON schemas
- validators
- validator implementation
- schema implementation
- runtime behavior
- parser behavior
- automation
- API
- panel
- runners
- context packs
- context-pack output or context-pack loading
- target-project artifacts
- database/read-model direction
- projection architecture
- write authorization behavior
- Resolver behavior
- manifest shape
- index shape
- selector shape
- contract loader behavior
- actual skeleton files
- workflow composition
- relationship population

This document also does not define runtime routing, parser rules, selector execution, contract loading order, evidence collection, response rendering, PR creation behavior, validation behavior, or write permissions.

## 15. Readiness for manifest/index/selector shape issue

This document is intended to let a future manifest/index/selector shape issue proceed without re-deciding:

- what `ResolverInput` carries for request identity
- how current actor surface is represented as classification context
- how target actor is optional and limited to routing/delegating context
- how requested role remains a hint rather than permission
- how requested intent, repository/project references, issue references, PR references, resource references, requested output shape, available evidence references, PM-provided scope, and language/variable hints are grouped
- what `ResolverOutput` returns as selected-context references
- why `status_token` and `estado_ref` coexist
- why selected relationships are returned as `selected_relations` / `selected_relacion_refs`
- how required and missing evidence references are represented
- how boundary and failure shape remains reference-based
- why examples must be placeholder-safe and non-canonical
- why no runtime behavior or Resolver behavior is introduced here

A future manifest/index/selector issue should still define manifest shape, index shape, selector shape, and any contract inventory references as data shape only. It must not use this document to introduce contract loader behavior, runtime behavior, parser behavior, automation, validators, API, panel, database/read-model direction, write authorization behavior, workflow composition, or relationship population.

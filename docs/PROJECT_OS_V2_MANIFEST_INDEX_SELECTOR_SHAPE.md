# Project OS v2 Manifest, Index, Selector, and Loading Metadata Shape

## 1. Objective

Define the structure-only shape for later, explicitly scoped Project OS v2 manifest, index, selector, and loading metadata support bundles.

This document defines static data shapes that can later help `Resolver` discover and select candidate contracts without loading the entire system. R0.01 updates it as docs-only rebaseline work. It does not create JSON contract files, populated contract data, JSON schemas, validators, runtime behavior, parser behavior, automation, API, panel, runners, context packs, target-project artifacts, database/read-model direction, generated indexes, selector runtime, contract loader behavior, write authorization behavior, or Resolver behavior.

## 2. Scope

This issue is documentation-only and structure-only.

It defines future static shapes for:

1. manifest shape
2. index shape
3. selector shape
4. loading metadata shape
5. relationship to `ResolverInput` and `ResolverOutput`
6. contract discovery without full-system loading
7. selector dimensions
8. selector output references
9. no-runtime, no-loader, and no-parser rule
10. readiness for the first JSON skeleton issue

The shapes in this document are field-group decisions only. They are not contract instances, JSON schemas, generated indexes, loader instructions, parser rules, or executable selection behavior.

## R0.01 Roadmap Rebaseline Boundary

The active fixed roadmap source is GitHub issue #92. Issue #47 is historical/provenance, issue #91 is completed roadmap rebaseline evidence, and issue #90 is open/paused tooling-readiness evidence. This document must not imply that #47 remains the active roadmap.

Stage-scoped permissions apply:

- Planning issues do not create contracts.
- Docs issues may modify only approved docs.
- Contract population issues may create or update contracts only when explicitly scoped.
- Schema issues may create schemas only after schema strategy approval.
- Validator issues may create validators only after schema implementation.
- Loader, Resolver, runtime, panel, and write authorization remain blocked until their explicit roadmap IDs or later PM-approved roadmap amendments.

Under #92, schemas and validators happen after normalization and before Project OS inventory, mapping, and migration. Migrated baseline contracts are reviewed with schemas and validators before loader or Resolver work. Read-only loader work is R10, read-only Resolver work is R11, Base v0.1 dogfood-ready certification is R12, and dogfood begins only after certification. Panel planning/implementation is outside the fixed backlog.

Policy, manifest, index, and selector are non-entity static support bundles. They are not members of the 18 base entity families. They support Resolver discovery/reference behavior but do not implement runtime behavior, generated indexes, selector runtime, contract loader behavior, Resolver behavior, or write authorization.

## 3. Relationship to foundation / structure / envelope / skeleton / resolver shape docs

This document depends on and preserves:

- `docs/PROJECT_OS_V2_FOUNDATION_DESIGN.md`
- `docs/PROJECT_OS_V2_CONTRACT_STRUCTURE.md`
- `docs/PROJECT_OS_V2_CONTRACT_ENVELOPE.md`
- `docs/PROJECT_OS_V2_CONTRACT_SKELETON_PATTERNS.md`
- `docs/PROJECT_OS_V2_RESOLVER_CONTRACT_SHAPE.md`
- `fuentes/Modelo-de-entidades-base.txt`
- `fuentes/Modelo-base-con-definiciones-y-atributos-normalizados.txt`
- `fuentes/Relaciones-principales-y-cardinalidad.txt`

Foundation decisions preserved here:

- `Resolver` is the future single AI read entrypoint.
- AI should not read all Project OS contracts to answer a request.
- `Relación` owns compatibility, permission, requirement, dependency, sequencing, and restriction.
- `WorkflowStep` remains a reusable process block.
- `Workflow` composes `WorkflowStep` through `Relación`.
- GitHub remains live evidence for issues, PRs, commits, comments, reviews, tags, and validation outputs.
- Durable JSON must not store mutable GitHub truth.
- Markdown remains human design/reference until equivalent reviewed contracts exist.

Structure decisions preserved here:

- Future contract root remains `contracts/`.
- Future file shape remains `contracts/<entity_family>/<contract_id>.json`.
- Future manifest and index names are reserved conceptually as `contracts/manifest.json` and `contracts/index.json`.
- This document does not create `contracts/manifest.json`, `contracts/index.json`, or the `contracts/` directory.
- Future relationship contracts remain under `contracts/relacion/`.

Envelope and skeleton decisions preserved here:

- Later explicitly scoped contracts use the common envelope boundary for metadata and `payload`.
- Envelope metadata and payload data must not duplicate each other.
- Future skeleton values must be placeholder-safe.
- Examples must be non-canonical and documentation-only.
- The `version` object decision and `descripcion` ownership rule remain unchanged.

Resolver shape decisions preserved here:

- `ResolverInput` provides request classification data before selected contracts are known.
- `ResolverOutput` returns selected-context references only.
- `ResolverOutput` carries both `status_token` and `estado_ref`, with `estado_ref` becoming the future canonical `Estado` reference when approved `Estado` contracts exist.
- Selected `Relación` references remain reference-based and are not embedded as full relationship bodies.
- `ResolverOutput` materializes effective inherited context in deterministic order: Actor hard limits, Actor output boundaries, Role lens constraints, Workflow requirements, WorkflowStep requirements, action/resource/scope requirements, evidence/source requirements, template/artifact output shape, and state/failure rules.
- No lower layer may weaken an Actor hard limit.

## 4. Manifest shape

The future manifest is a contract inventory shape. It lists which contract references exist and where their contract files can be found without requiring the future Resolver to load every contract body.

The manifest shape should answer:

- Which manifest inventory is being read?
- Which contract root does it describe?
- Which entity families are represented?
- Which contract references are available?
- Which relationship contract references are available?
- Which source references explain the manifest's existence?
- What is the safe empty state when no contracts are listed yet?

Recommended manifest field groups:

| Field group | Candidate fields | Purpose | Boundary |
| --- | --- | --- | --- |
| manifest identity | `manifest_id`, `manifest_ref`, `manifest_name` | Identify the inventory shape by reference. | Does not create a real manifest contract or populated inventory. |
| manifest version | `manifest_version`, `version_ref` | Identify the manifest shape/version. | Version metadata is not runtime release state. |
| contract root reference | `contract_root_ref`, `contract_root_path` | Point to the future `contracts/` root. | Reference only; this document does not create the directory. |
| contract families represented | `entity_family_refs`, `represented_families` | List the entity-family tokens covered by the manifest. | Family presence does not imply populated contracts exist. |
| contract references | `contract_refs`, `entity_contract_refs` | List future entity contract IDs and file references. | References only; no contract bodies are copied. |
| relationship contract references | `relationship_contract_refs`, `relacion_contract_refs` | List future `Relación` contract IDs and file references. | References only; no relationship bodies are embedded. |
| optional manifest source references | `source_refs`, `manifest_source_refs` | Point to approved design docs, issues, PRs, or comments that explain the manifest. | References only; no issue body, PR body, comment, review, commit metadata, validation output, or branch state is copied. |
| placeholder-safe empty state | `contract_refs: []`, `relationship_contract_refs: []`, `represented_families: []` | Make an intentionally empty inventory visible and safe. | Empty arrays mean intentionally empty, not hidden population. |
| live evidence boundary | `evidence_ref_categories`, `live_evidence_ref_policy` | Allow references to categories of live evidence when later approved. | No live GitHub state is copied into the manifest. |

The manifest must not become a source of entity attributes, relationship semantics, workflow composition, status decisions, or evidence bodies. It is an inventory of selected references and paths only.

This issue does not create `contracts/manifest.json` and does not create actual manifest data.

## 5. Index shape

The future index shape is discoverability metadata only. It helps a future Resolver find candidate contracts by reference after the manifest is known, without loading every contract body.

The index shape should answer:

- Which index metadata is being read?
- Which entity families can be searched by reference?
- Which relationship types can be searched by reference?
- Which contract IDs, file paths, version references, and status references may identify candidates?
- Which optional tags or dimensions may help narrow candidate references without becoming canonical truth?

Recommended index field groups:

| Field group | Candidate fields | Purpose | Boundary |
| --- | --- | --- | --- |
| index identity | `index_id`, `index_ref`, `index_version` | Identify the discoverability metadata. | Does not create `contracts/index.json` or generated index files. |
| indexed entity families | `indexed_entity_family_refs`, `indexed_entity_families` | Declare which entity-family tokens are represented. | Family presence does not populate entity data. |
| indexed relationship types | `indexed_relationship_type_refs`, `indexed_relacion_types` | Declare relationship type references available for lookup. | Relationship type metadata does not own relationship semantics. |
| contract IDs | `contract_ids`, `contract_refs` | Point to candidate contract IDs. | IDs are references only; no contract bodies are copied. |
| file paths | `file_refs`, `contract_file_refs` | Point to future `contracts/<entity_family>/<contract_id>.json` paths. | Paths are references only; files are not created by this issue. |
| status references | `status_refs`, `estado_refs`, `contract_status_refs` | Help narrow candidate contracts by status/reference when later approved. | Status handling remains aligned with `ResolverOutput`; no status behavior is implemented. |
| version references | `version_refs`, `major_version_refs` | Help distinguish contract versions. | Version references are metadata only, not release behavior. |
| placeholder-safe tags or dimensions | `tag_refs`, `dimension_refs`, `selector_dimension_refs` | Optional non-canonical hints for discovery. | Tags or dimensions must not become a second source of truth. |
| copied body boundary | `body_inclusion_policy` | Make explicit that bodies are excluded. | No copied contract bodies, relationship payloads, evidence bodies, or Markdown content. |

The index must not replace the contract files. It must not copy entity attributes, relationship endpoints, relationship cardinality, required flags, order, rule behavior, limit severity, evidence verification data, template content, or workflow composition.

This issue does not create `contracts/index.json`, generated indexes, database/read-model direction, selector runtime, contract loader behavior, or any index generation behavior.

## 6. Selector shape

The future selector shape is static data used to choose candidate contract references. It is not runtime behavior, a selector algorithm, a scoring model, a parser, a loader, or a second source of truth.

Selectors should map request classification dimensions from `ResolverInput` to candidate contract and relationship references from the manifest/index shapes. A selector may describe which dimensions are relevant for a future selection, but it must not execute that selection.

Recommended selector field groups:

| Field group | Candidate fields | Purpose | Boundary |
| --- | --- | --- | --- |
| selector identity | `selector_id`, `selector_ref`, `selector_version` | Identify the selector shape by reference. | Does not create selector runtime or Resolver behavior. |
| input dimension references | `input_dimension_refs`, `required_dimension_refs`, `optional_dimension_refs` | Name the dimensions a future Resolver may compare with `ResolverInput`. | Dimension references do not parse user input. |
| candidate contract references | `candidate_contract_refs`, `selected_contract_ref_candidates` | Point to possible contract references. | Candidate references are not selected contract bodies. |
| candidate relationship references | `candidate_relacion_refs`, `selected_relationship_ref_candidates` | Point to possible `Relación` references. | Candidate relationship references do not embed relationship payloads. |
| output reference groups | `output_contract_ref_groups`, `resolver_output_ref_groups` | Describe which reference groups may flow into `ResolverOutput`. | Does not populate `ResolverOutput`. |
| evidence reference expectations | `required_evidence_ref_categories`, `missing_evidence_ref_categories` | Name evidence categories or refs that may be relevant. | Does not collect live evidence. |
| boundary hints | `boundary_hint_refs`, `failure_hint_refs` | Reference structural boundary/failure hints. | Hints do not authorize writes, execute workflows, or determine final state. |
| non-canonical dimension tags | `dimension_tags`, `selector_tags` | Optional placeholder-safe grouping hints. | Tags are non-canonical and cannot override contracts or relationships. |

Selector shape rules:

- Selectors must point to contract and relationship references only.
- Selectors must not duplicate entity attributes.
- Selectors must not duplicate relationship semantics.
- Selectors must not copy `Actor`, `Rol`, `Workflow`, `WorkflowStep`, `Acción`, `Recurso`, `Scope`, `Fuente`, `Evidencia`, `Estado`, `Límite`, `Regla`, `Variable`, `Plantilla`, `Artefacto`, `Relación`, or `Contrato` payload data.
- Selectors must not decide permissions, compatibility, requirements, dependencies, sequencing, restrictions, workflow composition, evidence sufficiency, or write authorization.
- Selectors must not become a second source of truth.

## 7. Loading metadata shape

The future loading metadata shape is static guidance describing which contract references may be needed after manifest/index/selector matching. It is not loader runtime, parser behavior, execution behavior, or a required loading order implementation.

The shape may describe the reference flow:

1. load manifest reference
2. inspect index reference groups
3. apply selector dimensions as data
4. collect candidate contract references
5. expand selected `Relación` references by reference
6. load related entity references only when selected by reference
7. return `ResolverOutput` references

Recommended loading metadata field groups:

| Field group | Candidate fields | Purpose | Boundary |
| --- | --- | --- | --- |
| loading metadata identity | `loading_metadata_id`, `loading_metadata_ref` | Identify the metadata shape. | Does not create loader behavior. |
| manifest reference | `manifest_ref` | Point to the manifest inventory shape. | Reference only; no manifest body embedded. |
| index references | `index_refs` | Point to one or more index metadata references. | Reference only; no generated indexes are created. |
| selector references | `selector_refs` | Point to selector data shapes. | Reference only; no selector runtime is created. |
| candidate collection references | `candidate_contract_refs`, `candidate_relacion_refs` | Carry references gathered from static shapes. | Does not load or validate the bodies. |
| selected contract references | `selected_contract_refs` | Carry contract references that may flow to `ResolverOutput`. | Does not embed selected contract bodies. |
| selected relationship references | `selected_relationship_refs`, `selected_relacion_refs` | Carry `Relación` references that may flow to `ResolverOutput`. | Does not embed full relationship bodies. |
| related entity references | `related_entity_refs` | Point to related entity contracts selected through relationships. | Does not flatten related contracts into one large object. |
| return reference groups | `resolver_output_ref_groups` | Name the reference groups returned by `ResolverOutput`. | Does not render responses or execute a next step. |

Loading metadata must keep the model layered and reference-based. It may describe that selected relationships can lead to related entity references, but it must not define how a loader reads files, parses JSON, resolves conflicts, orders execution, flattens graphs, caches results, or handles writes.

## 8. Selector dimensions

Selector dimensions are candidate classification dimensions that may be compared with `ResolverInput` in a future issue. They are data shape only.

Allowed selector dimensions include:

| Dimension | Candidate field names | Purpose | Boundary |
| --- | --- | --- | --- |
| requested intent | `requested_intent_ref`, `requested_action_hint` | Narrow candidates by the request's stated intent. | Does not execute the action. |
| current actor surface | `current_actor_ref`, `current_actor_surface_token` | Narrow candidates by the surface carrying the request. | Does not grant permission. |
| optional target actor | `target_actor_ref` | Support routing/delegation references when explicitly provided. | Optional; not a permission grant. |
| optional requested role hint | `requested_role_ref`, `requested_role_hint` | Support professional-lens selection as a hint. | Does not prove role compatibility. |
| repository/project reference | `repository_ref`, `target_project_ref` | Scope candidates to a project/repository reference. | Does not copy repository state. |
| resource type | `resource_type_ref`, `resource_refs` | Narrow candidates by resource category. | Does not copy file contents or live resource state. |
| issue / PR / resource references | `issue_refs`, `pr_refs`, `resource_refs` | Point to live or static resources mentioned by the request. | References only; no body text is copied. |
| output shape | `requested_output_contract_ref`, `response_shape_ref`, `output_template_hint` | Narrow candidates by requested output/report/body shape. | Does not select or expand a template by behavior; Plantilla owns shape/format/body conventions, not permission or rendering. |
| evidence availability | `available_evidence_refs`, `available_source_refs` | Represent already-known evidence references. | Does not collect or verify evidence. |
| missing evidence | `missing_evidence_refs`, `required_evidence_refs` | Represent references required but unavailable. | Does not invent evidence. |
| workflow lifecycle stage | `lifecycle_hint`, `workflow_stage_ref` | Narrow candidates by lifecycle stage references. | Does not compose workflows. |
| boundary/failure state hints | `boundary_hint_refs`, `failure_kind_token`, `blocking_ref` | Surface structural boundary or failure categories. | Does not determine final `Estado` behavior. |

Selector dimensions are not entity attributes. They are classification references and hints for candidate discovery. Any dimension that begins to express compatibility, permission, requirement, dependency, sequencing, restriction, workflow-specific order, required flags, or artifact expectations belongs in `Relación`, not in selector data.

## 9. ResolverInput / ResolverOutput integration

`ResolverInput` provides request classification data. Manifest, index, selector, and loading metadata shapes provide reference-oriented data that can help a future Resolver narrow candidate contracts without loading the whole system.

Reference flow:

1. `ResolverInput` carries request identity, current actor surface, requested intent, repository/project references, issue/PR/resource references, requested output shape, available evidence references, PM scope references, optional target actor, optional requested role, and language/variable hints.
2. Manifest shape lists available contract and relationship references by inventory.
3. Index shape exposes discoverability metadata for entity families, relationship types, contract IDs, file paths, status references, version references, and non-canonical dimension hints.
4. Selector shape maps `ResolverInput` dimensions to candidate contract and relationship references as data.
5. Loading metadata shape describes reference groups that may be needed to connect selected contracts and selected relationship references.
6. Selected contract references and selected relationship references flow into `ResolverOutput`.
7. `ResolverOutput` remains reference-based and compact.

`ResolverOutput` should continue to use the selected reference groups defined in `docs/PROJECT_OS_V2_RESOLVER_CONTRACT_SHAPE.md`, including selected `Actor`, `Rol`, `Workflow`, `WorkflowStep`, `Acción`, `Recurso`, `Scope`, `Fuente`, `Evidencia`, `Estado`, `Límite`, `Regla`, `Variable`, `Plantilla`, `Artefacto`, `Relación`, and `Contrato` references when those references are needed.

`Estado` and status handling remains as defined in `docs/PROJECT_OS_V2_RESOLVER_CONTRACT_SHAPE.md`: `ResolverOutput` may carry both a `status_token` and an `estado_ref`, with `estado_ref` treated as the future canonical `Estado` reference once reviewed `Estado` contracts exist.

## 10. Relationship expansion handling

Relationship expansion must remain reference-based.

Required handling:

- `Relación` owns compatibility, permission, requirement, dependency, sequencing, and restriction.
- `Relación` owns relationship endpoints, `tipo_relacion`, `cardinalidad`, `requerido`, and `orden`.
- Selected `Relación` references should be expanded by reference only.
- Full relationship bodies are not embedded unless a later issue explicitly allows it.
- Manifest and index shapes may list relationship contract references, but they must not copy relationship payloads.
- Selector shape may point to candidate relationship references, but it must not duplicate relationship semantics.
- Loading metadata may describe selected relationship references and related entity references, but it must not flatten the relationship graph.
- `Actor`, `Rol`, `Workflow`, and `WorkflowStep` behavior must not be flattened into one large object.
- Workflow-specific order must remain in `Relación.orden`, not in `WorkflowStep`.
- Workflow-specific required or optional state must remain in `Relación.requerido`, not in `Workflow` or `WorkflowStep` payloads.

This preserves the approved normalized model and prevents manifest/index/selector data from becoming a hidden workflow composition layer.

## 11. Evidence handling

Evidence handling stays live and reference-based.

Rules:

- GitHub remains live evidence.
- Manifest, index, selector, and loading metadata shapes may reference evidence categories or evidence refs.
- Static shapes must not copy issue bodies, PR bodies, comments, reviews, commit metadata, validation output, or branch state.
- Static shapes must not copy live GitHub issue state, PR state, review state, tag state, branch state, or validation state.
- Static shapes must not copy live roadmap state or durable GitHub truth into JSON.
- `Evidencia` references can point to future evidence contracts or live evidence references, depending on later approved contract work.
- `Fuente` references identify authority sources; they do not replace `Evidencia`.
- Missing evidence may be represented as missing evidence references or categories, not invented evidence content.
- No live evidence collection behavior is created by this document.

The manifest can list references to evidence categories only when needed for inventory provenance. The index can expose evidence-related dimensions only as non-canonical discovery hints. The selector can include evidence availability and missing evidence dimensions only as reference hints. Loading metadata can carry required or missing evidence reference groups only as static guidance.

Issue, PR, branch, commit, review, validation, and roadmap state must be checked live when needed. `Fuente` and `Evidencia` contracts are stable references/categories, not live snapshots.

## 12. Placeholder-safe examples policy

Examples are allowed only inside documentation.

Examples must be:

- placeholder-safe
- explicitly non-canonical
- visibly artificial
- not copied as real future contract content
- not populated operational data
- limited to explaining manifest shape, index shape, selector shape, loading metadata shape, selector dimensions, selected contract references, selected relationship references, and `ResolverInput` / `ResolverOutput` integration

Examples must not define real Project OS v2 actors, roles, workflows, WorkflowSteps, actions, resources, scopes, sources, evidence, states, limits, rules, variables, templates, artifacts, relationships, contracts, Resolver behavior, operational decisions, live GitHub evidence, target-project artifacts, or populated contract data.

If an example needs a token, it must use visibly artificial values such as `placeholder_manifest_ref`, `placeholder_index_ref`, `placeholder_selector_ref`, `placeholder_contract_ref`, `placeholder_relacion_ref`, or `example_only_dimension`. These tokens are not reserved IDs and must not be copied as future contract content.

## 13. Markdown scaffolding lifecycle

Markdown design documents are temporary scaffolding for contract design.

Current role:

- Markdown explains manifest, index, selector, and loading metadata shape decisions for human review.
- Markdown records why contract discovery should be reference-based.
- Markdown preserves the no-population and no-behavior boundaries before JSON contracts exist.

Later role, after equivalent JSON contracts exist and are reviewed:

- `contracts/**` becomes the canonical stable structure for entity and relationship contracts.
- AI should read the future `Resolver`, manifest/index/selector contract references, and selected contracts/relationships, not Markdown docs, as the operational source.
- Markdown remains human reference and historical design context.
- Markdown must not become a parallel contract system.
- Markdown must not duplicate live operational evidence or contract data.

This issue does not create archive behavior, migration behavior, loaders, archival rules, or behavior for replacing Markdown with contracts.

## 14. No-population rule

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

No real manifest inventory, index metadata, selector data, loading metadata, selected contracts, selected relationships, relationship expansion, workflow composition, evidence references, status references, source references, or contract data are populated by this document.

This document does not create `contracts/manifest.json`, `contracts/index.json`, populated contract data, JSON skeleton files, JSON schema files, validators, generated indexes, or database/read-model direction.

## 15. Explicit non-implementation boundaries

This issue explicitly does not create or implement:

- JSON contract files
- `contracts/manifest.json`
- `contracts/index.json`
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
- generated indexes
- selector runtime
- contract loader behavior
- write authorization behavior
- Resolver behavior
- template rendering behavior
- variable interpolation behavior
- generated-output behavior
- body-file generation behavior
- command execution behavior
- actual skeleton files
- workflow composition
- relationship population
- relationship body embedding
- live evidence collection behavior
- response rendering behavior
- PR creation behavior
- validation behavior
- write permissions

This document also does not define a selector algorithm, scoring model, file loading order implementation, parser rule, JSON reader, cache, index generator, database projection, API endpoint, UI panel, runner, context-pack generator, target-project artifact writer, or authorization layer.

## 16. Roadmap Readiness

This document is intended to let later explicitly scoped manifest/index/selector, skeleton, schema, validator, loader, Resolver, and population work proceed without re-deciding:

- manifest shape as contract inventory
- index shape as discoverability metadata
- selector shape as candidate-reference selection data
- loading metadata shape as static reference guidance
- contract discovery without full-system loading
- selector dimensions
- selector output references
- `ResolverInput` / `ResolverOutput` reference-based integration
- selected contract reference flow
- selected relationship reference flow
- reference-based relationship expansion
- GitHub-live evidence handling
- placeholder-safe and non-canonical examples policy
- Markdown scaffolding lifecycle
- no-population rule
- no-runtime, no-loader, and no-parser boundaries

The next roadmap item after R0.01 is R0.02 roadmap hygiene. Contract creation, schema work, validator work, loader behavior, Resolver behavior, runtime behavior, panel work, and write authorization remain unavailable unless a later explicit roadmap ID or PM-approved amendment scopes them. Later skeleton or population work must still decide concrete file creation scope, exact placeholder IDs, exact family-by-family payload field lists, and whether source references are attached as references. It must not use this document to create populated contract data, generated indexes, selector runtime, contract loader behavior, database/read-model direction, schemas, validators, API, panel, context packs, target-project artifacts, write authorization behavior, Resolver behavior, workflow composition, or relationship population.

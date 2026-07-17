# Skill: mobile development

A quality lens for mobile work inside an already resolved Project OS task. It
does not prescribe a framework or explain how to operate Project OS: it adds the
judgment needed for an app to remain correct as lifecycle state changes, the
network disappears, device capabilities are used, or platform constraints apply.

## Responsibility

Apply engineering judgment to lifecycle, navigation and state, offline
operation, permissions, accessibility, device resources, native APIs, local
persistence, and cross-platform delivery, sized to the product and hardware
that are actually supported.

## When to use it

- The scope touches a mobile application, a native view, or an integration with
  hardware or operating-system APIs.
- Navigation, persistent state, synchronization, intermittent connectivity, or
  background work is involved.
- Permissions, notifications, deep links, local storage, or private device data
  appear in the change.
- The work reviews performance, memory/battery use, startup, accessibility, or
  behavioral differences between iOS and Android.
- Validation needs emulators and physical hardware, not only isolated tests.

## Quality criteria

- **Explicit lifecycle.** Foreground, background, suspension, resumption,
  system termination, and UI recreation preserve invariants. Code does not
  assume that a process or view survives after losing focus.
- **Navigation and state ownership.** Restorable routes, ephemeral screen state,
  session state, and persisted data have distinct owners. Back navigation, deep
  links, and restoration cannot create impossible screens or duplicate work.
- **Offline and intermittent connectivity.** Define what can be read or edited
  without a network, how pending/synchronized/conflicted states appear, and how
  retries reconcile. Connectivity does not imply that a service is reachable.
- **Proportionate permissions.** Request each permission in context when the
  feature needs it, with a fallback for denial or restriction. Technical access
  to a sensor or file never implies product authorization to use its data.
- **Mobile accessibility.** Validate screen readers, focus order, text scaling,
  contrast, reduced motion, orientation, and touch targets through tools and
  real use, not appearance alone.
- **Performance and resources.** Cold/warm startup, main-thread work, memory,
  battery, network, and storage have measurable budgets. Lists, images, sensors,
  and periodic work release or limit resources with the lifecycle.
- **Hardware and native APIs.** Camera, location, biometrics, files, Bluetooth,
  and other device features are optional capabilities that may be absent, fail,
  or change during use. Callbacks honor cancellation and current state.
- **iOS/Android differences.** System navigation, permissions, background
  limits, formats, notifications, and API availability are verified per
  supported platform/version. A shared abstraction does not erase differences.
- **Local persistence and migrations.** Local schemas have versions and atomic
  or recoverable migrations compatible with existing data. Discardable cache is
  distinct from user data that must not be lost.
- **Notifications and background work.** Duplicate, late, or missing delivery is
  part of the contract. Tasks are idempotent, bounded, and compatible with
  system quotas; correctness never depends on continuous execution.
- **Device privacy.** Minimize data, retention, logs, and backups; avoid exposing
  sensitive content through notifications, screenshots, clipboard, or
  unsuitable storage. Telemetry names events without private values.
- **Stores and releases as separate gates.** Technical compatibility never
  implies authority to sign, publish, or distribute. Stores, signing, and
  releases require their own evidence, authority, and validation outside this
  skill.
- **Representative validation.** Unit tests cover logic; integration covers
  persistence and bridges; UI tests cover critical flows. Emulators broaden the
  matrix, while physical hardware validates sensors, memory, battery,
  notifications, accessibility, and thermal behavior.

## Risks to detect

- Lost or duplicated actions when suspending/resuming or recreating a screen.
- Navigation state that conflicts with session, persisted data, or deep links.
- Offline queues without idempotency, ordering, or a conflict policy.
- Permissions requested at startup without explanation or a denial path.
- Heavy main-thread work, blocked startup, memory leaks, or battery-draining
  wakeups.
- Native API usage without availability, cancellation, and platform/version
  handling.
- Destructive local migrations or caches treated as durable sources of truth.
- Notifications that leak data, process twice, or open invalid routes.
- Compatibility claims based only on a simulator or a powerful device.

## Decisions to favor

- Model lifecycle transitions and recoverable states before adding effects.
- Separate ephemeral, persisted, and synchronized state, with an explicit source
  of truth for each.
- Treat offline behavior as a product contract, not invisible retries.
- Request the minimum capability at the point of use and preserve a degraded path.
- Measure on the weakest supported devices before optimizing by intuition.
- Encapsulate native differences behind testable boundaries without claiming
  parity that the platforms do not provide.
- Keep migrations small and recoverable while preserving user data.
- Combine automation with physical-device and assistive-technology sessions for
  the highest-risk flows.

## Warning signs

- "The framework handles lifecycle/offline for us."
- "Once granted, a permission will always be available."
- "It works in the simulator" as sufficient compatibility evidence.
- Putting all navigation and data into one global store.
- Background work that must run every minute for the product to be correct.
- Deleting the local database after any migration error.
- Treating signing, publication, or store access as an automatic consequence of
  a successful build.

## Examples of judgment

Compact, portable contrasts. These are conceptual pseudocode, not production
code or Flutter, Kotlin, or Swift instructions.

### Resume without duplicate effects

Problematic — every foreground transition starts another write:

```text
onForeground:
  uploadDraft(currentDraft)
```

Better — persisted state identifies the operation and makes retries idempotent:

```text
onForeground:
  for operation in pendingOperations:
    syncOnce(operation.id, operation.version)
```

### Permission denial as a supported state

Problematic — asks for camera access at launch and blocks the app on denial:

```text
onLaunch -> requestCamera -> denied -> fatalScreen
```

Better — asks in context and preserves a proportionate alternative:

```text
onScanAction -> explainPurpose -> requestCamera
granted -> scan
denied  -> manualEntry + settingsHelp
```

### Offline with explicit conflict handling

Problematic — last-write-wins silently overwrites remote changes:

```text
reconnect -> upload(localDocument)
```

Better — synchronizes against a known version and applies or presents a defined
conflict policy:

```text
reconnect -> compare(local.baseVersion, remote.version)
same      -> upload(localChange, operationId)
different -> resolveConflict(localChange, remoteChange)
```

## Expected output

Return actionable judgment within scope: missing transitions and states,
platform or device risks and their consequences, the recommended decision and
rationale, relevant budgets, and a proportionate validation matrix that
distinguishes automation, emulators, and physical hardware. Do not produce
artifacts, workflows, or publication instructions.

## Limits / non-authorization

This skill is optional. It grants no permission and never replaces live scope,
PM approval, branch preflight, evidence, validation, traceability, or
review-before-close. It does not authorize signing, store access, releases,
distribution, or use of device data/hardware; Project OS and the target continue
to govern those gates.

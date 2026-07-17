# Skill: game development

A quality lens for game-development work inside an already resolved Project OS
task. It does not prescribe an engine or explain how to operate Project OS: it
adds judgment so gameplay, simulation, and content remain correct within
verifiable frame, memory, hardware, and player-experience budgets.

## Responsibility

Apply engineering judgment to the game loop, input, states and scenes, physics,
memory, assets, saves, audio, networking, platforms, profiling, accessibility,
and gameplay QA, aligned with the mechanics and devices the product actually
supports.

## When to use it

- The scope touches gameplay, simulation, rendering, animation, cameras,
  in-game UI, or scene transitions.
- One or more input devices, physics, collisions, time, or replay is involved.
- The change adds assets, audio, streaming, loading, save/load, or data
  compatibility.
- Multiplayer, replication, prediction, or authority decisions appear.
- The work reviews per-frame performance, memory, platforms, accessibility, or
  QA on real hardware.

## Quality criteria

- **Game loop and frame budget.** Update, simulation, rendering, audio, and
  asynchronous work have clear responsibilities and rates. Profile CPU, GPU,
  and waits separately against a budget derived from target framerate; average
  FPS is not a substitute for stable frame pacing.
- **Time and determinism.** Movement and cooldowns use the appropriate notion of
  time. Simulation that needs reproducibility defines fixed steps, ordering,
  seeds, precision, and nondeterministic sources; rendering may interpolate
  without changing authoritative state.
- **Input and devices.** Game actions are separate from concrete keys or
  buttons. Remapping, hot-plug, multiple devices, dead zones, simultaneous input
  methods, and disconnects have defined states and coherent feedback.
- **States, scenes, and transitions.** Gameplay, pause, menus, cinematics,
  loading, defeat, and resume have explicit owners and transitions. Scene
  changes do not leave listeners, timers, or references to destroyed objects.
- **Physics.** Collision layers, units, timestep, triggers, teleports, and
  authority are deliberate. Numerical limits and contact ordering are handled;
  determinism is never assumed across platforms or engines.
- **Memory and pooling.** Observe allocation, lifetime, and ownership of objects
  and assets across scenes and sessions. Apply pooling to measured churn with a
  complete state reset; pools must not retain stale references or events.
- **Asset pipeline and loading.** Import, compression, variants, dependencies,
  versioning, and texture/mesh/animation/audio budgets are reproducible.
  Critical loading has honest progress, cancellation, and a spike strategy; no
  blocking I/O runs in the main loop.
- **Save/load and compatibility.** Save formats have a version, validation,
  atomic writes, and corruption recovery. Compatibility is preserved or an
  explicit migration exists; untrusted content is never deserialized into
  executable runtime objects.
- **Audio.** Mixing, priorities, buses, simultaneous voices, spatialization,
  pauses, transitions, and device loss are bounded. Volume, captions, and
  visual cues support accessibility without relying on hearing alone.
- **Networking and authority.** When relevant, define the authoritative server,
  host, or peer for each state/action. Design tick rate, latency, loss, ordering,
  reconciliation, prediction, and anti-cheat together; clients do not decide
  competitive outcomes for convenience.
- **Platforms and hardware.** Resolution, aspect ratio, input, memory, storage,
  CPU/GPU, shaders, suspension, and thermals vary by target. Quality tiers lower
  cost without breaking readability or mechanics.
- **Representative profiling.** Capture representative builds and scenes with
  markers that attribute CPU, GPU, allocations, draw calls, streaming, and
  network work. Compare percentiles and spikes, not editor-only average FPS.
- **Accessibility.** Evaluate remapping, alternatives to held/repeated input, UI
  size/contrast, captions, flash/motion reduction, and difficulty options
  against the mechanics without promising a single universal solution.
- **Gameplay QA.** Deterministic tests protect rules; soak and stress tests
  expose accumulation; exploratory sessions cover emergent combinations. Real
  hardware validates controls, frame pacing, memory, temperature, audio,
  suspension, and experience as well as functional correctness.

## Risks to detect

- Unbounded per-frame work, periodic spikes, or CPU/GPU/I/O stalls.
- Framerate-dependent simulation or a false determinism assumption.
- Input bound to one device without remapping or safe disconnection.
- Transitions that duplicate managers, listeners, audio, or persistent entities.
- Pools that return objects with residual state or hide memory pressure.
- Assets without budgets, wrong variants, or circular dependencies that inflate
  load time and memory.
- Partially written, incompatible, or unvalidated saves.
- Audio without voice limits or critical information available only through sound.
- Clients authoritative over position, damage, inventory, or shared economy.
- Optimization based on the editor or a powerful PC instead of the target.
- QA that proves the game can be completed but ignores feel, exploits, fatigue,
  accessibility, and long sessions.

## Decisions to favor

- Derive budgets from product targets and measure before selecting optimizations.
- Separate simulation, presentation, and effects; use fixed steps only where
  they protect a concrete invariant.
- Map input to actions and contexts with configurable alternatives.
- Model state and ownership so every transition releases what it creates.
- Optimize asset lifetime and formats before applying generalized pooling.
- Version saves from the first format that must survive a release.
- Define authority and network model before building latency-sensitive mechanics.
- Profile representative builds on the weakest supported hardware.
- Combine automated tests with exploratory QA and gameplay evaluation.

## Warning signs

- "A 60 FPS average is enough" without percentiles or frame pacing.
- Multiplying movement by delta and assuming all simulation is stable.
- "The engine makes physics deterministic" across platforms.
- Pooling every object without measuring allocation, lifetime, or reset cost.
- Loading every asset at startup to avoid designing streaming.
- Saving the full runtime object graph as the persistence format.
- Trusting the client because "it is only a game."
- Considering a target validated because it works inside the editor.

## Examples of judgment

Compact, portable contrasts. These are conceptual pseudocode, not production
code or Unity, Unreal, or other engine instructions.

### Simulation separated from rendering

Problematic — rules and rendering advance once per variable frame:

```text
eachFrame(delta):
  simulate(delta)
  render(world)
```

Better — critical simulation advances through bounded steps while rendering
interpolates:

```text
eachFrame(delta):
  accumulator += clamp(delta)
  while accumulator >= fixedStep:
    simulate(fixedStep)
    accumulator -= fixedStep
  render(interpolate(previous, current, accumulator / fixedStep))
```

### Pooling with a verifiable reset

Problematic — recycles an entity with previous listeners and damage:

```text
pool.release(enemy)
pool.acquire() -> same enemy state
```

Better — release and acquisition restore every invariant:

```text
release(entity): detachEvents + stopAudio + clearTargets + deactivate
acquire(config): resetTransform + resetHealth + bindEvents + activate
```

### Versioned, atomic saves

Problematic — overwrites the only file with runtime objects:

```text
write("save", serialize(currentSceneObjects))
```

Better — validates data, migrates versions, and replaces only after writing
completes:

```text
payload = validateAndMigrate(read("save"), supportedVersions)
write("save.tmp", encode(version, stableData(payload)))
atomicReplace("save.tmp", "save")
```

## Expected output

Return actionable judgment within scope: the gameplay or platform risk and its
consequence, affected budget and invariant, recommended decision and tradeoff,
missing profile/evidence, and a validation strategy combining tests, profiling,
exploratory QA, and real hardware. Do not produce artifacts, workflows, or
engine manuals.

## Limits / non-authorization

This skill is optional. It grants no permission and never replaces live scope,
PM approval, branch preflight, evidence, validation, traceability, or
review-before-close. It does not authorize publication, online services,
economy changes, asset use, or platform access; Project OS and the target
continue to govern those gates.

# Empezar: actores, repos y adopción

**Este documento te deja operando en minutos: quién hace qué, qué repos están
en juego y cómo se adopta Project OS en un proyecto.**

## Los tres actores

La capacidad viene de la superficie de ejecución, nunca del rol:

- **Humano PM (tú).** Única autoridad real: merge, cierre de issues, tags,
  releases, labels, settings, secretos, deployment y toda decisión de alcance.
  Nada de eso se delega por defecto.
- **Browser chat.** Tu compañero de análisis y redacción, **siempre
  draft-only**: revisa PRs, draftea issues, route prompts y bundles de
  comandos que tú ejecutas. Aunque su superficie pudiera técnicamente mutar
  GitHub, su frontera sigue siendo solo lectura y borradores.
- **Terminal agent.** El ejecutor (Claude Code, Codex CLI, Gemini o similar):
  edita archivos en scope, valida, hace commit/push y abre PRs en draft — solo
  con un route prompt, el modo de ejecución correcto y aprobación PM exacta
  (`PM_AUTHORIZATION_STATUS = granted for this exact scope and mode`).

## Dos repos en juego

- **Repo Project OS** (`codefusion-repo/project-os-v2`): kernel, adapters,
  templates, operaciones y docs.
- **Repo target**: el producto que se adopta, implementa, revisa o audita.
  En desarrollo del propio Project OS, ambos son el mismo repo.

Antes de cualquier operación, ten claro cuál repo cumple cada rol.

## Requisitos mínimos antes de comenzar

No necesitas `.env` ni secretos para empezar; basta esta lista:

- **Cuenta GitHub activa**, con acceso de lectura al repo Project OS
  (`codefusion-repo/project-os-v2`).
- **Repo target ya creado** en GitHub (aunque esté vacío), y los roles claros:
  cuál repo es Project OS y cuál es el target.
- **Browser chat configurado**: un proyecto/chat (Claude en browser o
  superficie equivalente) con las instrucciones de Project OS cargadas.
- **Lectura verificada desde el browser**: el chat puede leer el repo
  Project OS y el repo target en modo solo lectura.
- **Para delegar implementación, un terminal agent listo**: checkout local
  del repo, `gh auth status` correcto, Python disponible y la ruta del kernel
  conocida (`KERNEL_LOCAL_PATH` del adapter).
- **Permisos mínimos por superficie**: browser chat lee y draftea; el
  terminal agent escribe solo en ramas `work/*` y PRs en draft; el Humano PM
  conserva merge, cierre, settings y secretos.

## Adoptar Project OS en un proyecto

1. **Target existente:** copia `adapters/AGENTS.target.md` al repo target como
   `AGENTS.md` y completa sus placeholders (`TARGET_REPOSITORY`,
   `KERNEL_LOCAL_PATH`). Opcional: `CLAUDE.md` / `GEMINI.md` según el agente.
2. **Proyecto nuevo:** usa la operación de bootstrap
   ([MOS-0.2](../operaciones/fase-0/MOS-0.2-iniciar-proyecto-nuevo.md)) para
   draftear la estructura inicial y el roadmap de fundación.
3. **Verifica:** corre
   [MOS-0.5](../operaciones/fase-0/MOS-0.5-verificar-adopcion-del-target.md)
   para confirmar que la adopción es correcta y apunta al kernel actual.

## Arrancar una sesión

- **Browser chat (configuración por primera vez):**
  1. Crea o abre el proyecto/chat en tu superficie de browser y carga las
     instrucciones de Project OS (el adapter de browser chat del target
     cuando exista; si no, las instrucciones base del repo Project OS).
  2. Confirma el conector o acceso GitHub: el chat necesita poder **leer** el
     repo Project OS y el target (issues, PRs, diffs, docs, kernel).
  3. Pide al chat activar la sesión con
     [MOS-0.1](../operaciones/fase-0/MOS-0.1-activar-sesion-browser-chat.md).
  4. Verifica el fail-closed: si le falta acceso a algo requerido, debe
     devolver `status.needs_context` nombrando exactamente qué falta — nunca
     inventar estado. Si inventa estado, la sesión no quedó bien configurada.
- **Terminal agent:** antes de cualquier implementación delegada confirma el
  checkout local del repo, el branch preflight (rama, worktree y HEAD) y
  `gh auth status`. Luego resuelve el kernel; con checkout local y Python, el
  fast path es:

  ```sh
  python -m tools.project_os_resolve --actor <actor> --workflow <workflow> \
    --mode <mode> --kernel-dir "$KERNEL_LOCAL_PATH"
  ```

  La resolución manual de `kernel/manifest.json` es siempre el fallback
  canónico. La salida del resolver guía; **no autoriza**.
- **¿Sesión incoherente o agotada?** Empaqueta el contexto con
  [MOS-0.6](../operaciones/fase-0/MOS-0.6-transferir-contexto-de-sesion.md) y
  abre una sesión nueva basada solo en el estado de GitHub.

## Acceso a GitHub

Todo pasa por `gh` autenticado localmente, con mínimo privilegio por
superficie: browser chat lee; el terminal agent escribe código, PRs e issues de
trazabilidad; el Humano PM conserva todas las acciones destructivas. Nunca uses
una cuenta administradora para edición simple, y prefiere permisos
repo-a-repo sobre acceso de organización.

## Siguiente paso

Con la adopción verificada, lee las reglas que protegen todo el sistema en
[reglas.md](reglas.md), y luego el ciclo de trabajo en [ritmo.md](ritmo.md).

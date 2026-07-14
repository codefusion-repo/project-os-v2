# Benchmark reproducible de contexto

**Cuánto contexto de instrucciones carga una sesión de agente al inicio,
medido sobre stacks convencionales reales y públicamente verificables y sobre
el stack de Project OS, para una misma tarea declarada.** Este benchmark solo
mide tamaños: no mide calidad, no demuestra ahorro frente a ningún stack, no
promete ahorros universales y no otorga permisos
(`boundary.output_not_permission`).

Versión inglesa: [context-benchmark.md](../../project-os-en/docs/context-benchmark.md).

## Tarea declarada y unidad de medida

- **Tarea declarada:** gobernar a un agente de codificación de terminal que
  implementa una unidad de trabajo acotada dentro de un repositorio.
- **Unidad de medida (equivalencia funcional):** los archivos de instrucciones
  repo-wide que cada herramienta carga por convención al inicio de cada sesión
  para esa tarea, antes de cualquier estado vivo. Queda fuera el contexto
  on-demand de cada stack (archivos `CLAUDE.md` de subdirectorios,
  instructions con `applyTo`, skills, operaciones MOS): se carga solo cuando
  se usa.
- **Stack de sesión de Project OS para esa tarea:** shim `CLAUDE.md` +
  bootloader `AGENTS.md` + stdout del resolver con
  `--hydration-level compact --compact` para la tupla `actor.terminal_agent` /
  `workflow.issue_implementation` / `mode.delegated_commit_pr`.

## Metodología declarada

- **Fecha de medición:** 2026-07-14.
- **Archivos locales:** commit `84a615d2b838` de `codefusion-repo/project-os-v2`;
  los insumos medidos (`CLAUDE.md`, `AGENTS.md` y ambos directorios de kernel)
  no cambian después de ese commit en la rama que corrige este documento.
- **Corpus público:** cada archivo se mide tal como existe en su repositorio
  de origen al commit pineado en la tabla de procedencia; no se copia a este
  repositorio y la reproducción lo descarga desde ese commit.
- **Métricas:** bytes UTF-8, caracteres y tokens.
- **Tokenizer declarado:** `tiktoken` 0.13.0 (Python 3.12.13), con dos
  encodings públicos para mostrar la variación entre tokenizers: `o200k_base`
  y `cl100k_base`. Los conteos de tokens dependen del tokenizer y del modelo:
  ningún número de estas tablas es un ahorro universal.
- **Separación de kernel y estado vivo:** el output del resolver contiene solo
  contrato de kernel ya resuelto. No incluye issues, PRs, ramas, diffs ni
  ningún estado vivo: eso se lee desde GitHub al momento de la tarea y queda
  fuera de esta medición por diseño.

## Benchmark principal — stacks convencionales públicos

### Criterios de selección, declarados antes de medir

1. **Mecanismos:** los archivos de instrucciones repo-wide con convención
   documentada por su vendor en los agentes de codificación de terminal
   first-party de Anthropic, OpenAI, Google y GitHub: Claude Code
   (`CLAUDE.md`), Codex CLI (`AGENTS.md`), Gemini CLI (`GEMINI.md`) y GitHub
   Copilot (`.github/copilot-instructions.md`).
2. **Archivo por mecanismo:** el del repositorio público de la propia
   herramienta cuando lo publica en su ubicación canónica; si no lo publica,
   el del repositorio público con más estrellas de la organización GitHub del
   vendor que sí lo publica. Selección al HEAD del default branch en la fecha
   de medición, pineada por commit.
3. **Resultados de aplicar la regla:** `openai/codex`,
   `google-gemini/gemini-cli` y `microsoft/vscode-copilot-chat` publican su
   propio archivo. `anthropics/claude-code` no publica `CLAUDE.md` raíz, así
   que el fallback seleccionó `anthropics/claude-cookbooks`, el repositorio
   con más estrellas de esa organización que sí lo publica en la fecha de
   medición. Cursor rules quedó excluido por la propia regla: su vendor no
   publica un repositorio con `.cursor/rules` verificable.

### Corpus: procedencia y licencias

| Stack | Archivo medido | Repositorio | Commit | Licencia |
| --- | --- | --- | --- | --- |
| Claude Code | `CLAUDE.md` | `anthropics/claude-cookbooks` | `67ce644d33e5` | MIT |
| Gemini CLI | `GEMINI.md` | `google-gemini/gemini-cli` | `fa975395bcc6` | Apache-2.0 |
| GitHub Copilot | `.github/copilot-instructions.md` | `microsoft/vscode-copilot-chat` | `5863f5a70889` | MIT |
| Codex CLI | `AGENTS.md` | `openai/codex` | `393f64565ab4` | Apache-2.0 |

### Resultados

| Stack de sesión | Bytes | Caracteres | Tokens `o200k_base` | Tokens `cl100k_base` |
| --- | ---: | ---: | ---: | ---: |
| Claude Code — `claude-cookbooks` | 3520 | 3520 | 914 | 914 |
| Gemini CLI — `gemini-cli` | 4610 | 4610 | 1140 | 1140 |
| GitHub Copilot — `vscode-copilot-chat` | 17401 | 17393 | 3970 | 3832 |
| Codex CLI — `codex` | 22519 | 22485 | 5182 | 5160 |
| Project OS — kernel español (default) | 17815 | 17789 | 4195 | 4563 |
| Project OS — kernel inglés (selección explícita) | 16981 | 16960 | 3831 | 3899 |

Desglose del stack de Project OS en bytes: `CLAUDE.md` 296 + `AGENTS.md` 2301
+ resolver `compact` 15218 (kernel español) o 14384 (kernel inglés).

### Lectura de los resultados

- El stack de sesión de Project OS cae **dentro del rango observado** en los
  stacks convencionales reales (3520–22519 bytes; 914–5182 tokens
  `o200k_base`): más grande que dos de los cuatro y más pequeño que los otros
  dos. Este benchmark **no demuestra ahorro** frente a stacks convencionales y
  no debe citarse como si lo hiciera.
- Lo que difiere es el tipo de contenido, no principalmente el tamaño: los
  archivos convencionales medidos llevan conocimiento de ingeniería del
  proyecto en prosa (build, tests, estilo, arquitectura); el stack de Project
  OS lleva un contrato ya resuelto por tupla (reglas, límites, evidencia
  requerida, outputs y estados, con no-autorización explícita). Cuál conviene
  depende del proyecto: este benchmark no lo decide y no afirma que Project OS
  reemplace a ninguna de estas herramientas.

## Perfil interno de hidratación

Esta sección es un **perfil interno**: mide el kernel de Project OS contra sí
mismo y no compara contra terceros. Sus porcentajes no son comparables con el
benchmark principal y no deben citarse como ahorro frente a stacks
convencionales.

Dos referencias internas, construidas desde el kernel real:

- **Baseline por tupla (el exigido por ADR 0004):** un documento estático que
  inline-a exactamente lo que esta tupla necesita. Coincide con el output
  `full/debug` serializado: un documento estático no puede seleccionar por
  actor/workflow/mode, así que debe llevar el contrato completo de la tupla.
- **Kernel completo (techo interno):** la concatenación byte a byte de los 11
  archivos JSON del kernel, `manifest.json` primero y el resto en orden de
  nombre: lo que costaría inline-ar el kernel entero para servir cualquier
  tupla sin selección.

### Kernel español (default)

| Alternativa | Bytes | Caracteres | Tokens `o200k_base` | Tokens `cl100k_base` |
| --- | ---: | ---: | ---: | ---: |
| Resolver `minimal` | 6696 | 6696 | 1646 | 1757 |
| Resolver `compact` | 15218 | 15213 | 3566 | 3885 |
| Baseline por tupla (= `full/debug`) | 16504 | 16499 | 3939 | 4259 |
| Kernel completo (11 archivos) | 47584 | 47579 | 11000 | 11576 |

Reducción frente al baseline por tupla: `minimal` −59,4 % bytes (−58,2 %
tokens `o200k_base`, −58,7 % `cl100k_base`); `compact` −7,8 % bytes (−9,5 %,
−8,8 %). Frente al kernel completo (solo perfil interno): `minimal` −85,9 %
bytes (−85,0 %, −84,8 %); `compact` −68,0 % (−67,6 %, −66,4 %); `full/debug`
−65,3 % (−64,2 %, −63,2 %).

### Kernel inglés (selección explícita)

Misma tupla, mismos comandos, con `--kernel-dir project-os-en/kernel`:

| Alternativa | Bytes | Caracteres | Tokens `o200k_base` | Tokens `cl100k_base` |
| --- | ---: | ---: | ---: | ---: |
| Resolver `minimal` | 6509 | 6509 | 1530 | 1539 |
| Resolver `compact` | 14384 | 14384 | 3202 | 3221 |
| Baseline por tupla (= `full/debug`) | 15670 | 15670 | 3575 | 3595 |
| Kernel completo (11 archivos) | 46000 | 46000 | 10183 | 10200 |

Reducción frente al baseline por tupla: `minimal` −58,5 % bytes; `compact`
−8,2 %. Frente al kernel completo (solo perfil interno): `minimal` −85,9 %
bytes; `compact` −68,7 %; `full/debug` −65,9 %.

### Qué información conserva cada alternativa

- **`minimal`** conserva la identidad de manifest/actor/mode/workflow, todos
  los límites aplicables, las acciones prohibidas, la evidencia requerida, los
  outputs permitidos y los estados: lo necesario para detener trabajo
  prohibido. No incluye la guía mandatoria completa.
- **`compact`** (default práctico) añade las reglas operativas mandatorias, el
  contexto operativo seleccionado y las referencias resolubles a
  artefactos/templates/skills: la vista con la que se ejecuta.
- **El baseline por tupla (`full/debug`)** añade los metadatos completos de la
  resolución seleccionada; como nivel de hidratación es para revisión y
  auditoría, no el modo normal.
- **El kernel completo** conserva el kernel entero para todas las tuplas a la
  vez, sin seleccionar nada: cada sesión paga el contrato entero aunque solo
  use una tupla.

La reducción no elimina límites, evidencia, outputs, estados, no-autorización
ni secret safety: eso lo guardan los tests
`tests/test_project_os_hydration_levels.py`
(`test_levels_have_deterministic_monotonic_contract_shapes_and_keep_safety` y
`test_requested_skills_and_existing_fail_closed_boundaries_survive_each_level`).

## Reproducción

Desde la raíz del repo, con Python 3.12+:

```sh
python -m venv .venv && . .venv/bin/activate
pip install tiktoken==0.13.0

mkdir -p /tmp/pos-bench/corpus /tmp/pos-bench/stacks
curl -fsSL -o /tmp/pos-bench/corpus/claude-code-claude-cookbooks.md \
  https://raw.githubusercontent.com/anthropics/claude-cookbooks/67ce644d33e5/CLAUDE.md
curl -fsSL -o /tmp/pos-bench/corpus/gemini-cli-gemini-cli.md \
  https://raw.githubusercontent.com/google-gemini/gemini-cli/fa975395bcc6/GEMINI.md
curl -fsSL -o /tmp/pos-bench/corpus/copilot-vscode-copilot-chat.md \
  https://raw.githubusercontent.com/microsoft/vscode-copilot-chat/5863f5a70889/.github/copilot-instructions.md
curl -fsSL -o /tmp/pos-bench/corpus/codex-cli-codex.md \
  https://raw.githubusercontent.com/openai/codex/393f64565ab4/AGENTS.md

for kernel in project-os-es project-os-en; do
  for level in minimal compact full/debug; do
    python tools/project_os_resolve.py --actor actor.terminal_agent \
      --workflow workflow.issue_implementation --mode mode.delegated_commit_pr \
      --kernel-dir "$kernel/kernel" --hydration-level "$level" --compact \
      > "/tmp/pos-bench/stacks/$kernel-${level//\//-}.json"
  done
  (cd "$kernel/kernel" && cat manifest.json $(ls *.json | grep -v '^manifest')) \
    > "/tmp/pos-bench/stacks/$kernel-full-kernel.txt"
  cat CLAUDE.md AGENTS.md "/tmp/pos-bench/stacks/$kernel-compact.json" \
    > "/tmp/pos-bench/stacks/$kernel-session-stack.txt"
done

python - <<'PY'
from pathlib import Path
import tiktoken
encodings = {n: tiktoken.get_encoding(n) for n in ("o200k_base", "cl100k_base")}
for path in sorted(Path("/tmp/pos-bench").rglob("*")):
    if path.is_dir():
        continue
    text = path.read_text(encoding="utf-8")
    tokens = {name: len(enc.encode(text)) for name, enc in encodings.items()}
    print(path.name, {"bytes": len(text.encode("utf-8")), "chars": len(text), **tokens})
PY
```

`*-session-stack.txt` reproduce las filas de Project OS del benchmark
principal; `/tmp/pos-bench/corpus/*` reproduce las filas del corpus público;
`*-minimal.json`, `*-compact.json`, `*-full-debug.json` y `*-full-kernel.txt`
reproducen el perfil interno.

## Límites de este benchmark

- Los números valen para la fecha y los commits declarados; los archivos del
  corpus evolucionan en sus repositorios y la reproducción solo es estable
  contra los commits pineados. Si el kernel o el corpus cambian, vuelve a
  medir y actualiza fecha, commits y tablas juntos.
- El corpus son cuatro archivos dogfood de los propios vendors: es verificable
  y no cherry-picked bajo la regla declarada, pero no representa a todos los
  proyectos ni a todas las formas de configurar cada herramienta.
- La equivalencia es funcional (contexto de instrucciones repo-wide cargado al
  inicio de sesión para la tarea declarada), no de contenido: cada archivo
  gobierna un proyecto distinto con contenido distinto.
- Un conteo de tokens depende del tokenizer y del modelo; usa el tokenizer de
  tu modelo real antes de planificar contexto con estas cifras.
- Medir tamaño no mide utilidad ni calidad: `minimal` es más pequeño porque
  devuelve menos guía, no porque sea siempre suficiente. El default práctico
  sigue siendo `compact` (ver [empezar.md](empezar.md)).
- Este documento no publica precios, costos ni ahorros de suscripciones, no
  compara features y no afirma que Project OS reemplace herramienta alguna.

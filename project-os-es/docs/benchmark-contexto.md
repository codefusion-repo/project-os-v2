# Perfil interno reproducible de hidratación

**Cuánto contrato ya resuelto devuelve el resolver de Project OS en cada
nivel de hidratación, medido contra dos referencias internas construidas
desde el kernel real, para una misma tupla declarada.** Este es el benchmark
reproducible de contexto que exige ADR 0004
([0004-public-presentation-and-packaging.md](../../docs/decisions/0004-public-presentation-and-packaging.md))
y es un **perfil interno**: mide el kernel de Project OS contra sí mismo y no
compara contra ninguna herramienta externa. No mide calidad, no demuestra ni
promete ahorro alguno fuera de este perfil y no otorga permisos
(`boundary.output_not_permission`).

Este documento es el apéndice técnico de
[beneficios.md](beneficios.md), donde viven la explicación de beneficios,
la arquitectura modular y los escenarios propios de Project OS.

Versión inglesa: [context-benchmark.md](../../project-os-en/docs/context-benchmark.md).

## Tarea declarada y unidad de medida

- **Tarea declarada:** gobernar a un agente de codificación de terminal que
  implementa una unidad de trabajo acotada dentro de un repositorio.
- **Tupla medida:** `actor.terminal_agent` / `workflow.issue_implementation`
  / `mode.delegated_commit_pr`, idéntica en todas las alternativas.
- **Unidad de medida:** el stdout del resolver para esa tupla en cada nivel
  de hidratación, con `--compact` (JSON sin indentación), más las dos
  referencias internas descritas abajo. Queda fuera el contexto on-demand
  (operaciones MOS, templates, skills): se carga solo cuando se usa.

## Metodología declarada

- **Fecha de medición:** 2026-07-18.
- **Insumos:** commit `7a7aab501983` de `codefusion-repo/project-os-v2`; los
  insumos medidos (ambos directorios de kernel y
  `tools/project_os_resolve.py`) no cambian después de ese commit en la rama
  que corrige este documento.
- **Métricas:** bytes UTF-8, caracteres y tokens.
- **Tokenizer declarado:** `tiktoken` 0.13.0 (Python 3.12.13), con dos
  encodings públicos para mostrar la variación entre tokenizers: `o200k_base`
  y `cl100k_base`. Los conteos de tokens dependen del tokenizer y del modelo:
  ningún número de estas tablas es un ahorro universal.
- **Separación de kernel y estado vivo:** el output del resolver contiene solo
  contrato de kernel ya resuelto. No incluye issues, PRs, ramas, diffs ni
  ningún estado vivo: eso se lee desde GitHub al momento de la tarea y queda
  fuera de esta medición por diseño.

## Referencias internas

Dos referencias, construidas desde el kernel real:

- **Baseline por tupla (el exigido por ADR 0004):** un documento estático que
  inline-a exactamente lo que esta tupla necesita. Coincide con el output
  `full/debug` serializado: un documento estático no puede seleccionar por
  actor/workflow/mode, así que debe llevar el contrato completo de la tupla.
- **Kernel completo (techo interno):** la concatenación byte a byte de los 11
  archivos JSON del kernel, `manifest.json` primero y el resto en orden de
  nombre: lo que costaría inline-ar el kernel entero para servir cualquier
  tupla sin selección.

## Kernel español (default)

| Alternativa | Bytes | Caracteres | Tokens `o200k_base` | Tokens `cl100k_base` |
| --- | ---: | ---: | ---: | ---: |
| Resolver `minimal` | 15516 | 15516 | 3739 | 3856 |
| Resolver `compact` | 27801 | 27760 | 6418 | 6868 |
| Baseline por tupla (= `full/debug`) | 29251 | 29210 | 6839 | 7290 |
| Kernel completo (11 archivos) | 67020 | 66979 | 15334 | 16055 |

Reducción frente al baseline por tupla: `minimal` −47,0 % bytes (−45,3 %
tokens `o200k_base`, −47,1 % `cl100k_base`); `compact` −5,0 % bytes (−6,2 %,
−5,8 %). Frente al kernel completo (solo perfil interno): `minimal` −76,8 %
bytes (−75,6 %, −76,0 %); `compact` −58,5 % (−58,1 %, −57,2 %); `full/debug`
−56,4 % (−55,4 %, −54,6 %).

## Kernel inglés (selección explícita)

Misma tupla, mismos comandos, con `--kernel-dir project-os-en/kernel`:

| Alternativa | Bytes | Caracteres | Tokens `o200k_base` | Tokens `cl100k_base` |
| --- | ---: | ---: | ---: | ---: |
| Resolver `minimal` | 15288 | 15288 | 3576 | 3565 |
| Resolver `compact` | 26836 | 26836 | 5949 | 5946 |
| Baseline por tupla (= `full/debug`) | 28286 | 28286 | 6370 | 6368 |
| Kernel completo (11 archivos) | 65285 | 65285 | 14390 | 14368 |

Reducción frente al baseline por tupla: `minimal` −46,0 % bytes; `compact`
−5,1 %. Frente al kernel completo (solo perfil interno): `minimal` −76,6 %
bytes; `compact` −58,9 %; `full/debug` −56,7 %.

## Qué información conserva cada alternativa

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

mkdir -p /tmp/pos-bench
for kernel in project-os-es project-os-en; do
  for level in minimal compact full/debug; do
    python tools/project_os_resolve.py --actor actor.terminal_agent \
      --workflow workflow.issue_implementation --mode mode.delegated_commit_pr \
      --kernel-dir "$kernel/kernel" --hydration-level "$level" --compact \
      > "/tmp/pos-bench/$kernel-${level//\//-}.json"
  done
  (cd "$kernel/kernel" && cat manifest.json $(ls *.json | grep -v '^manifest')) \
    > "/tmp/pos-bench/$kernel-full-kernel.txt"
done

python - <<'PY'
from pathlib import Path
import tiktoken
encodings = {n: tiktoken.get_encoding(n) for n in ("o200k_base", "cl100k_base")}
for path in sorted(Path("/tmp/pos-bench").iterdir()):
    text = path.read_text(encoding="utf-8")
    tokens = {name: len(enc.encode(text)) for name, enc in encodings.items()}
    print(path.name, {"bytes": len(text.encode("utf-8")), "chars": len(text), **tokens})
PY
```

`*-minimal.json`, `*-compact.json` y `*-full-debug.json` reproducen las filas
de resolver; `*-full-kernel.txt` reproduce la fila de kernel completo. El
baseline por tupla es el mismo `*-full-debug.json` (ver «Referencias
internas»).

## Límites de este perfil

- Los números valen para la fecha y el commit declarados. Si el kernel o el
  resolver cambian, vuelve a medir y actualiza fecha, commit y tablas juntos.
- Este es un perfil interno: sus porcentajes comparan niveles de hidratación
  del propio kernel entre sí y **no deben citarse como ahorro frente a
  ninguna herramienta, convención o stack externo**.
- Un conteo de tokens depende del tokenizer y del modelo; usa el tokenizer de
  tu modelo real antes de planificar contexto con estas cifras.
- Medir tamaño no mide utilidad ni calidad: `minimal` es más pequeño porque
  devuelve menos guía, no porque sea siempre suficiente. El default práctico
  sigue siendo `compact` (ver [empezar.md](empezar.md)).
- Este documento no publica precios, costos ni ahorros de suscripciones, no
  compara features y no afirma que Project OS reemplace herramienta alguna.

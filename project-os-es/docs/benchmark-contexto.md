# Benchmark reproducible de contexto

**Cuánto contexto consume resolver el kernel según el nivel de hidratación,
comparado con un baseline monolítico construido desde el kernel real.** Este
benchmark solo mide tamaños: no mide calidad, no promete ahorros universales y
no otorga permisos (`boundary.output_not_permission`).

Versión inglesa: [context-benchmark.md](../../project-os-en/docs/context-benchmark.md).

## Metodología declarada

- **Fecha de medición:** 2026-07-14.
- **Estado del árbol:** commit `b9f8805` de `codefusion-repo/project-os-v2`
  (los directorios `project-os-es/kernel/` y `project-os-en/kernel/` no
  cambiaron en la rama que añadió este documento).
- **Tupla medida (idéntica en todas las alternativas):**
  `actor.terminal_agent` / `workflow.issue_implementation` /
  `mode.delegated_commit_pr`.
- **Corpus:** el stdout exacto del resolver CLI con `--compact` (JSON en una
  línea, newline final incluido) para cada nivel de hidratación, más un
  baseline monolítico: la concatenación byte a byte de los 11 archivos JSON del
  kernel, `manifest.json` primero y el resto en orden de nombre. El baseline
  representa lo que un bootloader estilo `AGENTS.md` tendría que inline-ar para
  servir cualquier tupla sin selección: un documento estático no puede
  seleccionar por actor/workflow/mode, que es exactamente lo que el resolver sí
  hace.
- **Métricas:** bytes UTF-8, caracteres y tokens.
- **Tokenizer declarado:** `tiktoken` 0.13.0 (Python 3.12.13), con dos
  encodings públicos para mostrar la variación entre tokenizers:
  `o200k_base` y `cl100k_base`. Los conteos de tokens dependen del tokenizer y
  del modelo: ningún número de esta tabla es un ahorro universal.
- **Separación de kernel y estado vivo:** el output del resolver contiene solo
  contrato de kernel ya resuelto. No incluye issues, PRs, ramas, diffs ni
  ningún estado vivo: eso se lee desde GitHub al momento de la tarea y queda
  fuera de esta medición por diseño.

## Resultados — kernel español (default)

| Alternativa | Bytes | Caracteres | Tokens `o200k_base` | Tokens `cl100k_base` |
| --- | ---: | ---: | ---: | ---: |
| Resolver `minimal` | 6696 | 6696 | 1646 | 1757 |
| Resolver `compact` | 15218 | 15213 | 3566 | 3885 |
| Resolver `full/debug` | 16504 | 16499 | 3939 | 4259 |
| Baseline monolítico (11 archivos) | 47584 | 47579 | 11000 | 11576 |

Reducción frente al baseline: `minimal` −85,9 % bytes (−85,0 % tokens
`o200k_base`, −84,8 % `cl100k_base`); `compact` −68,0 % bytes (−67,6 %,
−66,4 %); `full/debug` −65,3 % bytes (−64,2 %, −63,2 %).

## Resultados — kernel inglés (selección explícita)

Misma tupla, mismos comandos, con `--kernel-dir project-os-en/kernel`:

| Alternativa | Bytes | Caracteres | Tokens `o200k_base` | Tokens `cl100k_base` |
| --- | ---: | ---: | ---: | ---: |
| Resolver `minimal` | 6509 | 6509 | 1530 | 1539 |
| Resolver `compact` | 14384 | 14384 | 3202 | 3221 |
| Resolver `full/debug` | 15670 | 15670 | 3575 | 3595 |
| Baseline monolítico (11 archivos) | 46000 | 46000 | 10183 | 10200 |

Reducción frente al baseline: `minimal` −85,9 % bytes; `compact` −68,7 %;
`full/debug` −65,9 %.

## Qué información conserva cada alternativa

- **`minimal`** conserva la identidad de manifest/actor/mode/workflow, todos
  los límites aplicables, las acciones prohibidas, la evidencia requerida, los
  outputs permitidos y los estados: lo necesario para detener trabajo
  prohibido. No incluye la guía mandatoria completa.
- **`compact`** (default práctico) añade las reglas operativas mandatorias, el
  contexto operativo seleccionado y las referencias resolubles a
  artefactos/templates/skills: la vista con la que se ejecuta.
- **`full/debug`** añade los metadatos completos de la resolución seleccionada;
  es para revisión y auditoría, no el modo normal.
- **El baseline monolítico** conserva el kernel completo para todas las tuplas
  a la vez, sin seleccionar nada: cada sesión paga el contrato entero aunque
  solo use una tupla.

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
for level in minimal compact full/debug; do
  python tools/project_os_resolve.py --actor actor.terminal_agent \
    --workflow workflow.issue_implementation --mode mode.delegated_commit_pr \
    --kernel-dir project-os-es/kernel --hydration-level "$level" --compact \
    > "/tmp/pos-bench/${level//\//-}.json"
done
(cd project-os-es/kernel && cat manifest.json $(ls *.json | grep -v '^manifest')) \
  > /tmp/pos-bench/baseline.txt

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

Para el kernel inglés, repite los mismos comandos reemplazando
`project-os-es/kernel` por `project-os-en/kernel`.

## Límites de este benchmark

- Los números valen para la fecha y el commit declarados; si el kernel cambia,
  vuelve a ejecutar la reproducción y actualiza fecha, commit y tablas juntos.
- Un conteo de tokens depende del tokenizer y del modelo; usa el tokenizer de
  tu modelo real antes de planificar contexto con estas cifras.
- Medir tamaño no mide utilidad: `minimal` es más pequeño porque devuelve menos
  guía, no porque sea siempre suficiente. El default práctico sigue siendo
  `compact` (ver [empezar.md](empezar.md)).
- Este documento no publica precios, costos ni ahorros de suscripciones y no
  compara proveedores.

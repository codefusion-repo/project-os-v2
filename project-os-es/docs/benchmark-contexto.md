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

- **Fecha de medición:** 2026-07-26.
- **Insumos:** commit `9553b1c` de
  `codefusion-repo/project-os-v2`; los
  insumos medidos (ambos directorios de kernel y
  `tools/project_os_resolve.py`) no cambian después de ese commit en la rama
  que actualiza este documento.
- **Clase de cambio constante:** `change_class.small` en los tres niveles, y el
  nivel se selecciona explícitamente con `--hydration-level`. Desde #462 un
  workflow con mutación exige clase declarada, y la clase es material: aporta
  su propio bloque `change_class` y sus `remaining_gates`. Variar la clase junto
  con el nivel mezclaría dos efectos, así que aquí se mantiene fija y solo
  cambia la hidratación. Desde #468 los tres niveles están disponibles para
  cualquier clase: la clase gobierna los gates materiales y la densidad del
  reporte, nunca la hidratación.
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
| Resolver `minimal` | 15746 | 15746 | 3728 | 3920 |
| Resolver `compact` | 33103 | 33056 | 7453 | 8115 |
| Baseline por tupla (= `full/debug`) | 36989 | 36942 | 8429 | 9109 |
| Kernel completo (11 archivos) | 77405 | 77358 | 17395 | 18408 |

Reducción frente al baseline por tupla: `minimal` −57,4 % bytes (−55,8 %
tokens `o200k_base`, −57,0 % `cl100k_base`); `compact` −10,5 % bytes (−11,6 %,
−10,9 %). Frente al kernel completo (solo perfil interno): `minimal` −79,7 %
bytes (−78,6 %, −78,7 %); `compact` −57,2 % (−57,2 %, −55,9 %); `full/debug`
−52,2 % (−51,5 %, −50,5 %).

## Kernel inglés (selección explícita)

Misma tupla, mismos comandos, con `--kernel-dir project-os-en/kernel`:

| Alternativa | Bytes | Caracteres | Tokens `o200k_base` | Tokens `cl100k_base` |
| --- | ---: | ---: | ---: | ---: |
| Resolver `minimal` | 15421 | 15421 | 3521 | 3517 |
| Resolver `compact` | 31885 | 31885 | 6817 | 6819 |
| Baseline por tupla (= `full/debug`) | 35763 | 35763 | 7783 | 7786 |
| Kernel completo (11 archivos) | 75339 | 75339 | 16210 | 16214 |

Reducción frente al baseline por tupla: `minimal` −56,9 % bytes; `compact`
−10,8 %. Frente al kernel completo (solo perfil interno): `minimal` −79,5 %
bytes; `compact` −57,7 %; `full/debug` −52,5 %.

## Caso crítico normal (#468)

Hasta #468 la clase seleccionaba la hidratación: una resolución
`change_class.critical` sin override recibía automáticamente `full/debug`.
Desde #468 el default global es `compact` para cualquier clase. Esta sección
mide ese caso concreto sobre el mismo estado final, con la clase fija, de modo
que la única variable es la hidratación:

| Kernel | Antes (`full/debug` automático) | Después (`compact` por defecto) | Δ bytes | Δ % |
| --- | ---: | ---: | ---: | ---: |
| Español | 37590 | 33704 | −3886 | −10,3 % |
| Inglés | 36341 | 32463 | −3878 | −10,7 % |

En tokens: español 8558 → 7582 `o200k_base` (−11,4 %) y 9257 → 8263
`cl100k_base` (−10,7 %); inglés 7893 → 6927 (−12,2 %) y 7897 → 6930 (−12,2 %).

La fila «antes» reproduce exactamente la proyección que la clase activaba de
forma automática, ejecutando hoy `--change-class change_class.critical
--hydration-level full/debug`; la fila «después» ejecuta el mismo comando sin
`--hydration-level`. Medir ambas sobre el estado final aísla el efecto de la
hidratación del crecimiento del kernel, que este documento nunca suma.

Lo que **no** cambia entre esas dos filas, verificado en la misma resolución:
`formal_unit_required=true`, `pr_required=true`,
`review_level=review.independent`, `validation_level=validation.broad`,
`prior_docs=expected`, y un `output.execution_report` con los 10 campos
`must_include` de la densidad `full/debug`. La reducción es de contrato
serializado, no de gates ni de densidad del reporte.

Esta medición separa dos costos que antes se confundían:

- **costo de hidratación:** la diferencia de la tabla, el único efecto de #468;
- **lecturas externas del agente:** fuera del output del resolver y por tanto
  fuera de esta medición. Ningún nivel obliga a releer el kernel que el
  resolver ya procesó, así que una relectura manual no es atribuible al nivel.

## Eliminación total de la estructura de recibo y procedencia (#477)

Esta medición compara el baseline `main` inmediatamente anterior, commit
`4a22ce3`, con el commit de implementación
`9553b1c`, que fija todos los inputs medidos (kernels ES/EN y resolver). La
documentación posterior no cambia esos inputs; por eso los seis resultados son
los mismos en el head final de la rama del PR. En ambos lados se ejecutó la
misma tupla, `change_class.small`, niveles explícitos y JSON `--compact`.

| Kernel | Nivel | Antes (bytes UTF-8) | Después (bytes UTF-8) | Δ bytes | Δ % |
| --- | --- | ---: | ---: | ---: | ---: |
| ES | `minimal` | 16823 | 15746 | −1077 | −6,4 % |
| ES | `compact` | 34180 | 33103 | −1077 | −3,2 % |
| ES | `full/debug` | 38066 | 36989 | −1077 | −2,8 % |
| EN | `minimal` | 16498 | 15421 | −1077 | −6,5 % |
| EN | `compact` | 32962 | 31885 | −1077 | −3,3 % |
| EN | `full/debug` | 36840 | 35763 | −1077 | −2,9 % |

Los identificadores de esta lista aparecen solo como nombres históricos de la
estructura eliminada en el baseline: `context_receipt_contract`,
`context_receipt_key`, `context_plan`, `context_provenance`,
`executor_reported_fields` y `--context-provenance`. El estado después no
serializa ni expone ninguno; no existe un reemplazo funcional.

La comparación verifica que los límites, acciones prohibidas, evidencia
requerida, outputs permitidos, statuses, gates de la clase y densidad de reporte
siguen presentes y equivalentes en cada nivel. La reducción es estructura
retirada, no evidencia viva omitida: `Evidencia revisada`, la validación, los
riesgos, la degradación segura, la autorización exacta, secret safety y
fail-closed permanecen en sus contratos reales.

## Comparabilidad con mediciones anteriores

La medición publicada el 2026-07-18 sobre `7a7aab5` **no es directamente
comparable** con las tablas de arriba: precede al contrato de clases de cambio
que introdujeron #462 y PR #463, así que su resolución no transportaba el
bloque `change_class`, sus `remaining_gates` ni el `proportionality_contract`
del workflow, y tampoco exigía declarar una clase.

Entre `7a7aab5` y `3de282f` el kernel completo creció de 67020 a 79302 bytes en
español (+18,3 %) y de 65285 a 77309 en inglés (+18,4 %). Ese **crecimiento
acumulado del kernel** —no #464— explica que las filas de resolver sean mayores
que las de julio 18. La contribución de #464, medida contra su baseline
inmediato con la clase constante, es una **reducción** en los tres niveles y en
ambos kernels. Son dos efectos distintos y este documento no los suma.

## Qué información conserva cada alternativa

- **`minimal`** conserva la identidad de manifest/actor/mode/workflow, todos
  los límites aplicables, las acciones prohibidas, la evidencia requerida, los
  outputs permitidos y los estados: lo necesario para detener trabajo
  prohibido. No incluye la guía mandatoria completa.
- **`compact`** (default práctico) añade las reglas operativas mandatorias, el
  contexto operativo seleccionado y las referencias resolubles a
  artefactos/templates/skills: la vista con la que se ejecuta.
- **El baseline por tupla (`full/debug`)** añade los metadatos completos de la
  resolución seleccionada; como nivel de hidratación es un opt-in para auditar
  el kernel o debuggear el resolver, nunca el modo normal ni una consecuencia
  de la clase.
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
      --change-class change_class.small --hydration-level "$level" \
      --kernel-dir "$kernel/kernel" --compact \
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

Para reproducir el caso crítico normal de #468, sobre el estado final y sin
worktree adicional:

```sh
for kernel in project-os-es project-os-en; do
  python tools/project_os_resolve.py --actor actor.terminal_agent \
    --workflow workflow.issue_implementation --mode mode.delegated_commit_pr \
    --change-class change_class.critical --hydration-level full/debug \
    --kernel-dir "$kernel/kernel" --compact | wc -c
  python tools/project_os_resolve.py --actor actor.terminal_agent \
    --workflow workflow.issue_implementation --mode mode.delegated_commit_pr \
    --change-class change_class.critical \
    --kernel-dir "$kernel/kernel" --compact | wc -c
done
```

La segunda invocación de cada par declara `"hydration_level": "compact"` y
conserva los mismos `remaining_gates` y el mismo `must_include` de 10 campos
que la primera; `jq '.hydration_level, .resuelto.change_class.remaining_gates'`
lo verifica sin releer el kernel.

Para reproducir exactamente el benchmark de #477, en un checkout con esos
commits disponibles:

```sh
git worktree add --detach /tmp/pos-477-before 4a22ce3
git worktree add --detach /tmp/pos-477-after 9553b1c

python - /tmp/pos-477-before /tmp/pos-477-after <<'PY'
import json
import subprocess
import sys
from pathlib import Path

before, after = map(Path, sys.argv[1:])
levels = ("minimal", "compact", "full/debug")
kernels = ("project-os-es", "project-os-en")
retired = (
    "context_receipt", "context_plan", "context_provenance",
    "executor_reported_fields", "detailed_provenance_reasons",
)

def resolve(root, kernel, level):
    return subprocess.run([
        sys.executable, "tools/project_os_resolve.py",
        "--actor", "actor.terminal_agent",
        "--workflow", "workflow.issue_implementation",
        "--mode", "mode.delegated_commit_pr",
        "--change-class", "change_class.small",
        "--hydration-level", level,
        "--kernel-dir", f"{kernel}/kernel", "--compact",
    ], cwd=root, check=True, capture_output=True, text=True).stdout

def normalize(value):
    if isinstance(value, dict):
        return {
            key: normalize(item) for key, item in value.items()
            if key not in {"context_receipt_key", "context_receipt_contract"}
        }
    if isinstance(value, list):
        return [normalize(item) for item in value]
    return value

for kernel in kernels:
    for level in levels:
        old, new = resolve(before, kernel, level), resolve(after, kernel, level)
        old_payload, new_payload = json.loads(old), json.loads(new)
        assert len(new.encode("utf-8")) < len(old.encode("utf-8"))
        assert not any(name in new for name in retired)
        for field in ("limites", "estados_permitidos"):
            assert old_payload["resuelto"][field] == new_payload["resuelto"][field]
        for field in ("required_evidence", "minimum_evidence", "allowed_outputs"):
            assert normalize(old_payload["resuelto"]["workflow"][field]) == new_payload["resuelto"]["workflow"][field]
        assert old_payload["resuelto"]["change_class"] == new_payload["resuelto"]["change_class"]
        print(kernel, level, len(old.encode("utf-8")), len(new.encode("utf-8")))
PY
```

## Límites de este perfil

- Los números valen para la fecha y el commit declarados. Si el kernel o el
  resolver cambian, vuelve a medir y actualiza fecha, commit y tablas juntos.
- Este es un perfil interno: sus porcentajes comparan niveles de hidratación
  del propio kernel entre sí y **no deben citarse como ahorro frente a
  ninguna herramienta, convención o stack externo**.
- Un conteo de tokens depende del tokenizer y del modelo; usa el tokenizer de
  tu modelo real antes de planificar contexto con estas cifras.
- Medir tamaño no mide utilidad ni calidad: `minimal` es más pequeño porque
  devuelve menos guía, no porque sea siempre suficiente. El default global
  sigue siendo `compact` (ver [empezar.md](empezar.md)).
- La reducción del caso crítico es de contrato serializado y no toca gates,
  autoridad ni densidad del reporte; tampoco cubre relecturas manuales.
- Este documento no publica precios, costos ni ahorros de suscripciones, no
  compara features y no afirma que Project OS reemplace herramienta alguna.

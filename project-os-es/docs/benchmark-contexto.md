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

- **Fecha de medición:** 2026-07-25.
- **Insumos:** commit `5afb2c7` de `codefusion-repo/project-os-v2`; los
  insumos medidos (ambos directorios de kernel y
  `tools/project_os_resolve.py`) no cambian después de ese commit en la rama
  que actualiza este documento.
- **Clase de cambio constante:** `change_class.small` en los tres niveles, y el
  nivel se selecciona explícitamente con `--hydration-level`. Desde #462 un
  workflow con mutación exige clase declarada, y la clase es material: aporta
  su propio bloque `change_class`, sus `remaining_gates` y su densidad por
  defecto. Variar la clase junto con el nivel mezclaría dos efectos, así que
  aquí se mantiene fija y solo cambia la hidratación. El resolver lo permite
  porque un nivel explícito puede mantener o elevar la densidad contractual de
  una clase; solo bloquea reducirla.
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
| Resolver `minimal` | 16760 | 16760 | 3956 | 4139 |
| Resolver `compact` | 33760 | 33713 | 7612 | 8251 |
| Baseline por tupla (= `full/debug`) | 38250 | 38203 | 8716 | 9389 |
| Kernel completo (11 archivos) | 78981 | 78934 | 17756 | 18728 |

Reducción frente al baseline por tupla: `minimal` −56,2 % bytes (−54,6 %
tokens `o200k_base`, −55,9 % `cl100k_base`); `compact` −11,7 % bytes (−12,7 %,
−12,1 %). Frente al kernel completo (solo perfil interno): `minimal` −78,8 %
bytes (−77,7 %, −77,9 %); `compact` −57,3 % (−57,1 %, −55,9 %); `full/debug`
−51,6 % (−50,9 %, −49,9 %).

## Kernel inglés (selección explícita)

Misma tupla, mismos comandos, con `--kernel-dir project-os-en/kernel`:

| Alternativa | Bytes | Caracteres | Tokens `o200k_base` | Tokens `cl100k_base` |
| --- | ---: | ---: | ---: | ---: |
| Resolver `minimal` | 16446 | 16446 | 3752 | 3741 |
| Resolver `compact` | 32592 | 32592 | 6988 | 6983 |
| Baseline por tupla (= `full/debug`) | 37051 | 37051 | 8061 | 8057 |
| Kernel completo (11 archivos) | 76958 | 76958 | 16583 | 16560 |

Reducción frente al baseline por tupla: `minimal` −55,6 % bytes; `compact`
−12,0 %. Frente al kernel completo (solo perfil interno): `minimal` −78,6 %
bytes; `compact` −57,7 %; `full/debug` −51,9 %.

## Costo del recibo de fuentes (#464)

Antes de #464 cada resolución transportaba el contrato completo del recibo más
un `context_plan` que repetía parte de él, en los tres niveles. Esta sección
compara el **baseline inmediato** `3de282f` con el estado corregido de #464,
ejecutando exactamente el mismo comando en ambos: misma tupla, misma
`change_class.small` y el mismo `--hydration-level` explícito.

Resolución completa, kernel español, bytes UTF-8:

| Nivel | `3de282f` | Con #464 | Δ bytes | Δ % |
| --- | ---: | ---: | ---: | ---: |
| `minimal` | 19332 | 16760 | −2572 | −13,3 % |
| `compact` | 36211 | 33760 | −2451 | −6,8 % |
| `full/debug` | 40712 | 38250 | −2462 | −6,0 % |

Resolución completa, kernel inglés, bytes UTF-8:

| Nivel | `3de282f` | Con #464 | Δ bytes | Δ % |
| --- | ---: | ---: | ---: | ---: |
| `minimal` | 19008 | 16446 | −2562 | −13,5 % |
| `compact` | 35063 | 32592 | −2471 | −7,0 % |
| `full/debug` | 39533 | 37051 | −2482 | −6,3 % |

Casi toda esa diferencia proviene del recibo. Midiendo por separado las dos
superficies dentro de la misma resolución —cada subobjeto reserializado con
`json.dumps(obj, ensure_ascii=False)`, el mismo formato con el que el resolver
emite su salida, y contado en bytes UTF-8— el costo del recibo por resolución
queda así:

| Superficie | Antes (ES) | Antes (EN) | Después |
| --- | ---: | ---: | ---: |
| `context_receipt_contract` | 1300 | 1300 | 921 |
| `context_plan` en la ruta normal | 2175–2265 | 2165–2255 | 0 |
| Total del recibo por resolución | 3475–3565 | 3465–3555 | 921 |

Los rangos cubren los tres niveles: el contrato del recibo no varía con la
hidratación y el `context_plan` anterior crecía de `minimal` a `full/debug`.

Como el formato coincide con el de la salida, las cifras son aditivas contra
los totales. En `minimal` el recibo explica la diferencia completa: −2554 bytes
de contenido más los 18 de la clave `context_plan` suprimida dan exactamente
los −2572 de la tabla anterior (−2544 + 18 = −2562 en el kernel inglés). En
`compact` y `full/debug` la reducción del recibo es mayor que la neta porque
#464 también añadió prosa a las reglas operativas —200 bytes en español y 170
en inglés—, que solo se transportan desde `compact`. El saldo es negativo en
los seis casos medidos.

La procedencia detallada sigue disponible fuera de la ruta normal con
`--context-provenance <razón>`, y ese costo ya no se paga en cada resolución.

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

Para reproducir la comparación de #464 basta ejecutar ese mismo bucle en un
worktree del baseline y volver a comparar:

```sh
git worktree add /tmp/pos-base 3de282f07c65f8751d6827dd941dba7cbf90ef86 --detach
```

Y para el desglose por superficie, sobre cualquiera de los dos estados:

```sh
python - <<'PY'
import json, subprocess, sys
for level in ("minimal", "compact", "full/debug"):
    out = subprocess.run([sys.executable, "tools/project_os_resolve.py",
        "--actor", "actor.terminal_agent",
        "--workflow", "workflow.issue_implementation",
        "--mode", "mode.delegated_commit_pr",
        "--change-class", "change_class.small",
        "--hydration-level", level,
        "--kernel-dir", "project-os-es/kernel", "--compact"],
        capture_output=True, text=True, check=True).stdout
    payload = json.loads(out)
    def size(obj):
        if obj is None:
            return 0
        return len(json.dumps(obj, ensure_ascii=False).encode("utf-8"))
    print(level,
          "receipt", size(payload["resuelto"]["workflow"].get("context_receipt_contract")),
          "plan", size(payload.get("context_plan")),
          "total", len(out.encode("utf-8")))
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
  devuelve menos guía, no porque sea siempre suficiente. El default práctico
  sigue siendo `compact` (ver [empezar.md](empezar.md)).
- Este documento no publica precios, costos ni ahorros de suscripciones, no
  compara features y no afirma que Project OS reemplace herramienta alguna.

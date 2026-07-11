# AGENTS.md

AGENTS.md es el bootloader terminal de `codefusion-repo/project-os-v2`.
No es fuente de verdad ni concede permisos. El comportamiento genérico vive en
`project-os-es/kernel/`; los hechos de producto, dominio e implementación se
reconstruyen desde la evidencia viva de este repositorio.

## Identidad del repositorio

Estas rutas y la versión adoptada son configuración de máquina/adopción, no
estado vivo. Conserva estos campos y orden al adaptar esta superficie.

PROJECT_NAME = project-os-v2
REPOSITORY_NAME = codefusion-repo/project-os-v2
REPOSITORY_LOCAL_PATH = $HOME/projects/personal/project-os-v2/
DEFAULT_BRANCH = main
WORK_BRANCH_PATTERN = work/*
PM_FACING_LANGUAGE = es
KERNEL_REPOSITORY = codefusion-repo/project-os-v2
KERNEL_LOCAL_PATH = $HOME/projects/personal/project-os-v2/project-os-es/kernel/
KERNEL_VERSION_ADOPTED = tracks latest

## Resolución del kernel

Antes de trabajo no trivial, lee `project-os-es/kernel/manifest.json` y sigue
su `resolution_sequence`. En esta superficie terminal, el fast path es:

```sh
cd "$(git rev-parse --show-toplevel)"
if [ -d .venv ]; then . .venv/bin/activate; fi
python tools/project_os_resolve.py --actor <actor> --workflow <workflow> \
  --mode <mode> --kernel-dir project-os-es/kernel [--skill skill.<id>]
```

El resolver acelera la resolución; el manifest sigue siendo canónico. Ambos
solo dan forma y nunca autorizan una acción. Consulta artefactos, templates y
skills desde las referencias resueltas, sin copiar sus contratos aquí.

## Evidencia viva

Reconstruye el estado del trabajo desde GitHub, git, el roadmap canónico `#274`
y los ADRs de `docs/decisions/` cuando apliquen. No lo guardes en este archivo.
Ante kernel, evidencia, autoridad o validación requerida faltantes o ambiguos,
falla cerrado según el kernel resuelto.

## Notas propias del repositorio

- Conserva solo comandos estables, paths protegidos, restricciones de dominio,
  seguridad o escalaciones específicas del repositorio.
- Para cambios web/API/user-facing, considera los riesgos OWASP relevantes.
- No expongas valores sensibles; reporta rutas, nombres de variables y tipo de
  riesgo con `[REDACTED]`.
- La política completa de seguridad, trazabilidad y validación vive en
  `project-os-es/docs/reglas.md` y el kernel resuelto.

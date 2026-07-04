# Empezar con Project OS

**Guía breve para arrancar bien: confirma lo externo, elige superficie,
configura el browser, prepara terminal solo si vas a delegar y abre la primera
sesión con evidencia real.**

## 1. Requisitos externos

Project OS no controla estos puntos. Tenlos listos antes de operar:

- **Repo target creado en GitHub.** Es el producto que vas a adoptar,
  implementar, revisar o auditar.
- **Cuenta GitHub conectada con acceso al repo target.** El acceso conectado
  requerido es al target: issues, PRs, diffs y docs según el flujo.
- **Browser chat con lectura GitHub/repo target en modo read-only.** Recomendado:
  ChatGPT con GitHub conectado. Otra superficie sirve si permite proyecto/chat
  con instrucciones y lectura del repo target.
- **Terminal/local con acceso GitHub al target si delegarás implementación.**
  Debe poder leer y escribir lo aprobado; si el flujo usa issues o PRs, también
  necesita acceso a issues/PRs del target.
- **Repo Project OS readable.** Úsalo como fuente pública o legible de kernel,
  operaciones, adapters y docs; no lo presentes como requisito privado ligado a
  una cuenta especial.
- **Sin secretos para empezar.** No necesitas `.env`, tokens, llaves privadas ni
  credenciales de producción para activar una sesión.

## 2. Superficies

La capacidad depende de la superficie, no del rol:

- **Humano PM.** Decide alcance, aprobaciones exactas, merge, cierre de issues,
  labels, tags, releases, settings, secretos y despliegues.
- **Browser chat.** Sirve para draft, revision, routing y analisis. Permanece
  read-only/draft-only aunque la herramienta conectada pudiera escribir.
- **Terminal agent.** Ejecuta implementación delegada: edita en scope, valida,
  hace commit/push y abre PR draft solo con evidencia viva, rama correcta y
  aprobación PM exacta.

Dos repos aparecen en casi todos los flujos:

- **Repo Project OS:** kernel, operaciones, adapters y docs.
- **Repo target:** producto donde se adopta o ejecuta el trabajo. En el
  desarrollo de Project OS, target y Project OS pueden ser el mismo repo.

Antes de pedir trabajo, nombra cuál repo cumple cada rol.

## 3. Configuración browser

Haz esto en la superficie browser antes de usarla para draft o revisión:

1. Usa ChatGPT recomendado u otra superficie browser que permita proyecto/chat
   con instrucciones persistentes.
2. Carga las instrucciones de Project OS o el adapter del target cuando exista;
   para browser project/chat usa
   [`project-os-es/adapters/BROWSER_CHAT.target.md`](../adapters/BROWSER_CHAT.target.md)
   como bootloader.
3. Conecta o verifica GitHub en esa superficie.
4. Confirma que puede leer el repo target; cuando aplique, confirma también que
   puede leer el repo Project OS.
5. Si no puede leer una evidencia requerida, debe responder
   `status.needs_context` con lo que falta. No debe inventar estado de issues,
   PRs, ramas, diffs, validación ni roadmap.

## 4. Preparación terminal/local

Haz esto solo cuando vayas a delegar implementación a un terminal agent:

1. Ten el repo target clonado o el workspace local listo.
2. Verifica `gh auth status` para el repo target.
3. Confirma acceso a issues y PRs del target cuando el agente necesite leerlos,
   comentarlos o abrir PRs.
4. Ten Python disponible si usaras el resolver.
5. Adopta o revisa el adapter terminal del target con
   [`project-os-es/adapters/AGENTS.target.md`](../adapters/AGENTS.target.md) y
   conoce `KERNEL_LOCAL_PATH` desde ese adapter.

Fast path del resolver cuando el repo ya está listo:

```sh
python -m tools.project_os_resolve --actor <actor> --workflow <workflow> \
  --mode <mode> --kernel-dir "$KERNEL_LOCAL_PATH"
```

La resolución manual de `kernel/manifest.json` sigue siendo el fallback
canónico.

Cuando draftees outputs, el resolver puede exponer artefactos con
`required_template`; usa ese template de
[`project-os-es/templates/`](../templates/README.md) como forma del output, no
como permiso.

## 5. Primera sesión

1. **Elige superficie.** Usa browser chat para draft, revisión y routing;
   terminal agent para implementación delegada; Humano PM para cierre, merge,
   settings, secretos y despliegues.
2. **Activa browser chat con
   [MOS-0.1](../operaciones/fase-0/MOS-0.1-activar-sesion-browser-chat.md).**
3. **Verifica adopción cuando haya target con
   [MOS-0.5](../operaciones/fase-0/MOS-0.5-verificar-adopcion-del-target.md).**
   Si el target aún no adoptó Project OS, usa
   [MOS-0.2](../operaciones/fase-0/MOS-0.2-iniciar-proyecto-nuevo.md) para
   proyecto nuevo o
   [MOS-0.3](../operaciones/fase-0/MOS-0.3-adoptar-proyecto-existente.md) para
   proyecto existente.
4. **Usa
   [MOS-0.6](../operaciones/fase-0/MOS-0.6-transferir-contexto-de-sesion.md)
   solo si la sesión está incoherente, agotada o necesita traspaso.**
5. **Siguiente paso:** lee [reglas.md](reglas.md) y luego [ritmo.md](ritmo.md).

# Asistente Agentic QA DMAIC

Propósito: flujo agnóstico al proyecto para triage de defectos y soporte de análisis de causa raíz que combina Six Sigma y QA de software.

## Qué hace este starter

1. Lee el contexto del proyecto desde archivos YAML.
2. Lee eventos de defectos sintéticos desde un archivo JSON.
3. Ejecuta un flujo agentic de 3 pasos:
   - Planner: selecciona la ruta de análisis y verifica campos requeridos.
   - Analyzer: propone hipótesis de causa raíz y acciones CAPA.
   - Validator: verifica confianza y cumplimiento de quality gates.
4. Calibra la confianza usando señales de completitud de datos y calidad narrativa.
5. Calcula score y tier de priorización para ordenar acciones de triage.
6. Aplica RCA de 5 Whys antes de liberar CAPA.
7. Aplica CAPA con compuerta por evidencia: si el soporte de la hipótesis es débil o faltan artefactos de evidencia, la salida cambia a acciones de investigación primero.
8. Puntúa la calidad de artefactos de evidencia y valida la trazabilidad de artefactos contra IDs de defecto.
9. Requiere un plan de experimento de validación CAPA para cada recomendación CAPA confirmada.
10. Ingiere resultados de experimentos y calcula score de efectividad CAPA (effective/partial/ineffective/not_available).
11. Soporta sesiones RCA interactivas con compuertas de checkpoint y lógica adaptativa de stop/continue.
12. Genera un reporte de salida estructurado en data/output.
13. Incluye visibilidad de ejecución por defecto con `agent_trace` por defecto en reportes batch (planner/analyzer/validator por defecto).
14. Agrega una fila de evidencia para seguimiento de evaluación.

## Estructura del proyecto

- src: implementación
- project-context: configuración reutilizable de cliente/proyecto/estándares
- data/input: muestras de entrada de defectos sintéticos
- data/output: reportes de análisis generados
- evidence: logs para evidencia de evaluación
- metrics: KPIs base y por sprint

## Inicio rápido

1. Abre una terminal en esta carpeta.
2. Ejecuta:

   python src/main.py --context project-context/baseline-project.yaml --input data/input/synthetic_defects_sprint1.json --output data/output/report_sprint1.json

3. Revisa:
- data/output/report_sprint1.json
- evidence/evidence_log.csv

## Modo de sesión RCA interactiva

Inicia una sesión para un defecto:

```text
python src/main.py start-rca --context project-context/baseline-project.yaml --input data/input/synthetic_defects_with_evidence.json --defect-id PRJ-DEF-201 --session evidence/rca_sessions/prj-def-201.json
```

Responde el Why actual con evidencia y flags de checkpoint:

```text
python src/main.py answer-rca --session evidence/rca_sessions/prj-def-201.json --answer "Because the merge process allowed duplicate keys after replay due to a missing idempotency guard." --evidence-ref "PRJ-DEF-201_sql-output-dup-count-2026-08-07.csv" --evidence-ref "PRJ-DEF-201_pipeline-run-log-merge-window-2026-08-07.txt" --controllable
```

Revisa el Why actual en lugar de agregar un segundo intento:

```text
python src/main.py revise-rca --session evidence/rca_sessions/prj-def-201.json --answer "Because the merge process replayed records without an idempotency guard, duplicate keys were inserted into the target table." --evidence-ref "PRJ-DEF-201_sql-output-dup-count-2026-08-07.csv" --evidence-ref "PRJ-DEF-201_pipeline-run-log-merge-window-2026-08-07.txt" --controllable
```

Consulta estado de sesión:

```text
python src/main.py status-rca --session evidence/rca_sessions/prj-def-201.json
```

Exporta un reporte formal del caso RCA:

```text
python src/main.py export-rca-report --session evidence/rca_sessions/prj-def-201.json --output evidence/rca_reports/prj-def-201.md
```

Ejecuta un flujo RCA guiado en un solo comando (wizard interactivo en terminal):

```text
python src/main.py guided-rca --context project-context/baseline-project.yaml --input data/input/synthetic_defects_with_evidence.json --defect-id PRJ-DEF-201 --role qa
```

Flags opcionales del modo guiado:
- `--session` para reutilizar o fijar una ruta de sesión
- `--output-report` para personalizar la ruta del reporte markdown exportado
- `--role` valores: `dev`, `qa`, `sre`, `release-manager`
- `--quick-plan` para ejecutar en modo no interactivo desde un plan JSON predefinido

Ejecuta modo guiado no interactivo (modo rápido):

```text
python src/main.py guided-rca --context project-context/baseline-project.yaml --input data/input/synthetic_defects_with_evidence.json --defect-id PRJ-DEF-201 --role qa --quick-plan data/input/quick_plan_prj-def-201.json --session evidence/rca_sessions/prj-def-201-quick.json --output-report evidence/rca_reports/prj-def-201-quick.md
```

Esquema del quick plan:

```json
{
   "default_evidence_refs": ["artifact-a", "artifact-b"],
   "default_flags": {
      "controllable": true,
      "resolved": false,
      "prevents_recurrence": false
   },
   "answers": [
      {
         "answer": "Because ..."
      },
      {
         "answer": "Because ...",
         "evidence_refs": ["artifact-c"],
         "resolved": true,
         "prevents_recurrence": true
      }
   ]
}
```

Ejemplo de quick plan incluido:
- `data/input/quick_plan_prj-def-201.json`

Mejoras del modo guiado para adopción real del equipo:
- flujo de sesión en un solo comando desde inicio hasta exportación de reporte
- plantillas de respuesta por rol mostradas en cada paso Why
- sugerencia automática de evidencia por defect ID desde `evidence/` y `data/`
- exportación automática de reporte cuando se alcanza la condición de stop
- modo rápido no interactivo opcional para demos y ejecución asistida por CI

## Exportación CSV de CAPA (ADO/Jira/Generic)

Exporta tareas CAPA desde una sesión RCA confirmada como CSV listo para importación:

```text
python src/main.py export-capa-csv --session evidence/rca_sessions/prj-def-201-quick.json --output evidence/capa_exports/prj-def-201-ado.csv --provider ado --assignee qa.lead@sampleclient.com --due-date 2026-08-28
```

Ejemplo en formato Jira:

```text
python src/main.py export-capa-csv --session evidence/rca_sessions/prj-def-201-quick.json --output evidence/capa_exports/prj-def-201-jira.csv --provider jira --assignee qa.lead --due-date 2026-08-28
```

Opciones de provider:
- `ado`: columnas para importación en Azure DevOps
- `jira`: columnas para importación CSV en Jira
- `generic`: esquema neutro para tooling personalizado

## Exportación CSV de casos de prueba ADO

Exporta work items de tipo Test Case compatibles con ADO desde una sesión RCA usando el orden de campos requerido:

```text
python src/main.py export-ado-testcases-csv --session evidence/rca_sessions/prj-def-201-quick.json --output evidence/capa_exports/prj-def-201-ado-testcases.csv --assigned-to qa.lead@sampleclient.com --area-path SampleProject\\QA --iteration-path SampleProject\\Sprint-2 --state Design
```

Ejemplo en modo expandido (agrega variantes negativas y de frontera por cada caso base):

```text
python src/main.py export-ado-testcases-csv --session evidence/rca_sessions/prj-def-201-quick.json --output evidence/capa_exports/prj-def-201-ado-testcases-expanded.csv --assigned-to qa.lead@sampleclient.com --area-path SampleProject\\QA --iteration-path SampleProject\\Sprint-2 --state Design --variant-set expanded
```

Columnas exportadas (orden exacto):
- `ID`
- `Work Item Type`
- `Title`
- `Assigned To`
- `State`
- `Area Path`
- `Iteration Path`
- `Description`
- `Repro Steps`
- `System Info`
- `Acceptance Criteria`

Notas:
- La salida es CSV delimitado por comas.
- `Work Item Type` se establece como `Test Case` en todas las filas.
- `ID` queda vacío para que ADO lo asigne en la importación.
- El contenido de múltiples pasos se representa con `\\n` dentro de campos entre comillas para mantener integridad de filas.
- `--variant-set standard` exporta solo casos base alineados a CAPA (default).
- `--variant-set expanded` exporta estándar + variantes negativas + de frontera.

La sesión RCA interactiva:
- continúa si se necesita otro Why
- se detiene cuando el checkpoint confirma una causa controlable que debería prevenir recurrencia
- se pausa para más evidencia cuando la respuesta es demasiado débil para avanzar

## Cómo adaptar a otro proyecto

1. Copia project-context/project-profile.template.yaml en un nuevo archivo de perfil.
2. Completa estándares, flujo de trabajo, mapeo de severidad y criterios de aceptación.
3. Usa solo entradas de defectos sintéticos o no sensibles.
4. Ejecuta el mismo comando con el nuevo archivo de contexto.

## Checklist de evidencia por ejecución

Después de cada ejecución, captura:
- nombre del archivo de entrada y timestamp
- número de defectos analizados
- sugerencias aceptadas vs marcadas
- correcciones manuales realizadas
- delta estimado en tiempo de triage
- artefactos de evidencia enlazados por defecto cuando se espera confirmación CAPA
- métricas de resultado del experimento (baseline vs post, logro del objetivo, tamaño de muestra, señal de regresión)

Usa evidence/evidence_log.csv y evidence/validation_corrections_log.md.

## Ejecución guiada

Usa DAY_BY_DAY_SPRINT1_GUIDE.md para una cadencia de implementación de 10 días con checkpoints de evidencia.

## Web UI local (localhost)

Ejecuta el servidor local de UI:

```text
python src/web_app.py --host 127.0.0.1 --port 8787
```

Abre en navegador:

```text
http://127.0.0.1:8787
```

Qué soporta la UI:
- Inicio de sesión RCA desde selección de contexto/entrada/defecto
- El dropdown de Defect ID se carga automáticamente desde la lista JSON de entrada seleccionada (campo `defect_id`)
- Override manual de Defect ID cuando necesites escribir un ID que no aparece en el dropdown
- Cargar la sesión guardada más reciente desde un selector
- Ejecución de quick plan con un clic (no interactivo)
- Responder o revisar nodos Why con referencias de evidencia y flags de checkpoint
- Tarjetas verticales de opciones (`controllable`, `resolved`, `prevents recurrence`, `revise current node`) con explicación inline para usabilidad
- Bloque de ayuda de stop lógico para aclarar cierre temprano antes de Why 5 cuando se cumplen criterios de checkpoint
- Refrescar e inspeccionar el estado en vivo de la sesión
- Exportar reporte RCA, CSV CAPA y CSV de Test Cases ADO
- Visor de trazas de agentes para reportes batch: selección de reporte + defecto para inspeccionar `agent_trace`

Endpoint de salud de API:

```text
http://127.0.0.1:8787/api/health
```

Endpoint de trazas de agentes:

```text
http://127.0.0.1:8787/api/report-agent-trace?report=data/output/report_sprint1_orchestrated.json
```

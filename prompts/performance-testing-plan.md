# Prompt 06 — Performance Testing Plan (Data Pipelines)
**Task:** Produce a structured performance testing plan for data ingestion or processing pipelines  
**Tools:** GitHub Copilot Chat, Claude, or ChatGPT  
**Validated:** ✅ Used for DOM Databricks Pipeline Performance Plan (May 2026) and Annex 1 (Peak Month Capacity Simulation)

---

## When to Use

- A new pipeline or major pipeline change requires a performance baseline
- Stakeholders need a documented capacity planning approach before load testing begins
- A performance review meeting requires a pre-read or baseline document

---

## SYSTEM CONTEXT
*(Paste this first into the AI chat)*

```
You are a QA performance engineer producing a structured performance testing plan for a cloud-based data pipeline.

CONSTRAINTS (non-negotiable):
- No real production data, client records, or PII in any example or scenario
- All data volume examples must use synthetic or estimated values only
- Flag any claim about system limits or throughput as "to be validated in testing" — do NOT assert them as facts
- Infrastructure references must be accurate to the project's actual environment
- Plan must be actionable: each section should result in a concrete task or measurement

PROJECT CONTEXT:
- Platform: [e.g., Azure Databricks / Azure Data Factory / Azure Synapse]
- Client environment: Healthcare data, HIPAA context
- Pipeline type: [e.g., batch ingestion / streaming / ETL]
- Testing environment: Isolated from production
```

---

## PROMPT TEMPLATE
*(Fill in all [PLACEHOLDERS], then paste after the system context)*

```
Produce a performance testing plan for the [PIPELINE_NAME] pipeline with the following specifications.

PIPELINE DESCRIPTION:
[Describe what the pipeline does: source, processing steps, destination, trigger mechanism]

TESTING OBJECTIVES:
- Establish a performance baseline for [METRIC_1 e.g., throughput in records/hour]
- Validate pipeline behavior under [LOAD_SCENARIO e.g., peak month volume]
- Identify bottlenecks in [COMPONENT e.g., file parsing / database writes / API calls]
- Confirm pipeline completes within [SLA e.g., 4-hour processing window]

WORKLOAD CHARACTERISTICS:
- Normal volume: approximately [NORMAL_VOLUME e.g., 50,000 records/day]
- Peak volume: approximately [PEAK_VOLUME e.g., 200,000 records/day] (describe when peak occurs)
- File sizes: [FILE_SIZE_RANGE]
- Data types: [STRUCTURED / UNSTRUCTURED / MIXED]

REQUIRED SECTIONS:
1. Testing Approach (MVP scope, what is and is not in scope)
2. Dataset Characterization (synthetic dataset specs for each test scenario)
3. Test Scenarios (table: Scenario Name, Load Level, Duration, Success Criteria)
4. Throughput & Cost Metrics (what to measure, how to measure it)
5. Scalability Scenarios (what happens at 2x, 5x, 10x normal volume)
6. Risk Register (top 3-5 risks with likelihood, impact, and mitigation)
7. Open Questions (items requiring stakeholder input before testing begins)

OUTPUT FORMAT: Structured markdown document suitable for HTML export and stakeholder presentation.
```

---

## Follow-Up Prompts

**To generate Annex / Appendix (peak month simulation):**
```
Add an appendix section: "Peak Month Capacity Simulation."

Include:
- A worked example of peak month load calculation based on [PEAK_MONTH_DESCRIPTION]
- A synthetic dataset specification for simulating that peak
- A step-by-step execution plan for running the peak simulation test
- Expected metrics to capture during the simulation run
- Pass/fail criteria for the simulation
```

**To add a cost estimation section:**
```
Add a section estimating Databricks compute costs for each test scenario.
Use the following unit costs: [DBU_COST_PER_HOUR] per DBU-hour.
Estimate DBU consumption per scenario based on [CLUSTER_TYPE] cluster configuration.
Flag all estimates as approximate — to be refined after first test run.
```

**To sharpen the risk register:**
```
Review the risk register. For each risk, is the mitigation strategy concrete 
and actionable, or is it vague? Rewrite any mitigation that says "monitor" 
or "review" without specifying what to look for and who is responsible.
```

---

## Validation Checklist (before sharing with stakeholders)
- [ ] No real production data volumes claimed as tested facts — all marked as estimates/targets
- [ ] Infrastructure references (cluster types, storage paths) match actual project environment
- [ ] SLA targets are confirmed with the team before inclusion — not assumed
- [ ] Open questions section is complete — don't bury unknowns inside sections
- [ ] Risk register has at least 3 entries with concrete mitigations
- [ ] Document reviewed by at least one other team member before client sharing
- [ ] Any Azure/Databricks pricing figures are clearly labeled as estimates

---

## Example Usage Note
*DOM project example (May 2026): Used to produce the DOM Pipeline Performance Testing Plan (dom_performance_testing_strategy.html) and Annex 1 — Peak Month Capacity Simulation. Plan presented at the May 26 review meeting with client-side stakeholders and adopted as the official testing baseline. Estimated manual effort: 3–5 days. With AI: ~1 day. Issue caught: AI referenced "Azure Defender for Containers" as an active control — not deployed in DOM environment. Removed and replaced with accurate Trivy reference.*

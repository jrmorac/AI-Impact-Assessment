# Meeting Minutes
## Performance Testing Plan – Internal Review

### 1. Meeting Details
- Date: May 26, 2026
- Time: 12:27 PM CST
- Duration: ~1 hour 6 minutes
- Meeting Type: Internal Review (Preliminary)

### 2. Attendees
- Jose Rafael Mora Casal
- Cesar Leonardo Trompetero Roa
- Nelson Allan Araya Alvarado
- Sean Smith
- Steven Yelton

### 3. Meeting Objective
- Review and validate the draft performance testing plan for the DOM project.
- Align internally on scope, assumptions, and strategy before sharing with the client.
- Identify risks, gaps, and next steps for refinement.

### 4. Key Discussion Topics

#### 4.1 Scope of Performance Testing
- Focus on data ingestion and transformation pipelines (Databricks).
- Exclude web application performance, API load testing, and self-service portal testing for now.
- Objective is to measure throughput, execution time, and cost efficiency.

#### 4.2 Baseline Definition
- Proposed baseline: 500 GB dataset or 10 million rows.
- Team identified that file size, row count, number of files, and column structure all significantly affect performance.
- Baseline requires further clarification and characterization.

#### 4.3 Data Realism and Dataset Characterization
- Current datasets are synthetic.
- Need alignment with stakeholders to ensure test data reflects real-world workloads.
- File count, file size, and dataset width must be considered.

#### 4.4 Workload and Volume Understanding
- Historical ingestion estimates indicate approximately 20 TB per month.
- Data is currently too aggregated to derive realistic test scenarios.
- Need workload characterization by client, project, and peak-load scenarios.

#### 4.5 Testing Strategy
- Start with a Minimum Viable Performance Test.
- Execute a representative dataset through a single pipeline.
- Measure execution time, throughput, and infrastructure cost.
- Expand later into scalability and concurrency testing.

#### 4.6 Concurrency Testing
- Initial proposal included 2x, 4x, and 8x concurrent execution scenarios.
- Team agreed concurrency should focus on realistic pipeline scenarios rather than artificial workload simulations.
- Azure scaling capabilities may mitigate many traditional concurrency concerns.

#### 4.7 Tools and Instrumentation
- JMeter and Azure Load Testing were discussed.
- Team agreed these tools are better suited for application load testing than data pipeline performance testing.
- Preferred monitoring tools include Databricks metrics, Spark UI, and Azure monitoring.

#### 4.8 Structured vs Unstructured Data
- Structured data is in scope.
- Unstructured data processing is not currently ready and remains out of scope.

#### 4.9 Scope Control and Expectations Management
- Performance testing is planned for a future project phase.
- Team emphasized avoiding scope creep and ensuring stakeholders understand the distinction between application testing and pipeline testing.

### 5. Decisions Made
- Focus exclusively on pipeline performance.
- Adopt a simplified MVP approach.
- Limit initial testing to structured data and single-pipeline execution.
- Remove unsupported edge cases.
- Avoid relying on web load-testing tools for performance analysis.

### 6. Open Questions and Risks
- What is the exact production data profile?
- What are the expected SLAs and success criteria?
- How will performance versus cost be evaluated?
- What level of concurrency is actually required?
- How will real-world datasets be obtained?

### 7. Action Items
1. Jose Mora to simplify and refine the performance testing plan.
2. Jose Mora and Cesar Trompetero to improve dataset characterization.
3. Team to validate assumptions with stakeholders.
4. Remove unsupported edge cases from the current draft.
5. Define a practical baseline test scenario.

### 8. Next Steps
- Finalize an updated draft.
- Validate assumptions with Mediquant stakeholders.
- Execute an initial baseline performance test.
- Expand testing scope based on results.

### 9. Key Takeaway
The team agreed to approach performance testing as a data-pipeline validation effort focused on realistic datasets, throughput, execution time, and cost, rather than traditional application load testing.

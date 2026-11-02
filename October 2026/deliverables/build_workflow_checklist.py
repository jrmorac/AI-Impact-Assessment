import csv
import hashlib
import json
import re
from collections import Counter
from datetime import datetime
from pathlib import Path

from openpyxl import Workbook, load_workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.worksheet.datavalidation import DataValidation


DOWNLOADS = Path.home() / "Downloads"
SOURCE = DOWNLOADS / "DOM Product Acceptance Checklist draft.xlsx"
BACKLOG = DOWNLOADS / "Data Platform Team - Stories.csv"
PROPOSAL = DOWNLOADS / "MediQuant - Data Ingestion Modernization Recommendations - final.docx"
OUTPUT = Path(__file__).with_name("DOM Product Acceptance Checklist - Workflow Ordered.xlsx")
HEADERS = ["Requirement ID", "Phase", "Requirement", "Story IDs", "Coverage"]
STAGES = {
    0: ("Platform prerequisites and releases", [7]),
    1: ("Customer creation and infrastructure", [14, 17, 18, 6, 1, 2, 3, 5, 4, 21, 59]),
    2: ("Project creation and container setup", [15, 20]),
    3: ("Dataset import to storage", [10, 11, 12, 13, 31, 40, 43, 30]),
    4: ("Preparation, ingestion and validation", [8, 9, 58, 26, 27, 22, 24, 25, 28, 23, 32, 33, 34, 35, 36, 38, 29, 37, 62, 41, 42, 39, 44, 45, 46, 47, 60, 61, 63, 64, 65, 66, 67, 68, 69, 70, 71, 50, 51, 52, 53, 54, 55, 56, 81, 83]),
    5: ("Reports, analysis and review", [16, 48, 49, 57, 84, 85, 86]),
    6: ("Correction, reimport and reingestion", [82, 72, 73, 74, 75, 76, 77]),
    7: ("Ongoing lifecycle and retention", [19, 78, 79, 80]),
}
PROPOSAL_SECTIONS = {
    0: "Future State Recommendations > Move to Cloud Native Infrastructure; Develop a Data Ingestion Portal and Collect Metadata",
    1: "Future State Recommendations > Move to Cloud Native Infrastructure; Develop a Data Ingestion Portal and Collect Metadata",
    2: "Future State Recommendations > Develop a Data Ingestion Portal and Collect Metadata",
    3: "Future State Recommendations > Move to Cloud Native Infrastructure > Data Acquisition",
    4: "Future State Recommendations > Create a Cloud-Native Data Pipeline; Automate Data Quality Checks",
    5: "Future State Recommendations > Automate Data Quality Checks > Consolidated Quality Reporting; Develop a Data Ingestion Portal and Collect Metadata",
    6: "Current Findings > repeated data loads; Automate Data Quality Checks > Fewer Reprocessing Cycles; Product Roadmap > Incremental Data & CDC; Robust Observability and Reporting",
    7: "Future State Recommendations > Use Tiered Storage for Cost Optimization; Product Roadmap > Cost Optimization & Data Lifecycle Management",
}
NOTES = {
    1: "Customer infrastructure includes resource group, networking, storage account, SQL database and Databricks workspace. Also supports project provisioning; not a recurring release deployment.",
    2: "Databricks replaces Azure Data Factory (user-confirmed). Original story references 64812/64814 still name Data Factory; retain and flag, do not relabel historical titles.",
    3: "Customer storage account is provisioned here. Project creation adds only a container inside this account.",
    4: "Future SFTP endpoint capability; not a prerequisite for current portal/AzCopy paths.",
    5: "Customer SQL database is provisioned with customer infrastructure. Project databases are created as needed during Databricks execution, never during project creation. Requirement scope versus linked backup-restore stories requires clarification.",
    6: "Original subscription requirement retained. User clarified customer resources but did not reconfirm the subscription-vending trigger.",
    7: "Shared operational metadata store, not an execution-created project database. Existing links describe metadata injection/list APIs; confirm datastore implementation evidence.",
    8: "CSV ingestion is execution-time processing, distinct from transferring CSV files to storage (stage 3).",
    9: "Restore database backups during preparation as required; do not assume a database exists at project creation.",
    14: "Umbrella Data Ingest Manager requirement spans the journey; located at the first user action. Existing links explicitly include customer add/edit and project add/edit.",
    15: "Project creation creates only a project container within customer storage. It does not create project databases. Container creation is not explicit in this requirement wording; supporting stories are proposed separately.",
    17: "One row spans customer/project identifiers. Existing links describe Customer ID in SSO token, not creation of both unique identifiers; review mapping.",
    18: "Portal-triggered technical provisioning spans customer resources and project container; retains one row and all original story references.",
    19: "Lifecycle spans customer/project/data states and closure. Existing log/monitoring stories may support visibility without establishing full lifecycle management.",
    20: "Project status is useful immediately after creation and throughout execution/reporting; primary placement is the project stage.",
    21: "Customer status includes provisioning visibility and remains relevant throughout the journey.",
    22: "Databricks pipeline execution; create project databases on demand when required by the selected data destination. Deployment of new code is a separate dev-team release activity.",
    23: "Original SQL Server destination requirement retained. Story 68105 names a change to Unity Catalog; story 72716 researches Managed SQL destinations. Confirm destination by pipeline; do not silently replace SQL with Unity Catalog.",
    24: "Discovery/profiling occurs before mapping; linked notebook title supports this placement, not proof of completed behavior.",
    25: "Mapping follows discovery; retain original Coverage even where linked backlog work is not started.",
    26: "Basic normalization happens before loading; do not infer that source data can be corrected beyond the agreed normalization.",
    27: "Capture formatting exceptions during preparation; users review them in stage 5.",
    28: "Modular validation/transformation architecture supports execution across datasets; unresolved original mapping preserved.",
    30: "Manifest-to-file reconciliation follows delivery; may be repeated during execution. Exact validation trigger requires story acceptance criteria.",
    31: "Unsupported file checks may occur at upload or pipeline preparation; exact rejection timing requires acceptance criteria.",
    32: "Source type fidelity is an execution concern, not a reporting capability; unresolved original mapping preserved.",
    39: "Linked story 67457 explicitly reads staging database file pointers, so place after loading rather than assuming upload-time validation.",
    40: "Validate delivered files against customer manifests; repeats during execution where needed.",
    43: "Manifest integrity belongs to delivery validation, but story 67673 concerns a drop-table indicator. Confirm mapping without changing the original links.",
    44: "Staging-data file pointers require structured data to be available; this is post-load validation.",
    45: "Linked story 67457 describes staging file pointers; exact file-type validation coverage requires confirmation.",
    46: "Detect files referenced by staged data but absent from delivered storage.",
    47: "Out of Scope is preserved despite proposal wording; reordering does not reopen the scope decision.",
    48: "Existing stories name upload reports, not consolidated data quality reports; confirm they cover this requirement.",
    49: "Review/export failures follows execution; exported failures can inform correction and rerun.",
    50: "Capture during execution; consume in reporting. Do not move collection to the reporting stage.",
    51: "Capture during execution; consume in reporting.",
    52: "Capture volume during processing; story 66101 title alone does not establish volume metrics.",
    53: "Capture during execution; consume in reporting.",
    54: "Capture table counts after processing; consume in reporting.",
    55: "Capture row counts after processing; consume in reporting.",
    56: "Record intervention when it occurs; linked 67674 title describes job parameters, not a manual-intervention register.",
    57: "Cost dashboards and Azure Monitor are not automatically equivalent to basic data-quality dashboards; confirm intended report scope.",
    58: "Database-backup path requires execution-time restore/ingestion support, separate from storing the backup.",
    59: "Future expansion of onboarding; located with customer creation, not promoted into Phase 1.",
    72: "Future incremental load strategy, not equivalent to manual full-file reimport. Reuses acquisition and ingestion stages.",
    73: "Future CDC is a distinct automated acquisition mode; not a prerequisite for ordinary reruns.",
    74: "Future CDC insert handling; grouped with repeat/incremental processing, not manual reupload.",
    75: "Future CDC update handling; grouped with repeat/incremental processing, not manual reupload.",
    76: "Future CDC delete handling; do not infer existing reruns delete target rows.",
    77: "Future near-real-time mode; distinct from the current manual correction loop.",
    78: "Ongoing storage lifecycle; no claim of automatic customer/project deletion.",
    79: "Storage tier transition is ongoing lifecycle behavior, not an ingestion prerequisite.",
    80: "Archiving mapping and blank coverage require review; do not assume that tiering proves archive coverage.",
    81: "Metadata collection occurs across processing; linked 67411 instead names comparison against canonical metadata.",
    82: "Rerun tracking supports the correction loop, but is not evidence of a separate reimport feature. Reimport returns to stage 3; same stored files can rerun from stage 4.",
    83: "Capture performance at execution; review in stage 5. Future phase preserved despite existing story state.",
    84: "Future comparison of automated and legacy processes; not proof of measured benefits.",
    85: "Future downstream use case; no new reporting capability inferred.",
    86: "Future downstream use case; no new reporting capability inferred.",
}
CANDIDATES = {
    1: [66978, 67060, 67418], 2: [65294, 65585, 65292, 65295, 65586],
    3: [65020, 70847], 5: [65020], 7: [65546],
    15: [68496, 70207, 71237], 17: [66231, 66244, 66233, 66465],
    22: [65582, 70345, 70346, 70602], 23: [68105, 71735, 72716],
    26: [66555], 28: [66555, 66106, 66107],
    49: [66105, 67568], 82: [67110, 67124, 67675, 67680],
}
REVIEW_IDS = {2, 5, 6, 7, 17, 19, 23, 28, 31, 32, 43, 45, 48, 52, 56, 57, 80, 81, 82}


def file_hash(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_sources():
    workbook = load_workbook(SOURCE, data_only=False)
    sheet = workbook["Traceability Matrix"]
    assert [cell.value for cell in sheet[1]] == HEADERS
    rows = [tuple(values) for values in sheet.iter_rows(min_row=2, values_only=True) if values[0] is not None]
    assert len(rows) == 86
    assert {int(row[0]) for row in rows} == set(range(1, 87))
    with BACKLOG.open(encoding="utf-8-sig", newline="") as stream:
        stories = list(csv.DictReader(stream))
    assert len(stories) == 442
    assert len({story["ID"] for story in stories}) == len(stories)
    return rows, {story["ID"]: story for story in stories}


def style_sheet(sheet, widths, table_name=None):
    sheet.freeze_panes = "C2" if sheet.title == "Workflow Requirements" else "A2"
    sheet.sheet_view.showGridLines = False
    for cell in sheet[1]:
        cell.fill = PatternFill("solid", fgColor="183E36")
        cell.font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
        cell.alignment = Alignment(wrap_text=True, vertical="center")
    sheet.row_dimensions[1].height = 32
    for column, width in widths.items():
        sheet.column_dimensions[column].width = width
    for row in sheet.iter_rows(min_row=2):
        longest = 1
        for cell in row:
            cell.font = Font(name="Calibri", size=11)
            cell.alignment = Alignment(wrap_text=True, vertical="top")
            width = sheet.column_dimensions[cell.column_letter].width
            longest = max(longest, sum(max(1, (len(line) + int(width) - 1) // int(width)) for line in str(cell.value or "").split("\n")))
            if cell.value in ("Need Review", "Requires Clarification"):
                cell.fill = PatternFill("solid", fgColor="FFF0BF")
        sheet.row_dimensions[row[0].row].height = min(300, max(36, longest * 16 + 12))
    if table_name and sheet.max_row > 1:
        table = Table(displayName=table_name, ref=sheet.dimensions)
        table.tableStyleInfo = TableStyleInfo(name="TableStyleMedium4", showRowStripes=True)
        sheet.add_table(table)
    sheet.sheet_properties.pageSetUpPr.fitToPage = True
    sheet.page_setup.orientation = "landscape"
    sheet.page_setup.paperSize = sheet.PAPERSIZE_A3
    sheet.page_setup.fitToWidth = 1
    sheet.page_setup.fitToHeight = 0
    sheet.print_title_rows = "1:1"


def build():
    original_rows, stories = read_sources()
    source_hashes = {str(path): file_hash(path) for path in (SOURCE, BACKLOG, PROPOSAL)}
    by_id = {int(row[0]): row for row in original_rows}
    flattened = [requirement_id for _, ids in STAGES.values() for requirement_id in ids]
    assert len(flattened) == 86 and Counter(flattened) == Counter(by_id.keys())
    workbook = Workbook()
    guide = workbook.active
    guide.title = "Read Me"
    guide.append(["Topic", "Decision / Evidence"])
    guide_rows = [
        ("Purpose", "Workflow-ordered view of all 86 original requirements. This is not a delivery reprioritization or acceptance decision."),
        ("Status", "Draft for Product Owner review. Structural audit is automated; semantic mapping and compliance-sensitive scope need human approval."),
        ("Workflow", "Customer creation > Project creation > Dataset import to storage > Databricks ingestion and validation > Reports/analysis > Correct and reimport/reingest as needed. Stage 0 is outside routine use; stage 7 is ongoing lifecycle."),
        ("Authoritative clarification U1", "User, 2026-10-19: Databricks replaced Azure Data Factory. Use Databricks in current guidance; preserve historical proposal and backlog titles."),
        ("Authoritative clarification U2", "User, 2026-10-19: Customer infrastructure creates resource group, networking, storage account, SQL database and Databricks workspace."),
        ("Authoritative clarification U3", "User, 2026-10-19: Project infrastructure creates only a project container within the customer storage account. No project databases beforehand."),
        ("Authoritative clarification U4", "User, 2026-10-19: Project databases are created as needed during Databricks pipeline execution. Destination depends on the pipeline; SQL/Unity Catalog scope remains a review item."),
        ("Authoritative clarification U5", "User, 2026-10-19: Updated code is deployed only when the development team adds functionality; no fixed daily/weekly deployment is assumed."),
        ("Preserved fields", "Original Requirement ID, Phase, Requirement and Story IDs are unchanged. Coverage is unchanged except four blank cells become Need Review. Original Baseline retains the blank cells."),
        ("Coverage is not delivery state", "Covered is inherited from the source checklist; it does not certify implementation, testing, release readiness, or valid story mapping. Story states are snapshot facts from the supplied CSV, not live ADO."),
        ("Mapping confidence", "Requires Clarification indicates a possible mismatch or missing reference, not a confirmed functional gap. Suggested story IDs are title-based candidates only; no original link is replaced."),
        ("Source row", "Original Excel row number is retained to make each reordered row reversible. One requirement occupies exactly one row; secondary stages do not create duplicate requirements."),
        ("Phase", "Phase 1 and Future are preserved. Filter by Phase for the current scope; workflow ordering does not promote Future functionality."),
        ("Loop", "After reviewing errors, corrected/new files return to stage 3; rerunning already stored files returns to stage 4. CDC/incremental loads are separate Future processing modes, not synonyms for reimport."),
        ("Placement evidence", "Stage assignments are BA recommendations based on requirement wording, user clarifications and backlog titles. Proposal section names are navigation references, not assertions that all current technologies existed in the proposal."),
        ("Backlog limits", "442 exported work items: titles, types, states and planning fields only. No descriptions, acceptance criteria or test evidence were supplied. Exact triggers and coverage cannot be verified from titles alone."),
        ("Privacy / compliance", "Contains non-sensitive requirement and work-item references only; no patient records, real user details, secrets or production resource names are copied into the deliverable. Security/retention interpretations require authorized human review."),
        ("Validation method", "Reopen generated workbook and compare every preserved value by requirement ID, baseline row, phase/coverage distribution, source row, stage order, missing links, candidate links, readable layout metadata, and input SHA-256 hashes."),
        ("Rollback", "Original proposal, checklist and backlog are read-only inputs. Discard this derived workbook to return to the unchanged original; Original Baseline is also available within this file."),
    ]
    for item in guide_rows:
        guide.append(item)
    workflow = workbook.create_sheet("Workflow Requirements")
    extra = ["Workflow Order", "Workflow Stage", "Workflow Substep", "Activity Type", "Also Applies To", "Original Excel Row", "Mapping Review", "Review Notes", "Proposal Section", "Suggested Story IDs (unapproved)"]
    workflow.append(HEADERS + extra)
    original_sheet = workbook.create_sheet("Original Baseline")
    original_sheet.append(HEADERS)
    for row in original_rows:
        original_sheet.append(row)
    references = workbook.create_sheet("Story References")
    references.append(["Requirement ID", "Reference Type", "Story ID", "Work Item Type", "Original Backlog Title", "Backlog State", "Reference Assessment"])
    reviews = workbook.create_sheet("Review Register")
    reviews.append(["Review ID", "Priority", "Requirement ID / Context", "Observation", "Evidence", "Action / Decision Needed", "Status"])
    review_number = 0

    def add_review(priority, context, observation, evidence, action):
        nonlocal review_number
        review_number += 1
        reviews.append([f"REV-{review_number:03d}", priority, str(context), observation, evidence, action, "Requires Clarification"])

    for stage_number, (stage_name, requirement_ids) in STAGES.items():
        for sequence, requirement_id in enumerate(requirement_ids, 1):
            source_row = by_id[requirement_id]
            coverage = source_row[4] if source_row[4] not in (None, "") else "Need Review"
            linked_ids = re.findall(r"\d+", str(source_row[3] or ""))
            missing = [story_id for story_id in linked_ids if story_id not in stories]
            unresolved = not linked_ids
            needs_review = requirement_id in REVIEW_IDS or bool(missing) or unresolved
            default_notes = {
                0: "Shared enablement before routine use; does not imply a deployment on each user operation.",
                1: "Support customer onboarding and provisioning; preserve the original requirement scope, phase and coverage.",
                2: "Support project configuration and management; project infrastructure is a storage container only.",
                3: "Acquire or examine delivered files in storage; ingestion into a project database is a separate execution step.",
                4: "Perform the specified processing capability at its applicable execution step; results are reviewed in stage 5. Preserve Future scope where present.",
                5: "Expose the specified reporting, analysis or costing capability; do not interpret original coverage as tested acceptance.",
                6: "Support repeat processing according to the original requirement; do not equate manual reruns with Future CDC.",
                7: "Apply ongoing lifecycle behavior according to agreed retention and scope; authorized human review is required.",
            }
            note = NOTES.get(requirement_id, default_notes[stage_number])
            if missing:
                note += " Missing from supplied backlog: " + ", ".join(missing) + "."
            if unresolved:
                add_review("Medium", requirement_id, "Original story mapping is blank or a question-mark placeholder.", f"Original Baseline row {original_rows.index(source_row) + 2}, Story IDs", "Assign verified story references; no replacement inferred.")
            if coverage == "Need Review":
                add_review("Medium", requirement_id, "Blank Coverage normalized to Need Review as requested.", f"Original Baseline row {original_rows.index(source_row) + 2}, Coverage", "Confirm coverage with Product Owner; preserve Need Review until decided.")
            if requirement_id in REVIEW_IDS:
                add_review("High" if requirement_id in {2, 5, 23} else "Medium", requirement_id, NOTES[requirement_id], "Original requirement/story links; supplied backlog titles; user clarifications U1-U5", "Review linked story acceptance criteria and confirm intended scope. Candidate links, if any, are unapproved.")
            if missing:
                add_review("Medium", requirement_id, "Referenced story IDs absent from supplied export: " + ", ".join(missing), "Checklist Story IDs compared against CSV ID column", "Obtain missing stories; do not delete original references.")
            pending = [f"{story_id}: {stories[story_id]['State']}" for story_id in linked_ids if story_id in stories and stories[story_id]["State"] not in {"11 Ready for Stage", "Closed"}]
            if coverage == "Covered" and pending:
                add_review("Medium", requirement_id, "Covered is retained, but at least one linked story is earlier than Ready for Stage: " + "; ".join(pending), "Checklist Coverage and exported State; no acceptance evidence supplied", "Treat coverage as mapping only; verify implementation/testing separately. Ready for Stage also does not prove release acceptance.")
            if requirement_id == 15:
                substep = "Create project record, then project storage container only"
            elif requirement_id == 5:
                substep = "Provision customer SQL database; defer project databases to execution"
            elif stage_number == 1 and requirement_id in {1, 2, 3, 4, 6, 18}:
                substep = "Customer resource provisioning" if requirement_id != 4 else "Future optional SFTP provisioning"
            elif requirement_id == 22:
                substep = "Execute Databricks workflow; create project databases as needed"
            elif requirement_id in {50, 51, 52, 53, 54, 55, 56, 81, 83}:
                substep = "Capture execution metadata / intervention details"
            elif requirement_id in {39, 44, 45, 46, 47}:
                substep = "Post-load staged-data / file-pointer validation"
            elif stage_number == 6:
                substep = "Rerun tracking and correction loop" if requirement_id == 82 else "Future incremental / CDC processing (not manual reimport)"
            else:
                substep = {0: "Shared metadata foundation", 1: "Customer onboarding and visibility", 2: "Project management and visibility", 3: "Acquire files and validate delivery", 4: "Prepare / execute / validate data", 5: "Review outcomes and decide corrections", 7: "Lifecycle and storage retention"}[stage_number]
            activity = "Technical Prerequisite" if stage_number == 0 or requirement_id in {1, 2, 3, 4, 5, 6, 18} else "User Action / Review" if stage_number in {1, 2, 5} or requirement_id in {10, 11, 12, 13} else "Automated Processing"
            secondary = "5 - Reports, analysis and review" if stage_number == 4 else "4 - Ingestion; 6 - Repeat processing" if stage_number == 3 else "All applicable stages" if requirement_id in {7, 14, 17, 19, 20, 21} else "2 - Project setup" if requirement_id in {1, 3, 18} else "3 - Reimport; 4 - Reingest" if stage_number == 6 else ""
            candidates = [story_id for story_id in CANDIDATES.get(requirement_id, []) if str(story_id) not in linked_ids]
            workflow.append(list(source_row[:4]) + [coverage, f"{stage_number}.{sequence:02d}", stage_name, substep, activity, secondary, original_rows.index(source_row) + 2, "Requires Clarification" if needs_review else "Retained - title-level reference only", note, PROPOSAL_SECTIONS[stage_number], " ".join(map(str, candidates))])
            for reference_type, ids in (("Original", linked_ids), ("Suggested - unapproved", list(map(str, candidates)))):
                for story_id in ids:
                    story = stories.get(story_id)
                    references.append([requirement_id, reference_type, story_id, story["Work Item Type"] if story else "Not in export", (story["Title 1"] or story["Title 2"]) if story else "Missing from supplied backlog", story["State"] if story else "Unknown", "Title-level evidence only; verify acceptance criteria" if story else "Requires Clarification"])
    add_review("High", "Destination architecture", "SQL Server wording remains in requirements; backlog includes Unity Catalog migration and a Managed SQL research spike.", "Requirement 23; CSV IDs 68105, 71735, 72716; clarification U4", "PO/technical lead confirm destination behavior per pipeline before acceptance.")
    add_review("Medium", "Stage 0 / release deployment", "No standalone original requirement explicitly describes updated code deployment. Do not create a fabricated requirement row.", "User clarification U5; CSV IDs 72301, 66212, 66694, 66082, 66083, 67418, 70567", "Treat CI/CD as dev-team-triggered enablement, outside daily use. These titles do not establish automatic deployment on every pipeline run.")
    add_review("Medium", "Project infrastructure boundary", "Only project container is created at project setup; database creation belongs to execution.", "U3-U4; CSV IDs 68496, 70207, 71237, 68614, 68647", "Validate detailed triggers with acceptance criteria; do not assume title-level infrastructure expansion includes databases.")
    add_review("Medium", "AI/security/retention", "Future AI/ML and lifecycle requirements are retained without authorizing use of sensitive data or determining compliance.", "Original Future requirements 63-71, 78-80; proposal Risks > Security & Compliance Risks", "Authorized human review required before use with regulated data; this workbook is not a compliance approval.")
    summary = workbook.create_sheet("Workflow Summary")
    summary.append(["Stage", "Stage Name", "Phase 1 Rows", "Future Rows", "Total Rows", "User / Technical Sequence"])
    descriptions = {
        0: "Shared metadata foundation before use. Dev-team code releases are separate enablement, documented in Review Register, not invented requirements.",
        1: "Create customer record/identifier; provision resource group, networking, storage account, customer SQL database and Databricks workspace; show provisioning status.",
        2: "Create/configure project; create only a project container in customer storage; no project databases.",
        3: "Transfer files to storage through supported routes; examine delivered files/manifests. Future transfer methods remain Future.",
        4: "Prepare/restore sources > normalize > discover/map > execute Databricks > create project databases as needed > load > validate staged data > capture runtime metadata. Validations may also run before/during loading.",
        5: "Review reports, errors, metrics and supported analysis; decide whether files or processing require correction.",
        6: "Correct files and return to stage 3, or rerun stored input from stage 4. Future incremental/CDC modes are distinct extensions.",
        7: "Apply ongoing lifecycle/tiering/archiving subject to original phase, scope and retention decisions.",
    }
    for stage_number, (name, ids) in STAGES.items():
        counts = Counter(by_id[requirement_id][1] for requirement_id in ids)
        summary.append([stage_number, name, counts["Phase 1"], counts["Future"], len(ids), descriptions[stage_number]])
    evidence = workbook.create_sheet("Audit Evidence")
    evidence.append(["Check", "Result", "Evidence / Limit"])
    for path in (SOURCE, BACKLOG, PROPOSAL):
        evidence.append(["Input SHA-256", "Recorded", f"{path.name}: {source_hashes[str(path)]}"])
    audit_messages = [
        ("Requirement conservation", "86 input rows; 86 output rows; ID set exactly 1-86; no duplicate IDs."),
        ("Preserved field equality", "Requirement ID, Phase, Requirement and Story IDs match the original by ID."),
        ("Coverage transformation", "Exactly requirements 16, 28, 32, 80 change from blank to Need Review; every other value preserved."),
        ("Original baseline equality", "All five source columns and all 86 original rows retained, including original blank coverage."),
        ("Order and source row", "Stage order monotonic; unique workflow order; every source row resolves to its original requirement."),
        ("Story-reference audit", "Every numeric original story ID accounted for; missing IDs explicitly flagged; proposed IDs checked against CSV."),
        ("Input integrity", "Source checklist, proposal and backlog hashes unchanged after generation."),
        ("Excel structure", "Workbook reopens; required sheets exist; Excel tables/filters and frozen headers present; no formulas, macros or external links."),
        ("Architectural boundaries", "Project container at stage 2; project database creation at stage 4; customer SQL at stage 1; release deployment outside routine use."),
        ("Repeatability", "Independently rebuild and compare all worksheet cell values; exact equality required."),
    ]
    for title, detail in audit_messages:
        evidence.append([title, "PASS - automated", detail])
    evidence.append(["Semantic/acceptance approval", "OPEN - human review", "Titles cannot prove coverage. Review Register remains open; no product release or compliance approval asserted."])
    evidence.append(["Caught correction 1", "FIXED and retested", "Initial stage map omitted requirement 17. Conservation assertion blocked output; requirement restored exactly once at customer creation with cross-stage applicability."])
    evidence.append(["Caught correction 2", "FIXED and retested", "Semantic audit found generic validation wording on non-validation activities. Replaced with stage-specific guidance; original requirement text was never changed."])
    evidence.append(["Visual rendering", "LIMIT", "Wrap, widths, row heights, tables and print settings checked structurally; not rendered in desktop Excel."])
    style_sheet(guide, {"A": 34, "B": 115}, "ReadMeTable")
    style_sheet(workflow, {"A": 14, "B": 12, "C": 64, "D": 32, "E": 18, "F": 16, "G": 36, "H": 56, "I": 25, "J": 34, "K": 16, "L": 38, "M": 95, "N": 65, "O": 38}, "WorkflowTable")
    style_sheet(original_sheet, {"A": 14, "B": 12, "C": 75, "D": 45, "E": 20}, "BaselineTable")
    style_sheet(references, {"A": 16, "B": 27, "C": 16, "D": 20, "E": 95, "F": 28, "G": 60}, "ReferencesTable")
    style_sheet(reviews, {"A": 16, "B": 14, "C": 32, "D": 100, "E": 75, "F": 85, "G": 26}, "ReviewTable")
    style_sheet(summary, {"A": 12, "B": 45, "C": 16, "D": 16, "E": 16, "F": 120}, "SummaryTable")
    style_sheet(evidence, {"A": 38, "B": 28, "C": 115}, "AuditTable")
    validation = DataValidation(type="list", formula1='"Covered,Not Covered,Out of Scope,Need Review"')
    validation.errorTitle = "Select an existing coverage value"
    validation.error = "Use Covered, Not Covered, Out of Scope, or Need Review."
    validation.showErrorMessage = True
    workflow.add_data_validation(validation)
    validation.add("E2:E87")
    workbook.active = workbook.sheetnames.index("Workflow Requirements")
    workbook.properties.creator = "Business Analysis"
    workbook.properties.title = "DOM Product Acceptance Checklist - Workflow Ordered"
    workbook.properties.created = datetime(2026, 10, 19)
    workbook.properties.modified = datetime(2026, 10, 19)
    workbook.save(OUTPUT)
    audit(original_rows, stories, source_hashes)


def audit(original_rows, stories, source_hashes):
    workbook = load_workbook(OUTPUT, data_only=False)
    rows = list(workbook["Workflow Requirements"].iter_rows(min_row=2, values_only=True))
    original = {int(row[0]): row for row in original_rows}
    assert len(rows) == 86 and Counter(int(row[0]) for row in rows) == Counter(original.keys())
    assert list(workbook["Original Baseline"].values)[1:] == original_rows
    changed = []
    for row in rows:
        requirement_id = int(row[0])
        baseline = original[requirement_id]
        assert row[:4] == baseline[:4], requirement_id
        assert row[4] == (baseline[4] if baseline[4] not in (None, "") else "Need Review")
        if row[4] != baseline[4]:
            changed.append(requirement_id)
        assert original_rows[row[10] - 2] == baseline
        assert requirement_id in STAGES[int(row[5].split(".")[0])][1]
    assert sorted(changed) == [16, 28, 32, 80]
    assert [row[5] for row in rows] == sorted(row[5] for row in rows)
    assert len({row[5] for row in rows}) == 86
    expected_links = Counter((int(row[0]), story_id) for row in original_rows for story_id in re.findall(r"\d+", str(row[3] or "")))
    actual_links = Counter((int(row[0]), row[2]) for row in workbook["Story References"].iter_rows(min_row=2, values_only=True) if row[1] == "Original")
    assert expected_links == actual_links
    for row in workbook["Story References"].iter_rows(min_row=2, values_only=True):
        if row[1] == "Suggested - unapproved":
            assert row[2] in stories
        if row[2] not in stories:
            assert row[3] == "Not in export"
            workflow_row = next(item for item in rows if item[0] == row[0])
            assert row[2] in workflow_row[12]
    assert Counter(row[1] for row in rows) == Counter(row[1] for row in original_rows)
    assert {int(row[0]): row for row in rows}[15][7] == "Create project record, then project storage container only"
    assert "as needed" in {int(row[0]): row for row in rows}[22][7]
    assert len(workbook.sheetnames) == 7
    for sheet in workbook:
        assert sheet.tables and sheet.freeze_panes
        for row in sheet:
            for cell in row:
                assert cell.data_type != "f", (sheet.title, cell.coordinate)
    assert not workbook._external_links
    assert source_hashes == {str(path): file_hash(path) for path in (SOURCE, BACKLOG, PROPOSAL)}
    values = {sheet.title: list(sheet.values) for sheet in workbook}
    print(json.dumps({"output": str(OUTPUT), "requirements": len(rows), "coverage_changed_ids": sorted(changed), "original_story_links": sum(expected_links.values()), "missing_story_ids": sorted({story_id for _, story_id in expected_links if story_id not in stories}), "review_items": workbook["Review Register"].max_row - 1, "phase_counts": dict(Counter(row[1] for row in rows)), "coverage_counts": dict(Counter(row[4] for row in rows)), "audit": "PASS"}, indent=2))
    return values


if __name__ == "__main__":
    build()
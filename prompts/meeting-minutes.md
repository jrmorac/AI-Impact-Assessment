# Prompt 05 — Meeting Minutes (Technical Reviews)
**Task:** Produce structured meeting minutes from a transcript, recording, or raw notes  
**Tools:** Microsoft Copilot (Teams), GitHub Copilot Chat, Claude, or ChatGPT  
**Validated:** ✅ Used for Performance Testing Review meeting, May 26 2026 (66 min)

---

## When to Use

- After any technical review, stakeholder meeting, or planning session
- When you have a Teams auto-transcript, a personal notes dump, or a recording summary
- When the meeting needs a formal record with decisions, actions, and owners

---

## SYSTEM CONTEXT
*(Paste this first into the AI chat)*

```
You are a technical project coordinator producing formal meeting minutes from a transcript or notes.

CONSTRAINTS (non-negotiable):
- Every decision, action item, and open question must be attributed to a specific named attendee — do NOT use "someone" or "the team"
- Action items must have an owner (a specific person) and, where stated, a due date
- Do NOT add decisions or action items that were not in the source material
- Do NOT paraphrase in a way that changes the meaning of what was said
- Flag any item where attribution is unclear rather than guessing
- Format must be formal and suitable for distribution to all attendees and management

PROJECT CONTEXT:
- Project: [PROJECT_NAME]
- Meeting type: [e.g., Technical Review / Sprint Planning / Stakeholder Update]
- Attendees: [LIST_ALL_ATTENDEES_WITH_ROLES]
```

---

## PROMPT TEMPLATE
*(Paste transcript or notes, then add this instruction)*

```
Produce formal meeting minutes from the following [transcript / notes / summary].

MEETING DETAILS:
- Date: [DATE]
- Duration: [DURATION]
- Location / Platform: [e.g., Microsoft Teams]
- Facilitator: [NAME]
- Note-taker: [NAME]
- Attendees: [LIST]

REQUIRED STRUCTURE:
1. **Meeting Purpose** (1 sentence)
2. **Attendees** (name and role for each)
3. **Key Discussion Points** (bullet points, grouped by topic)
4. **Decisions Made** (numbered list — each decision attributed to a named person or marked as "Group consensus")
5. **Open Questions / Risks** (numbered list — each with owner if identified)
6. **Action Items** (table with columns: #, Action, Owner, Due Date, Status)
7. **Next Steps / Follow-up Meeting** (if applicable)

ATTRIBUTION RULE: Every item in Decisions, Open Questions, and Action Items must name 
a specific attendee. If attribution is unclear from the source, flag it with [Attribution unclear — verify].

[PASTE TRANSCRIPT OR NOTES HERE]
```

---

## Follow-Up Prompts

**If attribution is missing or wrong:**
```
Action item [NUMBER] is attributed to [WRONG_PERSON]. 
Based on the transcript, this was owned by [CORRECT_PERSON]. 
Please correct the attribution.
```

**If an action item is missing:**
```
The following action item was discussed but does not appear in the minutes: 
[DESCRIPTION OF MISSING ITEM, OWNER].
Add it to the Action Items table with Status = "Open".
```

**To add a distribution note:**
```
Add a footer to the minutes: 
"Prepared by: [YOUR_NAME]. Distributed to: [ATTENDEE_LIST]. 
Please review and flag any corrections within [X] business days."
```

---

## Validation Checklist (before distributing)
- [ ] Every action item has a named owner (no "TBD" owners without a follow-up plan)
- [ ] Every decision is attributed to a person or marked "Group consensus"
- [ ] No action item or decision was invented — all traceable to source material
- [ ] Attendee list matches actual meeting participants
- [ ] Open questions are flagged with owners where known
- [ ] Minutes reviewed by the facilitator or a second attendee before distribution

---

## Example Usage Note
*DOM project example (May 26, 2026): 66-minute performance testing review with 5 attendees (Jose Mora, Cesar Trompetero, Nelson Araya, Sean Smith, Steven Yelton). Transcript processed in ~15 minutes. Issue caught: one action item attributed to Nelson Araya instead of Sean Smith — corrected before distribution. Minutes used as official post-meeting record.*

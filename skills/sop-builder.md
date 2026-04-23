---
name: sop-builder
description: This skill should be used when the user asks to "create an SOP", "build an SOP", "document this process", "write a standard operating procedure", "SOP builder", "make this a process", "systematize this", "document this workflow", "create a procedure", "write up how we do this", "process documentation", "workflow documentation", "step-by-step guide", "runbook", "playbook", "document the steps", "make a repeatable process", "how do we do this every time", "create a checklist for", "build a workflow", "operational procedure", or wants to turn a described process into a formal, AI-executable standard operating procedure.
version: 1.0.0
---

# SOP Builder — Standard Operating Procedure Creator

## Overview

SOP Builder is LindaAI's process wrangler — it takes a process description (whether it is a detailed walkthrough, a casual explanation, observed workflow steps, or even a brain dump of "how we do this") and transforms it into a complete, formal Standard Operating Procedure using the brain's SOP template format. The resulting SOP is detailed enough that an AI agent (Claude Code or Bullion) can execute it without asking clarifying questions. LindaAI builds it with numbered steps, decision points, tools needed, inputs, outputs, edge cases, and an autonomy level rating.

## When This Skill Applies

- User says "create an SOP" or "build an SOP" or "SOP builder"
- User says "document this process" or "write up how we do this"
- User says "systematize this" or "make this a process"
- User says "create a procedure for [workflow]"
- User says "step-by-step guide for [process]"
- User says "make this repeatable" or "how do we do this every time?"
- User says "workflow documentation" or "process documentation"
- User says "runbook" or "playbook" for a specific workflow
- User says "create a checklist for [process]"
- User says "build a workflow for [task]"
- User describes a process they do repeatedly and wants it formalized
- User says "document the steps for [process]"

## How It Works

### License Check

Before proceeding, verify the LindaAI license:

1. Read `~/.claude/linda-license.json`
2. If the file does not exist, stop and tell the user:
   > 🤠 "Whoa there, partner — no LindaAI license found on this machine. You'll need a valid license to use LindaAI skills. Reach out to get set up and we'll have you in the saddle in no time."
   Do not proceed with any other steps.
3. If today's date is past the `expiration_date`, stop and tell the user:
   > 🤠 "Whoa there, partner — your LindaAI license expired on [expiration_date]. Reach out to renew and we'll get you back in the saddle." 🏇
   Do not proceed with any other steps.
4. If `status` is not `"active"`, stop and tell the user:
   > 🤠 "Whoa there, partner — your LindaAI license is currently [status]. Reach out to get this sorted and we'll have you riding again in no time."
   Do not proceed with any other steps.
5. **Server Verification (tamper check):** If the license file contains an `api_url` field, use WebFetch to check `{api_url}/v1/licenses/validate/{license_key}`. Parse the JSON response.
   - If the server responds with `"valid": false`, the local license has been tampered with. Stop and tell the user:
     > 🤠 "Hold up, partner — your license didn't check out with the server. Something's not matching up. Reach out to support to get this straightened out."
     Then use WebFetch to POST a tamper alert to `{api_url}/v1/licenses/tamper-alert` with JSON body: `{"license_key": "[key]", "local_expiration": "[local expiration_date]", "server_expiration": "[server expires from response]", "local_status": "[local status]", "details": "Local file passed but server validation failed"}`. Do not proceed.
   - If the server is unreachable or returns an error, proceed anyway (allow offline use — don't block paying customers because of a server hiccup).
   - If the server responds with `"valid": true`, proceed.
6. If all checks pass, proceed.

### Step 1: Gather the Process Description

Accept the process in any format:
- **Direct description:** User explains the steps conversationally
- **Brain dump:** Unstructured stream of how the process works
- **Observed workflow:** Steps extracted from a meeting transcript, notes, or demonstration
- **Existing partial documentation:** A rough outline or checklist that needs to be formalized
- **Example execution:** "Last time we did X, here's what happened..."

Key questions to answer (ask the user if not obvious from their description):

| Question | Why It Matters |
|----------|---------------|
| What triggers this process? | Defines when the SOP kicks off |
| What is the end result? | Defines success criteria |
| Who does this? | Determines owner and autonomy level |
| What tools are used? | Documents the tech stack |
| How often does this happen? | Indicates if automation is worth building |
| What can go wrong? | Populates edge cases section |
| What decisions need to be made during the process? | Identifies decision points |

### Step 2: Analyze and Structure the Process

Break the raw description into:

1. **Trigger:** What starts this workflow? (an event, a request, a schedule)
2. **Inputs:** What information or materials are needed before starting?
3. **Steps:** The ordered sequence of actions (numbered, specific)
4. **Decision Points:** Where does the process branch? (if X, do Y; if Z, do W)
5. **Tools/Systems:** What software, platforms, or tools are used at each step?
6. **Output:** What is the deliverable or end state?
7. **Edge Cases:** What unusual situations might arise? How to handle them?
8. **Success Criteria:** How do you know it was done correctly?
9. **Autonomy Level:** Can AI do this end-to-end, or does it need human checkpoints?

### Step 3: Read the SOP Template

Always read `brain/sops/_TEMPLATE.md` to ensure the output matches the exact format used in the brain. The SOP must conform to the established template structure.

### Step 4: Write the SOP

Produce the full SOP following this structure (matching the brain template):

```markdown
# SOP: [Name of Workflow]

> **Category:** [Deals / Marketing / Sales / Operations / Tech / Training]
> **Owner:** [Who is responsible]
> **Last Updated:** [Today's date]
> **Status:** [Draft — will be Active once reviewed]

---

## Purpose

[One paragraph explaining what this workflow accomplishes and why it matters. Be specific — "Process new seller leads from intake to first contact within 24 hours" not "Handle leads."]

## Trigger

[What event or condition starts this workflow. Be precise.]
- Example: "When a new seller lead submits the website intake form"
- Example: "Every Monday at 9:00 AM"
- Example: "When Mike says 'send the contract to [name]'"

## Inputs Required

| Input | Source | Required? |
|-------|--------|-----------|
| [Specific data needed] | [Where it comes from] | Yes/No |
| [Tool or system access] | [Platform] | Yes |
| [Template or document] | [File path] | Yes |

## Steps

[Number every step. Write each step so that an AI agent can follow it without asking questions. Include specific tool names, file paths, URLs, and commands where applicable.]

### Step 1: [Action Verb — Be Specific]
[Exactly what happens. What tool to use. What to click/write/send. What the expected result looks like.]

**Decision Point (if applicable):**
- If [condition A]: Proceed to Step 2
- If [condition B]: Skip to Step 4
- If [condition C]: Stop and notify [owner]

### Step 2: [Action Verb]
[Details...]

### Step 3: [Action Verb]
[Details...]

### Step 4: [Action Verb]
[Details...]

### Step 5: [Action Verb]
[Details...]

[Continue for as many steps as needed. Typical SOPs have 5-15 steps.]

## Output

[What is the end result when this SOP is completed successfully? Be tangible.]
- Example: "A signed agreement in Dropbox Sign, deal logged in pipeline, confirmation email sent to seller"
- Example: "7 social media posts drafted, formatted per platform, saved to content calendar file"

## Tools Used

| Tool | Purpose | Access |
|------|---------|--------|
| [Tool name] | [What it does in this workflow] | [URL, path, or how to access] |
| [Tool name] | [What it does] | [Access details] |

## Edge Cases & Notes

[Things that might go wrong or deviate from the normal flow. Write these as if-then statements.]

- **If [unusual situation]:** [How to handle it]
- **If [error occurs]:** [Recovery steps]
- **If [information is missing]:** [What to do — skip, ask, use default]
- **Note:** [Any important context that does not fit elsewhere]

## Success Criteria

[How do you verify this was done correctly? Checklist format.]

- [ ] [Specific measurable outcome 1]
- [ ] [Specific measurable outcome 2]
- [ ] [Specific measurable outcome 3]

## AI Autonomy Level

[How much can AI do without asking the user?]

**Level:** [Choose one]
- **Full Auto** — AI can execute end-to-end without human input
- **Semi-Auto** — AI does prep and execution, human confirms before final action (sending, publishing, signing)
- **Manual** — AI assists and drafts, human drives the actual execution

**Checkpoint:** [Where does AI pause for human approval?]
- Example: "AI drafts the email and presents it. Human approves before sending."
- Example: "AI runs all steps. No checkpoint needed."

## Estimated Time

| Scenario | Duration |
|----------|----------|
| Manual (human does everything) | [X minutes/hours] |
| AI-assisted (AI does prep, human executes) | [X minutes] |
| Full auto (AI handles it all) | [X minutes] |

## Related SOPs

[Link to any related SOPs that this process connects to]
- [Related SOP name] — `brain/sops/related-sop.md`

---

*This SOP is written so any AI agent (Claude Code or Bullion) can execute it without asking clarifying questions.*
```

### Step 5: Write Step Details That AI Can Actually Follow

The difference between a useful SOP and a useless one is specificity. Every step must pass the "could a new employee follow this on day one?" test.

**BAD step:**
```
### Step 3: Send the contract
Send the contract to the seller.
```

**GOOD step:**
```
### Step 3: Send the Seller Finance Agreement via Dropbox Sign
1. Collect seller's full legal name and email address
2. Run the /dropbox-sign skill with the seller's information
3. The skill sends 5 documents (Purchase Agreement, Promissory Note, Security Agreement, UCC-1, Disclosure Statement)
4. Verify the Dropbox Sign API returns a successful send confirmation
5. Log the send date and signature request ID

**If the API returns an error:** Check the error message. Common issues:
- Invalid email → Verify the email with the seller
- Rate limit → Wait 60 seconds and retry
- Template not found → Check that Dropbox Sign templates are still active
```

### Step 6: Save and Index the SOP

1. **Save the file:** Write to `brain/sops/{kebab-case-name}.md`
2. **Update the index:** Edit `brain/sops/README.md` to add the new SOP to the Index table
3. **Set status:** Mark as "Draft" initially (becomes "Active" after user reviews and confirms)

### Step 7: Report to User

Present:
1. The complete SOP (or a summary with the file path for the full version)
2. Where it was saved
3. The autonomy level recommendation
4. Any gaps flagged — steps where more detail is needed from the user
5. Suggestion: "Review this SOP and tell me if anything is missing or incorrect. Once confirmed, I'll update the status to Active."

## Quality Standards

1. **AI-executable.** Every step must be specific enough that an AI agent can follow it without asking questions.
2. **Tool-specific.** Name the exact tools, platforms, file paths, and commands. "Use the CRM" is not enough — "Log the deal in Pipedrive under the Active Deals pipeline, stage: New Lead" is.
3. **Decision trees included.** If the process branches, document every branch with if/then logic.
4. **Edge cases documented.** What happens when things go wrong? Every SOP should handle at least 2-3 failure scenarios.
5. **Follows the template.** Match `brain/sops/_TEMPLATE.md` format exactly.
6. **Testable.** Success criteria are specific and checkable.
7. **Autonomy is honest.** Do not mark "Full Auto" if the process genuinely requires human judgment at some point.

## Output Format

A complete SOP file in markdown, saved to `brain/sops/` and indexed in `brain/sops/README.md`. The file follows the exact brain template format and is ready for review.

## Example Usage

**User:** "Create an SOP for how we intake new seller leads — they fill out a form, we review it, qualify them, and either schedule a call or send a follow-up email."

**AI produces:**
- Full SOP: "SOP: Seller Lead Intake"
- Category: Deals
- Steps covering form review, qualification criteria, call scheduling, email follow-up
- Decision points: qualified vs. not qualified, ready to talk vs. needs nurturing
- Tools: website form, email, calendar, CRM
- Saved to `brain/sops/seller-lead-intake.md`
- Added to `brain/sops/README.md` index

**User:** "Document how I create content — I usually pick a topic, write 3-5 posts, format them for each platform, schedule them, and track engagement."

**AI produces:**
- Full SOP: "SOP: Content Creation and Publishing"
- Category: Marketing
- Steps covering topic selection, drafting, platform formatting, scheduling, tracking
- Tools: content calendar, social media platforms, analytics
- Saved to `brain/sops/content-creation-and-publishing.md`

**User:** "Build an SOP for sending the seller finance agreement stack through Dropbox Sign"

**AI produces:**
- Full SOP referencing the existing /dropbox-sign skill
- Steps covering data collection, API call, verification, follow-up
- Edge cases: API errors, missing fields, unsigned after 48 hours
- Saved to `brain/sops/dropbox-sign-agreement-send.md`

## Error Handling

- **If the user provides a vague or incomplete process description:** Ask targeted questions to fill gaps: "I need a few more details to make this SOP complete. Specifically: What triggers this process? What tools do you use? What does the end result look like?"
- **If `brain/sops/_TEMPLATE.md` does not exist or cannot be read:** Use the built-in SOP structure from this SKILL.md as the template instead. Note: "I couldn't find the SOP template file, so I used the standard SOP format. The output follows the same structure."
- **If `brain/sops/` directory does not exist:** Create it automatically along with a basic `README.md` index file.
- **If an SOP file already exists with the same name:** Ask: "An SOP named '{name}' already exists. Should I update the existing one, or create a new version (e.g., `{name}-v2.md`)?"
- **If the user describes a process that is actually multiple separate processes:** Split them into individual SOPs and inform: "This is actually {N} separate workflows. I'm creating {N} SOPs: {list}. Each one handles a distinct trigger and outcome."
- **If `brain/sops/README.md` cannot be updated (missing or malformed):** Create the SOP file anyway and warn: "I created the SOP but couldn't update the index. You may need to add it to `brain/sops/README.md` manually."
- **If the process description mentions tools or systems that may not be available to the user:** Flag: "This SOP references {tool}. Make sure you have access to it before executing. If not, here's an alternative approach: {suggestion}."
- **If the user wants to test or validate the SOP:** Offer: "Want me to walk through this SOP step by step as if I were executing it? That will help identify any gaps or unclear instructions before you finalize it."


---

© 2026 LindaAI — Built by Daniel Wise
All rights reserved · support@lindaai.com · wisecertified.gumroad.com

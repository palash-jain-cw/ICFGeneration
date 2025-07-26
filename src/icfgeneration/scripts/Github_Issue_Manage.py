from github import Github
from dotenv import load_dotenv
from icfgeneration.utils.constants import env_path
import os

load_dotenv(env_path)

# --- Configuration ---
token = os.getenv("GITHUB_REPO_PAT")
repo_name = os.getenv("GITHUB_REPO", "None")

print(token)
print(repo_name)

# --- Authenticate ---
g = Github(token)
repo = g.get_repo(repo_name)

# --- Issue List ---
issue_map = {
    "Protocol Parsing Module": [
        {
            "title": "Integrate PyMuPDF4LLM and Chunk Protocol Document",
            "body": """## Description
Use PyMuPDF4LLM to chunk clinical trial protocol PDFs into semantically meaningful sections.

## Implementation Notes
- Identify chunk strategy (e.g., section-based or sliding window).
- Include metadata: section titles, page numbers, etc.

## Acceptance Criteria
- At least 90% of key content from protocol recoverable in chunks.
- Metadata is stored per chunk.""",
        },
        {
            "title": "Extract Structured Fields from Protocol using LLM",
            "body": """## Description
Extract structured fields (e.g., objectives, risks, procedures) using prompt-driven LLMs.

## Implementation Notes
- Use OpenAI/GPT with templates for each section.
- Ensure extracted data is JSON-serializable and includes traceability.

## Acceptance Criteria
- Extracted output covers >10 fields from protocols across 3+ formats.
- Extraction quality is evaluated with manual validation.""",
        },
    ],
    "Guideline Management Module": [
        {
            "title": "Collect and Structure ICF Regulatory Guidelines",
            "body": """## Description
Collect global ICF regulatory guidance documents (FDA, ICH, EMA, CDSCO) and organize by section.

## Implementation Notes
- Download PDFs or source links for each guideline.
- Segment guidelines by key sections (e.g., risks, voluntariness).

## Acceptance Criteria
- At least 5 official guideline sources structured into section-wise rules.
- Sources stored in persistent and retrievable format.""",
        },
        {
            "title": "Embed Guideline Snippets into Vector Store",
            "body": """## Description
Embed ICF regulatory guideline text into a vector database for retrieval.

## Implementation Notes
- Use sentence-transformers or OpenAI embeddings.
- Store in FAISS or Chroma with metadata (source, section, anchor text).

## Acceptance Criteria
- Queries return top-N relevant guideline sections with metadata.
- Retrieval validated against manually selected sections.""",
        },
    ],
    "ICF Generation Engine": [
        {
            "title": "Design ICF Templating System",
            "body": """## Description
Design a modular ICF template with pluggable content sections.

## Implementation Notes
- Use Jinja2 templates or LLM prompt-templates per section.
- Enable insertion of extracted data + retrieved guidance + instructions.

## Acceptance Criteria
- At least 10 template sections with fillable fields.
- All templates pass basic rendering sanity checks.""",
        },
        {
            "title": "Generate ICF Sections using LLMs + Guidelines + Protocol Info",
            "body": """## Description
Use LLMs to generate each ICF section based on protocol content and guidelines.

## Implementation Notes
- For each section, prompt with: relevant extracted info + guidance snippets + section instructions.
- Apply output guardrails using regex or post-processing.

## Acceptance Criteria
- Generated ICF covers all required sections.
- Quality verified via SME review or checklist.""",
        },
    ],
    "Evaluation and Compliance": [
        {
            "title": "Develop ICF Quality and Compliance Checklist",
            "body": """## Description
Create a checklist based on global regulations to evaluate generated ICFs.

## Implementation Notes
- Derive checklist from ICH E6(R2), FDA 21 CFR 50, EMA guidelines.
- Automate checklist scoring where possible.

## Acceptance Criteria
- Checklist includes 20+ items mapped to specific ICF sections.
- Test ICFs can be evaluated using the checklist.""",
        },
        {
            "title": "Manual Evaluation of ICF Quality on Sample Protocols",
            "body": """## Description
Use the checklist to manually evaluate ICFs generated from 3+ sample protocols.

## Implementation Notes
- Collect reviewer feedback on clarity, completeness, ethics alignment.
- Document gaps and iteration areas.

## Acceptance Criteria
- At least 3 ICFs reviewed.
- Feedback synthesized into improvement plan.""",
        },
    ],
}

# --- Create Parent and Sub-Issues ---
parent_issue_map = {}

for parent_title, sub_issues in issue_map.items():
    parent = repo.create_issue(
        title=parent_title,
        body=f"""## Description
Parent issue for: {parent_title}

## Implementation Notes
Track progress using linked sub-issues.

## Acceptance Criteria
All sub-issues closed and functional module delivered.
""",
    )
    parent_issue_map[parent_title] = parent.number

    for sub in sub_issues:
        sub_issue = repo.create_issue(title=sub["title"], body=sub["body"])
        parent.create_comment(f"- [ ] #{sub_issue.number} {sub['title']}")

# CLAUDE.md — Session Operations
# Marketing Analytics | Instructor Configuration
# DO NOT MODIFY THIS FILE

## Overview
This file configures how Claude Code behaves during every session for this course.
It runs automatically at the start of each session. All logging is mandatory.

---

## Session Initialization

At the start of every session:
1. Create a `/logs` folder in the project directory if it does not already exist
2. Create a `/outputs` folder in the project directory if it does not already exist
3. Begin logging immediately — see Logging Requirements below
4. Read SKILLS.md before executing any student instruction
5. Confirm to the student: "Session started. Logging is active. SKILLS.md loaded."

## Logging Requirements

### 1. Prompt Log — `/logs/prompt_log.md`
Append every student prompt to this file in the following format:

```
---
[TIMESTAMP] STUDENT PROMPT
<exact text of the student's prompt>
```

No prompt is ever omitted. Logging happens before execution.

## Output Structure

All generated code files are saved to `/outputs` with descriptive filenames.
Example: `01_load_data.py`, `02_clean_data.py`, `03_transform_variables.py`

## Integrity Notice

This file is provided by the instructor and must not be modified.
Any modification to this file or the `/logs` folder contents is an academic integrity violation.
Logging gaps or missing files will be treated as incomplete submissions.

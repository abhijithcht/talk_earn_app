---
id: skill_review_prev_task
name: Previous Task Review
version: 1.0.0
description: Analyzes the immediate previous development task for code quality, logic gaps, and optimization opportunities.
tags: [analysis, quality-assurance, antigravity-core]
permissions: [read_file_history, analyze_diffs]
---

# Previous Task Review

## Overview
This skill allows the IDE to contextually look back at the last completed unit of work (commit, file save, or terminal command execution) to provide a "second pair of eyes" review.

## Triggers
* **Manual:** User invokes command `/review last`.
* **Automatic:** Triggered post-commit or upon closing a feature branch (configurable in settings).

## Capabilities

### 1. Contextual Diff Analysis
Compares the state of the codebase before and after the last task.
* **Input:** `git diff HEAD~1` or local history buffer.
* **Action:** Scans for syntax validity, style guide adherence (Google Style), and potential logical race conditions.

### 2. Dependency Check
Ensures no new dependencies were added without corresponding `package.json` / `requirements.txt` updates.

### 3. Cleanup Verification
* Detects leftover `TODO` comments introduced in the last session.
* Flags active `console.log` or print statements intended for debugging.

## Prompts

### standard_review
> "Analyze the changes made in the last task. Summarize the intent, identify 2 potential edge cases, and rate the code cleanliness on a scale of 1-5."

### quick_sanity_check
> "Did I break anything in `src/main` with my last edit? Check for compilation errors and circular dependencies."

## Output Format
Returns a structured JSON object or rendered Markdown card in the Antigravity HUD:

```json
{
  "status": "PASS",
  "issues_found": 0,
  "optimization_tip": "Consider memoizing the selector in line 42."
}
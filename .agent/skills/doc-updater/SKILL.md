---
id: skill_doc_updater
name: Documentation Rot Detector
version: 1.0.0
description: Audits existing documentation against the current codebase. Flags outdated docs where the source code has drifted significantly from the documented behavior.
tags: [maintenance, audit, documentation, quality-control]
permissions: [read_file_tree, read_file_content, write_file]
---

# Documentation Rot Detector

## Overview
This skill performs a "Reverse Dependency Check." It scans your `docs/` folder, parses the `**Source:**` metadata header in each file, and compares the documentation against the live code.

## Triggers
* **Manual:** `/docs audit` (Scans all docs).
* **On File Open:** When opening a `.md` file in `docs/`, it checks the source file in the background.

## Rules Engine

### 1. The Staleness Test
The skill reads the `Source` path defined in the Markdown header.
* **Structure Check:** If the code has new public methods, classes, or changed signatures that are missing from the doc -> **STALE**.
* **Absence Check:** If the source file no longer exists -> **ORPHANED**.

### 2. The "Warning Badge" Protocol
If a document is found to be stale, the skill injects a standard warning block at the top of the Markdown file so readers know to be cautious.

`> [!WARNING] STALE DOCUMENTATION`
`> This document was last updated for a previous version of the code. The source file `lib/core/router.dart` has since changed.`

## Prompts

### `audit_document`
**Input:**
1.  Current Markdown Content.
2.  Current Source Code Content.

**Logic:**
> "Compare the 'Key Components' section of the markdown with the actual classes/methods in the source code. Are there any missing methods or name changes? Answer YES or NO. If YES, list the discrepancies."

### `update_existing_doc`
**Input:** Stale Markdown + Fresh Code.
**Logic:**
1.  Preserve the "Overview" (as it often contains manual context/intent).
2.  **Delegate:** Call `doc-generator`'s `generate_docs` logic for "Key Components" and "Usage" sections to ensure consistent template usage.
3.  Remove the Stale Warning.

---

## Usage Example

**Scenario:** You renamed `ProductService.createProduct` to `ProductService.registerProduct` in the code, but the doc still says `createProduct`.

**User Command:** `/docs audit`

**Antigravity Output:**
* `[WARN] docs/backend/Product_Service.md` is outdated.
    * *Reason:* Method `createProduct` not found in source. Found `registerProduct` instead.

**Action:**
User clicks **"Fix"**, and the skill rewrites the markdown to reflect the name change automatically.
---
id: skill_flutter_very_good_analysis
name: flutter-very-good-analysis
version: 1.0.0
description: Enforces "Very Good Analysis" rules and standard formatting for Flutter projects.
tags: [flutter, linting, quality]
permissions: [read_file, write_file, run_command]
---

# Flutter Very Good Analysis Skill

## Goal
Ensure all Flutter projects adhere to the strict linting rules defined in `analysis_options.yaml`.

## Instructions
1.  **Check Configuration**:
    *   Verify `analysis_options.yaml` exists in the project root.
    *   If missing, copy it from `resources/analysis_options.yaml`.
    *   If present, ensure it includes `package:very_good_analysis/analysis_options.yaml` and sets `page_width: 100`.

2.  **Enforce Rules**:
    *   **Public Docs**: `public_member_api_docs` is explicitly `false`. Do not flag missing documentation for public members.
    *   **Line Length**: `lines_longer_than_80_chars` is `false`. Allow lines up to 100 chars (formatter setting).
    *   **Imports**: Enforce `always_use_package_imports`. Convert relative imports (e.g., `import '../model.dart'`) to package imports (e.g., `import 'package:app/model.dart'`).

3.  **Formatter**:
    *   Always run `dart format . --line-length=100` before finalizing code.

## Resources
*   `resources/analysis_options.yaml`: The master configuration file.

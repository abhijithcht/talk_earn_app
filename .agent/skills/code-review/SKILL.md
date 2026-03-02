---
id: skill_code_review
name: code-review
version: 1.0.0
description: Reviews code changes for bugs, style issues, and best practices. Use when reviewing PRs or checking code quality.
tags: [code_quality, review, best_practices]
permissions: [read_code]
---

# Code Review Skill

When reviewing code, follow these steps:

## Review checklist

1. **Correctness**: Does the code do what it's supposed to?
2. **Edge cases**: Are error conditions handled?
3. **Formatting & Static Analysis**: Delegate to `flutter-very-good-analysis` (Run `dart format` and check lints).
4. **Stack Alignment & Architecture**:
    *   **Flutter**: Delegate to `flutter-auditor` for Riverpod, GoRouter, and Centralization (Strings/Dimens/Assets) checks.
    *   **Laravel 12**: Delegate to `laravel-msc-architecture` to ensure MSC+RPR compliance and Service layer usage.
5. **Performance**: Are there obvious inefficiencies?

## How to provide feedback

- Be specific about what needs to change
- Explain why, not just what
- Suggest alternatives when possible

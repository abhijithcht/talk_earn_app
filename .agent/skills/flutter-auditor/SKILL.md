---
id: skill_flutter_auditor
name: flutter-auditor
version: 1.0.0
description: Reviews Flutter code for best practices, performance issues, and architectural compliance. Triggers when the user asks for a "review", "check my code", or before merging a major feature.
tags: [flutter, quality, audit]
permissions: [read_file, run_command]
---

# Flutter Auditor Skill

## Goal
To ensure code quality, maintainability, and adherence to the project's centralized architecture before code is finalized.

## Instructions
1.  **Static Analysis**:
    * Note: Static analysis and formatting are owned by `flutter-very-good-analysis`.
    * Run `flutter analyze` only if `flutter-very-good-analysis` has not been run.

2.  **Architectural Compliance Check** (Critical):
    * **Strings**: Scan for raw strings in `Text()` widgets. If found, flag them: "Hardcoded string detected. Move to `AppStrings`."
    * **Dimensions**: Scan for raw numbers in `SizedBox`, `Padding`, or `Container`. Flag them: "Magic number detected. Move to `AppDimens`."
    * **Colors**: Scan for `Colors.red` or `Color(0xFF...)`. Flag them: "Raw color used. Use `AppColors` or `Theme.of(context)`."
    * **Imports**: Check import statements. If a relative import goes up two levels (e.g., `../../domain/`), suggest using the Feature Barrel File instead.

3.  **Stack Compliance Check**:
    *   **State Management**: Flag usage of `ChangeNotifierProvider` or `Provider` (from `provider` package). Enforce `Riverpod` (`NotifierProvider`, `AsyncNotifierProvider`).
    *   **Navigation**: Flag usage of `Navigator.push` or `MaterialPageRoute`. Enforce `GoRouter` (`context.go`, `context.pushNamed`).
    *   **Linting**: Check for `// ignore:` comments. Warn if they bypass `very_good_analysis` rules without good reason.

4.  **Performance Check**:
    *   **Const Constructors**: Identify Widgets that can be `const` but aren't.
    *   **Build Method**: Warn if complex logic or heavy computations are present directly inside a `build()` method.
    *   **Lists**: If `ListView` or `Column` is used with children, suggest `ListView.builder` if the list is potentially long/dynamic.

5.  **Refactoring Suggestions**:
    * If a Widget exceeds ~100 lines, suggest extracting it into a smaller, separate Widget file.
    * Identify repetitive code blocks that should be extracted into a helper method or utility class.

## Interaction Style
* Be constructive but strict about the "Centralization" rules.
* Provide code snippets showing the *wrong* way vs the *corrected* way.

## Example Output
"I reviewed `login_screen.dart`.
1. ⚠️ **Hardcoded String**: Line 45 `Text('Welcome Back')` should be `Text(AppStrings.welcomeBack)`.
2. ⚠️ **Magic Number**: Line 50 `SizedBox(height: 20)` should use `AppDimens.spacingMedium`.
3. ✅ **Performance**: Good usage of `const` modifiers."
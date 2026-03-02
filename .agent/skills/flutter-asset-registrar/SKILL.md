---
id: skill_flutter_asset_registrar
name: flutter-asset-registrar
version: 1.0.0
description: Scans the project's assets directory and registers new files in pubspec.yaml. Use this when the user adds new images or fonts.
tags: [flutter, assets, build]
permissions: [read_file, write_file, run_command]
---

# Asset Registration Skill

## Goal
To ensure all files located in `assets/` (and subdirectories) are correctly defined in `pubspec.yaml` without breaking indentation.

## Instructions
1.  **Scan**: List all files in `assets/images/`, `assets/fonts/`, and `assets/icons/`.
2.  **Read**: Parse the current `pubspec.yaml`.
3.  **Verify**: Check if the paths already exist under the `flutter: assets:` section.
4.  **Update**:
    * If `flutter:` or `assets:` keys are missing, create them.
    * Append missing paths using 2-space indentation relative to the `assets:` key.
    * **CRITICAL**: Do not remove existing comments or other dependencies.
5.  **Confirm**:
    * Run `flutter pub get` to ensure the YAML is valid.
    * **Sync**: Automatically append the new asset constant to `lib/core/constants/app_assets.dart` per `resource-extractor` rules to ensure code-level access.

## Constraints
* Do not use wildcards (e.g., `assets/images/`) unless specifically asked; prefer explicit file paths for better build optimization.
* Stop if `pubspec.yaml` is malformed.
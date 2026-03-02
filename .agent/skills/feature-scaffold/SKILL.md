---
id: skill_feature_scaffold
name: feature-scaffold
version: 1.0.0
description: Generates the directory structure and boilerplate files for a new Flutter feature using Clean Architecture. Trigger this when the user says "create a new feature" or "scaffold X".
tags: [flutter, architecture, scaffold]
permissions: [write_file]
---

# Feature Scaffolding Skill

## Goal
Create a standardized folder structure for a new feature to ensure separation of concerns.

## Instructions
1.  **Identify Feature Name**: Extract the feature name from the prompt (e.g., "Login", "Profile"). Snake_case it (e.g., `user_profile`).
2.  **Create Directories**:
    * `lib/features/<name>/data/datasources`
    * `lib/features/<name>/data/repositories`
    * `lib/features/<name>/domain/entities`
    * `lib/features/<name>/domain/repositories`
    * `lib/features/<name>/presentation/providers` (Riverpod only)
    * `lib/features/<name>/presentation/pages`
    * `lib/features/<name>/presentation/widgets`
3.  **Generate Files**:
    *   Create a clean Dart file in each directory.
    *   **Domain Entity**: Must be a pure Dart class with `equatable` or `freezed`.
    *   **Repository Interface**: Abstract class in `domain/repositories`.
    *   **Implementation**: Concrete class in `data/repositories` implementing the domain interface.
    *   **Provider**: Use `Riverpod` (`Notifier` or `AsyncNotifier` preferred over `StateNotifier`).
    *   **Page**: Use `ConsumerWidget` or `HookConsumerWidget`.
4.  **Routing**:
    *   **Delegate**: Call `router-generator`'s `add_route` prompt to register the new page. Do not perform manual registration in `app_router.dart`.
5.  **Barrel Files**: Create a `path.dart` export file for the feature if the project uses them.
6.  **Finalize**: Run `license-header-adder` on all newly generated files.

## Example
User: "Create a chat feature."
Action: Agent creates `lib/features/chat/...` following the structure above.
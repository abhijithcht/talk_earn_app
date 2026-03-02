---
id: skill_laravel_to_flutter_bridge
name: laravel-to-flutter-bridge
version: 1.0.0
description: Translates Laravel Eloquent Resources and Enums into Flutter Dart Models and Providers.
tags: [laravel, flutter, integration]
permissions: [read_code, write_file]
---

# Laravel to Flutter Bridge Skill

This skill automates the creation of Flutter data structures based on Laravel backend definitions, following the "Feature-First" architecture.

## Instructions

1. **Analyze Laravel Input**: Identify the fields in the `toArray()` method of a Laravel Resource or the `$fillable` array in a Model.
2. **Handle Laravel Enums**: If a Laravel field uses a PHP Enum, create a matching `enum` in Dart.
3. **Map Logic**:
    - **Laravel ID** (`bigIncrements`) -> Dart `int`.
    - **Timestamps** -> Dart `DateTime`.
    - **Relationships** -> Map to nested Dart objects or `List<T>`.
    - **API Response Wrapper**: Wrap the result in a `Data` property if using Laravel's default resource wrapping.

## Output Requirements

### A. The Data Model (`lib/features/X/data/models/`)

- Use `@JsonSerializable(fieldRename: FieldRename.snake)` to automatically handle Laravel's `snake_case` to Dart's `camelCase`.
- Include `factory` constructors for JSON conversion.

### B. The Provider (`lib/features/X/presentation/providers/`)

- Create a `Notifier` or `AsyncNotifier` class (Riverpod).
- Use `ref.read` or `ref.watch` to access repositories.
- Handle state using `AsyncValue<T>` for robust loading/error states.
- Avoid `ChangeNotifier` to ensure strict state immutability.

## Style Guidelines

- **Paths**: Use project-relative paths (e.g., `lib/features/auth/...`).
- **Safety**: All fields from Laravel must be nullable (`?`) unless they are strictly required in the database schema.

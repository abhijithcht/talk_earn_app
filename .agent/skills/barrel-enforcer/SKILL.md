---
id: skill_dart_barrel_gen
name: Dart Feature Barrel Generator
version: 1.1.0
description: Auto-generates `imports.dart` barrel files for Flutter features, strictly separating internal feature exports from third-party/platform dependencies.
tags: [flutter, dart, architecture, automation]
permissions: [read_file_structure, write_file]
---

# Dart Feature Barrel Generator

## Overview
This skill scans a specific feature directory (e.g., `lib/features/auth`) and generates a single `imports.dart` file. It enforces a strict "Internal vs. External" import strategy to keep imports clean.

## Rules Engine

### 1. The `imports.dart` Strategy
The generated file acts as the single source of truth for the feature's internal components.
* **DO EXPORT:** All internal files within the feature folder (Models, Views, Controllers, Widgets).
* **DO NOT EXPORT:** Third-party packages (`provider`, `dio`, etc.) or platform-specific libraries (`dart:html`, `dart:io`).

### 2. File Organization
The skill recursively looks through subdirectories (like `widgets/`, `data/`) and adds `export` statements relative to the `imports.dart` file location.

## Prompts

### `generate_barrel`
**Input:** Path to feature directory (e.g., `lib/features/home`)
**Logic:**
1.  List all `.dart` files in directory tree.
2.  Filter out generated files (`.g.dart`, `.freezed.dart`).
3.  Exclude the target barrel file itself (`imports.dart`).
4.  Write strict `export` statements.
5.  Avoid comments in the barrel file.

**Template Output (`lib/features/home/imports.dart`):**
```dart
// Core Feature Exports
export 'home_screen.dart';
export 'home_controller.dart';

// Widgets
export 'widgets/header_card.dart';
export 'widgets/user_avatar.dart';

// Data/Models
export 'data/home_repository.dart';
export 'data/home_model.dart';
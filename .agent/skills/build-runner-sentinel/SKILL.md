---
id: skill_build_runner_sentinel
name: Build Runner Sentinel
version: 2.0.0
description: Intelligent background watcher for code generation tasks.
tags: [flutter, codegen, automation]
permissions: [read_file_events, execute_terminal]
---

# Build Runner Sentinel

## Overview
Eliminates the need to manually run build commands. It detects when a file requiring code generation is modified and triggers a targeted rebuild.

## Triggers
* **Event:** File Saved (`*.dart`)
* **Condition:** File content contains `@Freezed`, `@JsonSerializable`, `@HiveType`, or `@Retrofit`.

## Capabilities

### 1. Smart Execution
Instead of rebuilding the whole app, it runs:
`flutter pub run build_runner build --build-filter="package:myapp/path/to/file.dart"`
This reduces build time from minutes to seconds.

### 2. Conflict Resolver
If a build fails due to conflicting outputs, it automatically retries once with:
`--delete-conflicting-outputs`

### 3. Error Toaster
If the build fails (e.g., syntax error prevents generation), it pipes the error log directly to a unified "Problems" pane rather than cluttering the terminal.
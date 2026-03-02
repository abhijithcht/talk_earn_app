---
id: skill_laravel_log_bridge
name: Cross-Stack Debugger
version: 1.1.0
description: Automatically fetches the relevant Laravel stack trace when the Flutter app receives a 500 error during local development.
tags: [debugging, dx, laravel, flutter]
permissions: [read_file, execute_terminal]
---

# Cross-Stack Debugger

## Triggers
* **Event:** Flutter Debug Console logs `DioException [bad response]: 500`.

## Actions
1.  **Locate Log:** Reads the tail of `../backend/storage/logs/laravel.log`.
2.  **Parse:** Extracts the most recent Exception and Stack Trace.
3.  **Display:** Prints the PHP error directly in the Antigravity "Problems" pane or Chat window.

## Output Example
> **Flutter Error:** 500 Internal Server Error
> **Backend Cause:** `QueryException: Column 'is_active' not found in 'products' table.`
> **File:** `ProductService.php:42`
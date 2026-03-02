---
id: skill_api_contract_sync
name: API Contract Sentinel
version: 1.0.0
description: Ensures Flutter models match Laravel API Resources. Detects missing fields or type mismatches before runtime.
tags: [integration, safety, ci-cd]
permissions: [read_code]
---

# API Contract Sentinel

## Logic
1.  **Map:** Pairs a Laravel Resource (e.g., `UserResource.php`) with a Flutter Model (`user_model.dart`).
2.  **Scan:** extracting keys from the PHP array return and fields from the Dart constructor.
3.  **Compare:**
    * **Missing Keys:** Field exists in Dart but not in PHP (Risk: Null error).
    * **Type Mismatch:** PHP sends `string` ("100"), Dart expects `int` (Risk: Casting error).

## Prompt
> "Check `UserResource` against `UserModel`. Are there any fields in the Flutter model that the backend is not returning?"
---
name: gorouter-manager
description: Manages GoRouter configuration. Triggers when the user adds a new screen/page or asks to "add a route".
---

# GoRouter Manager Skill

## Goal
To automatically register new screens in the global GoRouter configuration and ensure type-safe/constant-based navigation.

## Instructions
1.  **Locate Router**: Find the main router configuration file (usually `lib/core/routes/app_router.dart` or similar).
2.  **Locate Constants**: Find the route constants file (e.g., `lib/core/routes/route_names.dart`).
3.  **Action - When adding a new Screen**:
    * **Step 1**: Add a `static const String` for the new route path and name in your constants file.
    * **Step 2**: Import the new screen using its **feature barrel file**.
    * **Step 3**: Append a new `GoRoute` entry to the `routes` list in the router config.
    * **Step 4**: Ensure the `builder` (or `pageBuilder`) returns the new Screen widget.

## Constraints
* **Never** hardcode route strings in the `GoRoute` definition; always use the constant.
* **Never** use `MaterialPageRoute` directly; always use GoRouter's declarative structure.
* If the route requires parameters (e.g., `:id`), ensure the builder parses `state.pathParameters`.
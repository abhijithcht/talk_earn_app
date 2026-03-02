---
id: skill_flutter_router_manager
name: Router Manager
version: 2.1.0
description: Manages the Router configuration for Flutter apps. Automates adding routes across `route_names.dart`, `app_router.dart` (or `main.dart` routes map) to enforce naming conventions.
tags: [flutter, navigation, architecture]
permissions: [read_file, write_file, analyze_code]
---

# Router Manager

## Overview
This skill acts as the gatekeeper for the routing configuration. It ensures that every new route is typed via constants and properly registered.

## Rules Engine

### 0. Unique Ownership
This skill is the **unique owner** of the routing configuration files (`route_names.dart`, `app_router.dart`). Other skills (like `feature-scaffold`) must delegate route registration to this skill.

### 1. The "Named Route" Protocol
Every new route must be registered to avoid magic strings:
1.  **`RoutePath`**: The URL segment (e.g., `'/details/:id'`).
2.  **`RouteName`**: The specific key for navigation (e.g., `'patientDetails'`).
3.  **Registry**: The actual route definition in `GoRouter` configuration.

### 2. Relative Path Enforcement
* **Root Routes**: Must start with `/` (e.g., `/dashboard`).
* **Nested Routes**: GoRouter paths should NOT start with `/` (e.g., `details` inside `/dashboard` becomes `/dashboard/details`).

## Prompts

### `add_route`
**Trigger:** `/route add <name> <path> [parent]`
**Example:** `/route add patient_details /patient/:id`

**Action Chain:**

**Step 1: Update Constants**
* Determine where route names are stored (e.g., `lib/core/routes/route_names.dart` or `lib/core/config/app_constants.dart`).
* Append `static const {{name}}Path = '{{path}}';`.
* Append `static const {{name}} = '{{name}}';`.

**Step 2: Generate Route Code**
* Creates a `GoRoute` block.
* Include `name: AppRoutes.{{name}}`.
* Include `path: AppRoutes.{{name}}Path`.
* Return the Page widget wrapped in `NoTransitionPage` if applicable, or standard `MaterialPage`.

**Step 3: Insert into Router Config**
* Locates `lib/core/routes/app_router.dart`.
* Injects the new `GoRoute` into the `routes` list.

## Usage Examples

**1. Create a simple page:**
User: "Add a 'Settings' page."
Skill:
1.  Adds `settings = 'settings'` and `settingsPath = '/settings'` to Constants.
2.  Injects `GoRoute` into the `GoRouter` configuration.
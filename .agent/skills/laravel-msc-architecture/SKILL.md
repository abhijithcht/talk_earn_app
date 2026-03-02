---
id: skill_laravel_msc_arch
name: Laravel MSC+RPR Architecture Enforcer
version: 2.0.0
description: Enforces the Model-Service-Controller-Resource-Policy-Request pattern. Ensures controllers remain skinny, logic resides in services, and responses are standardized.
tags: [laravel, architecture, design-patterns, backend]
permissions: [read_code, write_code, scaffold_files]
---

# Laravel MSC+RPR Architecture

## Overview
This skill mandates a strict separation of concerns. It forbids business logic in Controllers and formatting logic in Models.

## The 6-Layer Protocol

| Layer          | Responsibility                                                         | Allowed Dependencies                               |
| :------------- | :--------------------------------------------------------------------- | :------------------------------------------------- |
| **Request**    | Validation rules & authorization gate.                                 | `Illuminate\Foundation\Http\FormRequest`           |
| **Policy**     | User authorization logic.                                              | `User`, `Model`                                    |
| **Controller** | Traffic cop: Validates, Authorizes, Calls Service, Returns Response.   | `Request`, `Service`, `Resource`, `ResponseHelper` |
| **Service**    | **Business Logic Core.** DB transactions, calculations, external APIs. | `Model`, `DB`, `Log`, other `Services`             |
| **Model**      | Database definition, relationships, scopes, casts.                     | `Eloquent`, `Casts`                                |
| **Resource**   | Data transformation/formatting for API output.                         | `DateHelper`, `JsonResource`                       |

## Rules Engine

### 1. The "Skinny Controller" Rule
* **Forbidden:** Direct DB queries (`Model::where...`), complex loops, or raw `response()->json`.
* **Required:** Must inject a **Service**. Must return `ResponseHelper` wrapping a **Resource**.

### 2. The Service Isolation Rule
* Services must **not** know about HTTP (no `Request` objects passed to methods).
* Services return `Models`, `Collections`, or plain data (DTOs). They do **not** return JSON responses.

### 3. Standardization Hooks
* **Dates:** Resources must use `DateHelper::formatDateTime`.
* **Pagination:** Controllers must use `PaginationHelper::paginate` before passing to Resource.
* **Output:** Controllers must use `ResponseHelper`. It is the **only** allowed way to return JSON from Controllers.
* **Testing:** All layers must be tested according to `laravel-test-generator` conventions (Service tests in `Feature/`, Controller tests in `Feature/Api/`, etc.).

## Capabilities

### `scaffold_feature`
**Trigger:** `/scaffold <ModelName>`
**Action:** Generates all 6 layers for a feature, wired together automatically.

**Template Output for `/scaffold Product`:**

**1. Request (`StoreProductRequest.php`)**
```php
public function rules(): array {
    return [
        'name' => ['required', 'string', 'max:255'],
        'price' => ['required', 'numeric', 'min:0'],
    ];
}
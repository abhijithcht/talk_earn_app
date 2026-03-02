---
id: skill_laravel_response_std
name: Laravel API Response Standardizer
version: 1.0.0
description: Enforces consistent API response structures using app/Helpers/ResponseHelper.php and app/Helpers/PaginationHelper.php. Prevents ad-hoc `response()->json()` usage.
tags: [laravel, php, api, standardization]
permissions: [read_code, refactor_code]
---

# Laravel API Response Standardizer

## Overview
This skill acts as a linter and refactoring agent to ensure all API endpoints return data in a uniform structure. It specifically targets Controller methods to replace raw Laravel response macros with your custom `ResponseHelper`.

## Rules Engine

### 1. Forbidden Patterns
Flag and suggest replacements for direct JSON responses:
* **Detected:** `return response()->json(...)`
* **Action:** Suggest refactor to `ResponseHelper::success(...)` or `ResponseHelper::error(...)`.

### 2. Pagination Enforcement
* **Detected:** `$query->paginate($perPage)`
* **Action:** Replace with `PaginationHelper::paginate($query, $request, $searchFields)` combined with `ResponseHelper::paginated(...)`.

### 3. CRUD Mapping Strategy
Map standard controller actions to their corresponding Helper method:

| Action    | HTTP Status | Helper Method                         |
| :-------- | :---------- | :------------------------------------ |
| `index`   | 200         | `ResponseHelper::paginated($data)`    |
| `store`   | 201         | `ResponseHelper::created($data)`      |
| `show`    | 200         | `ResponseHelper::success(..., $data)` |
| `update`  | 200         | `ResponseHelper::success(..., $data)` |
| `destroy` | 200         | `ResponseHelper::deleted()`           |
| `catch`   | 400/500     | `ResponseHelper::error()`             |

## Prompts

### `generate_controller_method`
**Input:** Method type (e.g., "store"), Model name.
**Logic:**
1.  Wrap logic in `try-catch`.
2.  Use `DB::transaction` for mutations.
3.  Log errors using `ResponseHelper::logError`.
4.  Return standardized JSON.

**Template Output:**
```php
public function store(StoreRequest $request): JsonResponse
{
    try {
        $data = DB::transaction(function () use ($request) {
            return MyModel::create($request->validated());
        });

        // Always map through a Resource before returning
        $resource = new MyResource($data);

        return ResponseHelper::created($resource, 'Resource created successfully.');
    } catch (\Throwable $e) {
        ResponseHelper::logError('Failed to create resource', $e);
        return ResponseHelper::error('Unable to create resource.', 500);
    }
}
```
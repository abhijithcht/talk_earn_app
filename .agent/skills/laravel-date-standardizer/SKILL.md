---
id: skill_laravel_date_std
name: Laravel Date Formatting Standardizer
version: 1.0.0
description: Enforces global date consistency in API responses by mandating `App\Helpers\DateHelper` usage over raw Carbon formatting.
tags: [laravel, php, dates, standardization]
permissions: [read_code, refactor_code]
---

# Laravel Date Standardizer

## Overview
Inconsistent date formats (ISO8601 vs Y-m-d vs timestamps) break mobile apps. This skill detects manual date formatting and refactors it to use the `DateHelper` single source of truth.

## Rules Engine

### 1. The Carbon Ban
Detects manual formatting chains that bypass the helper.
* **Bad Pattern:** `$date->format('Y-m-d H:i:s')` or `Carbon::parse($d)->toDateTimeString()`
* **Refactor:** `DateHelper::formatDateTime($date)`

### 2. API Resource Enforcement
When generating or reviewing Laravel API Resources (`JsonResource`), ensure date fields use the helper.

* **Placement Policy:** Dates should be formatted in the **Resource** layer only. Do not format dates in Models or Services. Cross-check with `laravel-msc-architecture` for architectural compliance.

**Before:**
```php
return [
    'id' => $this->id,
    'created_at' => $this->created_at, // Risks returning ISO string
    'updated_at' => $this->updated_at->toDateTimeString(), // Hardcoded format
];
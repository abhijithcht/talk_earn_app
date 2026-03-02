---
id: skill_resource_extractor
name: resource-extractor
version: 1.0.0
description: Enforces centralization of primitives. Triggers when writing UI code involving text, layout dimensions, asset paths, or constants.
tags: [code_quality, flutter, refactoring]
permissions: [read_code, write_file]
---

# Resource Extractor Skill

## Goal
Eliminate "magic numbers" and "magic strings" by enforcing extraction to centralized configuration files.

## Instructions
1.  **Analyze Context**: Before writing any Widget code, scan:
    * `lib/core/constants/app_strings.dart`
    * `lib/core/constants/app_dimens.dart` (or `dimens.dart`)
    * `lib/core/constants/app_assets.dart`
    * `lib/core/constants/app_constants.dart`

2.  **Strings**:
    * If writing `Text('Login')`, check `app_strings.dart`.
    * If it exists, use `Text(AppStrings.login)`.
    * If not, **append it** to `app_strings.dart` first, then use the reference.

3.  **Dimensions/Padding**:
    * Never use `SizedBox(height: 20)`. Check `AppDimens` for a standard spacing (e.g., `AppDimens.spacingMedium`).
    * If a specific pixel value is needed and not standard, add it to `AppDimens` (e.g., `static const double imageHeaderHeight = 250.0;`).

4.  **Assets**:
    * Never use `Image.asset('assets/images/logo.png')`.
    * Always refer to `AppAssets.logo`.

## Rules
* Variable names should be descriptive (e.g., `welcomeMessage` instead of `text1`).
* Keep the centralized files sorted alphabetically if possible.
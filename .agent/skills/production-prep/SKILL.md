---
id: skill_flutter_production_prep
name: Production Launch Prep
version: 1.0.0
description: Automates the final polish for Flutter apps: Splash screens, Launcher icons, Package renaming, Dependency upgrades, and Asset cleanup.
tags: [flutter, production, automation, maintenance]
permissions: [read_file, write_file, execute_terminal]
---

# Production Launch Prep

## Overview
This skill consolidates five different manual tasks into single commands. It relies on standard community packages (`flutter_launcher_icons`, `flutter_native_splash`, `rename`, `flutter_clean_unused_assets`) to do the heavy lifting safely.

## Capabilities

### 1. `setup_branding`
**Trigger:** `/brand <App Name> <path_to_logo>`
**Action Chain:**
1.  **Icons:** Configures `flutter_launcher_icons` in `pubspec.yaml` using the provided logo.
2.  **Splash:** Configures `flutter_native_splash` (preserving transparency if PNG).
3.  **Rename:** Updates `AndroidManifest.xml`, `Info.plist`, and `Runner.xcodeproj` with the new App Name.
4.  **Execute:** Runs the generation commands automatically.

### 2. `update_package_id`
**Trigger:** `/package_id <com.new.id>`
**Action:**
* Uses the `rename` package logic to deeply refactor the Android package and iOS Bundle ID.
* **Safety Check:** Greps for the old package name in Kotlin/Swift files to ensure imports are updated.

### 3. `dependency_audit`
**Trigger:** `/audit deps`
**Action:**
1.  Runs `flutter pub outdated`.
2.  **Smart Upgrade:** Updates `pubspec.yaml` versions to the *resolvable* latest (avoiding major breaking changes unless requested).
3.  **Cleanup:** Runs `flutter pub deps --no-dev` to check for unused packages.

### 4. `cleanup_assets`
**Trigger:** `/clean assets`
**Action:**
1.  Scans `lib/` and `pubspec.yaml` for asset references.
2.  Compares against files in `assets/`.
3.  **Report:** Lists files that are sitting in `assets/` but **never used** in code.
4.  **Prompt:** "Found 12MB of unused images. Delete them?"

---

## Conflict Avoidance
*   **Asset Management**: Asset cleanup detects usage via `AppAssets` references (centralized by `resource-extractor`). Ensure `flutter-asset-registrar` and `resource-extractor` have run before performing a cleanup to avoid false positives.

## Prompts

### `generate_config`
**Input:** User provides a logo path.
**Template Output (`pubspec.yaml` additions):**
```yaml
dev_dependencies:
  flutter_launcher_icons: "^0.13.1"
  flutter_native_splash: "^2.3.1"

flutter_icons:
  android: "launcher_icon"
  ios: true
  image_path: "{{logo_path}}"
  adaptive_icon_background: "#FFFFFF"

flutter_native_splash:
  color: "#FFFFFF"
  image: "{{logo_path}}"
  branding: "assets/images/branding_bottom.png"
  android_12:
    image: "{{logo_path}}"
    color: "#FFFFFF"
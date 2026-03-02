---
id: skill_theme_manager
name: theme-manager
version: 1.0.0
description: Manages centralized application theming (colors, typography, theme data). Triggers when styling widgets or adding new visual properties.
tags: [flutter, theme, ui]
permissions: [read_code, write_file]
---

# Theme Guardian Skill

## Goal
Enforce a consistent design system by routing all style requests through centralized theme files.

## Instructions
1.  **Analyze Context**: Before applying a color or style, scan:
    * `lib/core/theme/app_colors.dart`
    * `lib/core/theme/app_theme.dart` (ThemeData configuration)
    * `lib/core/theme/app_typography.dart` (if separate)

2.  **Colors**:
    * **Forbidden**: `Color(0xFF123456)` or `Colors.red` inside a Widget.
    * **Action**: Check `AppColors`. If the color exists, use it. If not, add it to `AppColors` first (e.g., `static const heavyRed = Color(0xFFFF0000);`).
    * **Usage**: Prefer `Theme.of(context).colorScheme.primary` (Material 3) or `AppColors.customColor`.

3.  **Text Styles**:
    * **Forbidden**: `TextStyle(fontSize: 24, fontWeight: FontWeight.bold)`.
    * **Action**: Use `Theme.of(context).textTheme`.
    * *Mapping*:
        * Large Titles → `displayLarge` / `headlineMedium`
        * Content → `bodyLarge` / `bodyMedium`
        * Captions → `labelSmall`
    * If a custom style is absolutely needed, create a `static TextStyle` in your theme config, do not inline it.

4.  **Dark Mode**:
    * When adding a color to `AppColors`, strictly define both its Light and Dark variants if your app supports it.

## Example
User: "Make the button background blue."
Agent Action:
1.  Does `AppColors.primaryBlue` exist? Yes.
2.  Update Widget: `style: ElevatedButton.styleFrom(backgroundColor: AppColors.primaryBlue)`.
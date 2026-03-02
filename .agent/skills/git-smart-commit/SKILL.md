---
id: skill_git_smart_commit
name: git-smart-commit
version: 1.0.0
description: Stating and committing changes using Conventional Commits. Triggers when the user says "commit", "save progress", or "push changes".
tags: [git, commit, productivity]
permissions: [run_command]
---

# Smart Committer Skill

## Goal
To maintain a clean git history by strictly adhering to the **Conventional Commits** specification (`feat`, `fix`, `chore`, `refactor`, etc.).

## Instructions
1.  **Status Check**: Run `git status` to see modified files.
2.  **Staging**:
    * If the user specified files (e.g., "commit the login page"), `git add` only those files.
    * If unspecified, ask: "Should I stage all changes?" or run `git add .` if the context implies a full save.
3.  **Diff Analysis**: Run `git diff --staged` to understand *what* changed.
4.  **Message Generation**:
    * Generate a message in the format: `<type>(<scope>): <description>`
    * **Types**:
        * `feat`: New features.
        * `fix`: Bug fixes.
        * `ui`: Visual updates (styling/assets).
        * `refactor`: Code restructuring without behavior change.
        * `chore`: Maintenance (pubspec updates, config).
    * **Scope**: The feature or file affected (e.g., `auth`, `router`, `assets`).
    * **Description**: Lowercase, no period at end, imperative mood ("add" not "added").
5.  **Execution**: Run `git commit -m "..."`.

## Example
* *Change:* Added `GoRoute` for Settings.
* *Command:* `git commit -m "feat(navigation): add settings route configuration"`
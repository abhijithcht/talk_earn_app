---
id: skill_env_guard
name: Environment Variable Guard
version: 1.0.0
description: Prevents runtime crashes by ensuring .env files are in sync with code usage.
tags: [config, devops]
permissions: [read_file]
---

# Env Guard

## Rules Engine
1.  **Usage Scan:** Greps codebase for `env('KEY')` (Laravel) or `dotenv.env['KEY']` (Flutter).
2.  **Definition Check:** Verifies that every key found in code exists in `.env` and `.env.example`.
3.  **Cross-Check:** (Optional) Warns if `API_BASE_URL` in Flutter `.env` does not match the local IP of the Laravel server.

## Prompts
> "Scan the project for missing environment variables. Did I add `PUSHER_APP_ID` to `.env.example`?"
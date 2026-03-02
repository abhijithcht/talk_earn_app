---
id: skill_database_schema_validator
name: database-schema-validator
version: 1.0.0
description: Validates MySQL schema files/migrations for Laravel compliance, naming safety, and strict policy.
tags: [database, laravel, mysql, safety]
permissions: [run_command]
---

# Database Schema Validator Skill (Laravel/MySQL)

This skill ensures that SQL migration exports or schema files comply with Laravel's Eloquent expectations and MySQL safety standards.

## Policies Enforced

1. **Safety**: Forbidden `DROP TABLE` or `TRUNCATE` statements to prevent data loss.
2. **Naming**: Tables must be `snake_case` (plural preferred for Laravel).
3. **Primary Keys**: Every table must use an `id` column as the Primary Key (unsigned big integer/AI).
4. **Engine**: Tables should specify `ENGINE=InnoDB` for Laravel transaction support.

## Instructions

1. **Environment**: Use the system-wide **Python 3.12.10** on Windows 11.
2. **Execution**: Run the validation script using the `run_command` tool.

   ```powershell
   python "$HOME\.gemini\skills\database-schema-validator\scripts\validate_schema.py" <path_to_sql_file>

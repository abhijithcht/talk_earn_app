---
id: skill_license_header_adder
name: license-header-adder
version: 1.0.0
description: Injects a standardized license/copyright header into the top of code files (.dart, .php, .tsx, .ts, .js).
tags: [code_quality, license, legal]
permissions: [write_file]
---

# License Header Adder Skill

This skill ensures all source code files contain the mandatory project license header.

## Header Template

Customize the following block based on project needs:

```text
/*
 * File: {{filename}}
 * Project: {{project_name}}
 * Created Date: {{date}}
 * Author: {{user}}
 * -----
 * Copyright (c) {{year}} Your Company/Name
 */

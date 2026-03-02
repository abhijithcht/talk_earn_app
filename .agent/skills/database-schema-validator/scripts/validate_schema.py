import sys
import re
import os

def validate_laravel_mysql_schema(filename):
    """
    Validates MySQL schema for Laravel compliance:
    1. No DROP/TRUNCATE (Safety).
    2. Table names in snake_case.
    3. Primary key must be 'id'.
    4. InnoDB Engine check for transaction safety.
    """
    if not os.path.exists(filename):
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)

    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()

        errors = []

        # 1. Safety Check: Destructive operations
        if re.search(r'\b(DROP|TRUNCATE)\b\s+TABLE', content, re.IGNORECASE):
            errors.append("POLICY VIOLATION: 'DROP' or 'TRUNCATE' statements are forbidden.")

        # 2. Extract Table Definitions
        # Handles: CREATE TABLE `users` ( ... ) ENGINE=InnoDB;
        table_matches = re.finditer(
            r'CREATE\s+TABLE\s+[`"]?(?P<name>\w+)[`"]?\s*\((?P<body>.*?)\)(?P<suffix>[^;]*)',
            content,
            re.DOTALL | re.IGNORECASE
        )

        found_tables = False
        for match in table_matches:
            found_tables = True
            table_name = match.group('name')
            body = match.group('body')
            suffix = match.group('suffix')

            # Snake case check
            if not re.match(r'^[a-z][a-z0-9_]*$', table_name):
                errors.append(f"NAMING ERROR: Table '{table_name}' must be snake_case.")

            # Primary key 'id' check (Laravel standard)
            if not re.search(r'[`"]?id[`"]?\s+.*PRIMARY KEY', body, re.IGNORECASE):
                errors.append(f"SCHEMA ERROR: Table '{table_name}' is missing an 'id' PRIMARY KEY.")

            # InnoDB check (Required for Laravel transactions)
            if not re.search(r'ENGINE\s*=\s*InnoDB', suffix, re.IGNORECASE):
                errors.append(f"CONFIG ERROR: Table '{table_name}' should use ENGINE=InnoDB.")

        if not found_tables:
            errors.append("WARNING: No CREATE TABLE statements found in file.")

        if errors:
            for err in errors:
                print(err)
            sys.exit(1)
        else:
            print("MySQL Schema validation passed for Laravel.")
            sys.exit(0)

    except Exception as e:
        print(f"Internal Script Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python validate_schema.py <file_path>")
        sys.exit(1)
    validate_laravel_mysql_schema(sys.argv[1])
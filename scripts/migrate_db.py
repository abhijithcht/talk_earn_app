import sqlite3

def migrate():
    try:
        conn = sqlite3.connect('talk_earn.db')
        cursor = conn.cursor()
        
        # Check if full_name exists
        cursor.execute("PRAGMA table_info(users)")
        columns = [row[1] for row in cursor.fetchall()]
        
        if 'full_name' not in columns:
            print("Adding full_name column to users table...")
            cursor.execute("ALTER TABLE users ADD COLUMN full_name VARCHAR(255)")
            conn.commit()
            print("Migration successful.")
        else:
            print("full_name column already exists.")
            
        conn.close()
    except Exception as e:
        print(f"Migration error: {e}")

if __name__ == "__main__":
    migrate()

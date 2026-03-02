import sqlite3

conn = sqlite3.connect('talk_earn.db')
c = conn.cursor()
try:
    c.execute("ALTER TABLE users ADD COLUMN is_email_verified BOOLEAN DEFAULT 0")
    print("Added is_email_verified")
except Exception as e:
    print(e)
    
try:
    c.execute("ALTER TABLE users ADD COLUMN otp_code VARCHAR")
    print("Added otp_code")
except Exception as e:
    print(e)
    
c.execute("UPDATE users SET is_email_verified = 1, is_active = 1 WHERE email = 'akashmohanan2025@gmail.com'")
conn.commit()
conn.close()
print("Test User activated.")

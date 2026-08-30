import sqlite3

# Define target database file name
db_name = "harvester_vault.db"

# Step 1: Establish Connection Pipe and Cursor Workspace
conn = sqlite3.connect(db_name)
cursor = conn.cursor()

# Step 2: Define Persistent Relational Schema
cursor.execute("""
    CREATE TABLE IF NOT EXISTS api_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        search_topic TEXT NOT NULL,
        page_num INTEGER NOT NULL,
        url TEXT UNIQUE NOT NULL,
        fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")

print("✅ Database Connection Established & Table Schema Verified!")

# Step 3: Define Dynamic Record Data
sample_topic = "AI & Executive Automation"
sample_page = 1
sample_url = "https://httpbin.org/get?q=AI+Automation&page=1"

# Step 4: Parameterized Insertion Guardrail (Prevents SQL Injection)
try:
  cursor.execute(
      """
        INSERT INTO api_records (search_topic, page_num, url)
        VALUES (?, ?, ?)
    """,
      (sample_topic, sample_page, sample_url),
  )

  # Step 5: Commit Staged Transaction to Physical Disk
  conn.commit()
  print("✅ Record Successfully Staged and Committed to Disk File!")

except sqlite3.IntegrityError as err:
  print(f"⚠️ Duplicate Entry Blocked by UNIQUE Constraint: {err}")

# Step 6: Query and Read Back Disk Data
cursor.execute(
    "SELECT id, search_topic, page_num, url, fetched_at FROM api_records"
)
records = cursor.fetchall()

print("\n--- 📊 Persistent Database Vault Contents ---")
for row in records:
  print(
      f"ID: {row[0]} | Topic: {row[1]} | Page: {row[2]} | URL: {row[3]} |"
      f" Timestamp: {row[4]}"
  )

# Step 7: Clean Stream Shutdown
conn.close()
print("\n✅ Database Connection Stream Closed Safely.")
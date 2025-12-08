import psycopg2

conn = psycopg2.connect(
    host='localhost', 
    port=5432, 
    user='fastapi_user', 
    password='change-me', 
    database='fastapipro'
)

cur = conn.cursor()
cur.execute("""
    SELECT column_name, data_type, column_default 
    FROM information_schema.columns 
    WHERE table_name='groups' 
    ORDER BY ordinal_position;
""")

rows = cur.fetchall()
print('Groups table structure:')
for row in rows:
    print(f'{row[0]:20} {row[1]:20} {str(row[2])[:50]}')

cur.close()
conn.close()

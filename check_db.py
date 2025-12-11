import sqlite3

# Conecta ao arquivo gerado pelo seu Flask
con = sqlite3.connect("database.db")
cursor = con.cursor()

# Check if Table Exists
try:
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    if not users:
        print("A tabela 'users' existe, mas está vazia.")
    else:
        print(f"Foram encontrados {len(users)} registro(s):\n")
        print(f"{'ID':<5} | {'NOME':<20} | {'EMAIL'}                 | {'MESSAGE'} ")
        print("-" * 40)
        for user in users:

            # 0=id, 1=nome, 2=email
            print(f"{user[0]:<5} | {user[1]:<20} | {user[2]}             | {user[3]}")

except sqlite3.OperationalError:
    print("A tabela não existe!.")

con.close()
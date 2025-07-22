# Codigo para asignar ds_eval a Gazitua y Ruiz
# 500 cada uno de manera aleatoria en la bd

import psycopg2
import random
from dotenv import load_dotenv
import os

load_dotenv()

db_host = os.getenv('db_host')
db_user = os.getenv('db_user')
db_password = os.getenv('db_password')
db_port = os.getenv('db_port')
db_name = os.getenv('db_name')

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    host=db_host,
    user=db_user,
    password=db_password,
    port=db_port,
    database=db_name
)
# Create a cursor object
cur = conn.cursor()

# Get the list of all ds_eval where name is 'jalonsol' and security is null
cur.execute("SELECT sha FROM ds_eval WHERE name = 'jalonsol' AND security IS NULL")

# Fetch all the results
shas = cur.fetchall()

# Count the number of shas
num_shas = len(shas)
print(f"Number of shas: {num_shas}")

# Reorder the list of shas randomly
random.shuffle(shas)

# Gazitua user
nameG = 'fco_gazitua_requena'
# Ruiz user
nameR = 'ffruiz'

# Calculate the number of shas to assign to each user
cur.execute(f'SELECT COUNT(*) FROM ds_eval WHERE name = \'{nameG}\'')
num_assignedG = cur.fetchone()[0]
num_assignedG = 500 - num_assignedG

cur.execute(f'SELECT COUNT(*) FROM ds_eval WHERE name = \'{nameR}\'')
num_assignedR = cur.fetchone()[0]
num_assignedR = 500 - num_assignedR

# Assign shas to Gazitua and Ruiz
for i in range(num_assignedG):
    sha = shas[i][0]
    cur.execute(f"UPDATE ds_eval SET name = '{nameG}' WHERE sha = '{sha}' and name = 'jalonsol' AND security IS NULL")

for i in range(num_assignedR):
    sha = shas[i + num_assignedG][0]
    cur.execute(f"UPDATE ds_eval SET name = '{nameR}' WHERE sha = '{sha}' and name = 'jalonsol' AND security IS NULL")

# Commit the changes to the database
conn.commit()

# Print the number of shas remaining for 'jalonsol'
cur.execute("SELECT COUNT(*) FROM ds_eval WHERE name = 'jalonsol' AND security IS NULL")
remaining_shas = cur.fetchone()[0]
print(f"Number of shas remaining for jalonsol: {remaining_shas}")

# Print the number of shas assigned to Gazitua and Ruiz
cur.execute(f"SELECT COUNT(*) FROM ds_eval WHERE name = '{nameG}' AND security IS NULL")
num_assignedG = cur.fetchone()[0]
cur.execute(f"SELECT COUNT(*) FROM ds_eval WHERE name = '{nameR}' AND security IS NULL")
num_assignedR = cur.fetchone()[0]
print(f"Number of shas assigned to {nameG}: {num_assignedG}")
print(f"Number of shas assigned to {nameR}: {num_assignedR}")

# Close the cursor and connection
cur.close()
conn.close()

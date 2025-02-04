import psycopg2

dbname = 'bd2-2024'
user = 'postgres'
password = 'admin'
host = 'localhost'
port = '5432'

try:
    with psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    ) as conn:
        print("Ligação bem-sucedida!")
except psycopg2.Error as e:
    print(f"Falha na ligação: {e}")

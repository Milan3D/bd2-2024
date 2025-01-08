import psycopg2

dbname = 'bd2_postgres'
user = 'bd2_postgres_user'
password = '9yu4SjRH5MUWa1mfxYSPyJHPl2Kn9RaA'
host = 'dpg-cmhpknen7f5s739ugg4g-a.frankfurt-postgres.render.com'
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

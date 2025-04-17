import psycopg2
from config import load_config

def delete(name, phone):
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("CALL deleting(%s, %s)", (name, phone))
                if conn.notices:
                    for notice in conn.notices:
                        print(notice.strip())
                else:
                    print("Succes!")
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

name, phone = input("Enter a name: "), input("Enter a phone: ")
delete(name, phone)
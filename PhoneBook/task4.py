import psycopg2

config = {
    "host": "localhost",
    "database": "phone",
    "user": "postgres",
    "password": "12345"
}

def get_pagination(limit, offset):
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("select get_paginated_records(%s, %s)", (limit, offset))
                result = cur.fetchall()
                print(result)
        print("Success!")
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)
        
limit, offset = int(input("Enter limit: ")), int(input("Enter offset: "))
get_pagination(limit, offset)
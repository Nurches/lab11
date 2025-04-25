import psycopg2

def create_table_and_function():

    conn = psycopg2.connect(
        dbname="phone",
        user="postgres",
        password="",
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()

    try:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS phonebook (
            name TEXT,
            phone TEXT
        );
        """)

        cur.execute("""
        CREATE OR REPLACE FUNCTION insert_users_from_list(
            names TEXT[], 
            phones TEXT[]
        )
        RETURNS VOID AS $$
        DECLARE
            i INTEGER;
        BEGIN
            FOR i IN 1..array_length(names, 1) LOOP
                IF phones[i] IS NULL OR phones[i] !~ '^\\d+$' THEN
                    RAISE NOTICE 'incorrect: %, %', names[i], phones[i];
                ELSE
                    INSERT INTO phonebook(name, phone)
                    VALUES (names[i], phones[i]);
                END IF;
            END LOOP;
        END;
        $$ LANGUAGE plpgsql;
        """)

        conn.commit()
        print("Succes!")

    except Exception as e:
        print("Error", e)

    finally:
        cur.close()
        conn.close()


def insert_multiple_users():
    
    conn = psycopg2.connect(
        dbname="phone",
        user="postgres",
        password="12345",
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()

    try:
        while True:
            try:
                count = int(input("Enter "))
                if count <= 0:
                    print("Enter a Positive")
                    continue
                break
            except ValueError:
                print("Enter")

        users = []
        phones = []

        for i in range(count):
            name = input(f"Enter {i + 1}: ").strip()
            phone = input(f"Enter a phone #{i + 1}: ").strip()
            users.append(name)
            phones.append(phone)

        cur.execute(
            "SELECT insert_users_from_list(%s, %s);",
            (users, phones)
        )
        conn.commit()

        print("\n Succes")

    except Exception as e:
        print("Error! ", e)

    finally:
        cur.close()
        conn.close()


if __name__== "main":
    
    create_table_and_function()
    insert_multiple_users()
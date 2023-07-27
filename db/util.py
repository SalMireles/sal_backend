import psycopg2


def db_connection():
    connection = psycopg2.connect(
        host="db",
        database="science",
        user="postgres",
        password="postgres",
        port="5432",
    )

    return connection


def db_transaction(func):
    def wrapper(*args, **kwargs):
        conn = db_connection()
        cur = conn.cursor()

        try:
            func(cur, *args, **kwargs)
            if func.__name__.startswith("insert"):
                conn.commit()
                return {"status": "success"}
            else:
                all_data = [[str(x) for x in i] for i in cur.fetchall()]
                return {
                    "status": "success",
                    "headings": [i[0] for i in cur.description],
                    "data": all_data[0][0],
                }
        except Exception as error:
            print(error)
            return {
                "status": "err",
                "err": "There was a problem processing your request.",
            }
        finally:
            cur.close()
            conn.close()

    return wrapper

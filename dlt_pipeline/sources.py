import psycopg2
import dlt

from config import POSTGRES


def get_connection():
    return psycopg2.connect(
        host=POSTGRES["host"],
        port=POSTGRES["port"],
        database=POSTGRES["database"],
        user=POSTGRES["user"],
        password=POSTGRES["password"],
    )


@dlt.resource(write_disposition="replace")
def customers():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM customers")

    columns = [desc[0] for desc in cursor.description]

    for row in cursor.fetchall():
        yield dict(zip(columns, row))

    cursor.close()
    conn.close()


@dlt.resource(write_disposition="replace")
def employees():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM employees")

    columns = [desc[0] for desc in cursor.description]

    for row in cursor.fetchall():
        yield dict(zip(columns, row))

    cursor.close()
    conn.close()


@dlt.resource(write_disposition="replace")
def order_items():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM order_items")

    columns = [desc[0] for desc in cursor.description]

    for row in cursor.fetchall():
        yield dict(zip(columns, row))

    cursor.close()
    conn.close()


@dlt.resource(write_disposition="replace")
def orders():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM orders")

    columns = [desc[0] for desc in cursor.description]

    for row in cursor.fetchall():
        yield dict(zip(columns, row))

    cursor.close()
    conn.close()

@dlt.resource(write_disposition="replace")
def products():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM products")

    columns = [desc[0] for desc in cursor.description]

    for row in cursor.fetchall():
        yield dict(zip(columns, row))

    cursor.close()
    conn.close()

@dlt.resource(write_disposition="replace")
def stores():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM stores")

    columns = [desc[0] for desc in cursor.description]

    for row in cursor.fetchall():
        yield dict(zip(columns, row))

    cursor.close()
    conn.close()
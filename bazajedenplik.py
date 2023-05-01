import sqlite3
from sqlite3 import Error


# utworzenie bazy
def create_connection(db_file):
    """create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def execute_sql(conn, sql):
    """Execute sql
    :param conn: Connection object
    :param sql: a SQL script
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(sql)
    except Error as e:
        print(e)


# dodawanie danych do bazy
def add_item(conn, item):
    """
    Create a new item into the items table
    :param conn:
    :param item:
    :return: item id
    """
    sql = """INSERT INTO items(nazwa, quantity, description)
             VALUES(?,?,?)"""
    cur = conn.cursor()
    cur.execute(sql, item)
    conn.commit()
    return cur.lastrowid


def add_sale(conn, sale):
    """
    Create a new sale into the sales table
    :param conn:
    :param sale:
    :return: sale id
    """
    sql = """INSERT INTO sales(items_id, sales_quantity, status, sales_date)
             VALUES(?,?,?,?)"""
    cur = conn.cursor()
    cur.execute(sql, sale)
    conn.commit()
    return cur.lastrowid


# przykładowe pobieranie danych:


# pobranie wszystkiego -wszystkie wiersze w tabeli
def select_all(conn, table):
    """
    Query all rows in the table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {table}")
    rows = cur.fetchall()

    return rows


# pobranie wszystkie wybane wiersze
def select_where(conn, table, **query):
    """
    Query tasks from table with data from **query dict
    :param conn: the Connection object
    :param table: table name
    :param query: dict of attributes and values
    :return:
    """
    cur = conn.cursor()
    qs = []
    values = ()
    for k, v in query.items():
        qs.append(f"{k}=?")
        values += (v,)
    q = " AND ".join(qs)
    cur.execute(f"SELECT * FROM {table} WHERE {q}", values)
    rows = cur.fetchall()
    return rows


# przykładowe modyfikowanie danych:
def update(conn, table, id, **kwargs):
    """
    update quantity of a sales
    :param conn:
    :param table: table name
    :param id: row id
    :return:
    """
    parameters = [f"{k} = ?" for k in kwargs]
    parameters = ", ".join(parameters)
    values = tuple(v for v in kwargs.values())
    values += (id,)

    sql = f""" UPDATE {table}
             SET {parameters}
             WHERE id = ?"""
    try:
        cur = conn.cursor()
        cur.execute(sql, values)
        conn.commit()
        print("OK")
    except sqlite3.OperationalError as e:
        print(e)


# prrzykładowe usunięcie danych:
def delete_where(conn, table, **kwargs):
    """
    Delete from table where attributes from
    :param conn:  Connection to the SQLite database
    :param table: table name
    :param kwargs: dict of attributes and values
    :return:
    """
    qs = []
    values = tuple()
    for k, v in kwargs.items():
        qs.append(f"{k}=?")
        values += (v,)
    q = " AND ".join(qs)

    sql = f"DELETE FROM {table} WHERE {q}"
    cur = conn.cursor()
    cur.execute(sql, values)
    conn.commit()
    print("Deleted")


if __name__ == "__main__":
    # utworzenie bazy
    create_items_sql = """
   -- projects table
   CREATE TABLE IF NOT EXISTS items (
      id integer PRIMARY KEY,
      nazwa text NOT NULL,
      quantity text,
      description text
   );
   """

    create_sales_sql = """
   -- zadanie table
   CREATE TABLE IF NOT EXISTS sales (
      id integer PRIMARY KEY,
      items_id integer NOT NULL,
      sales_quantity integer NOT NULL,
      status VARCHAR(15) NOT NULL,
      sales_date text NOT NULL,
      FOREIGN KEY (items_id) REFERENCES items (id)
   );
   """

    db_file = "mojabaza.db"

    conn = create_connection(db_file)
    if conn is not None:
        execute_sql(conn, create_items_sql)
        execute_sql(conn, create_sales_sql)
        conn.close()

    # dodanie do bazy
    item = ("Książki", "Opowiadanki i takie tam inne", "34")
    item1 = ("Filmy", "O tym i o tamtym", "101")

    conn = create_connection("mojabaza.db")

    pr_id = add_item(conn, item)
    pr_id1 = add_item(conn, item1)

    sale = (pr_id, "4", "started", "2023-04-11 12:00:00")
    sale1 = (pr_id1, "15", "started", "2023-04-19 19:00:00")

    sale_id = add_sale(conn, sale)
    sale_id1 = add_sale(conn, sale1)

    print(pr_id, pr_id1, sale_id, sale_id1)
    conn.commit()

    # pobranie danych z bazy
    # select jednej rzeczy:
    print(select_where(conn, "items", id=1))
    print(select_where(conn, "sales", status="started"))

    # wszystkie wiersze z tabeli:
    print(select_all(conn, "items"))
    print(select_all(conn, "sales"))

    # modyfikowanie danych
    update(conn, "sales", 1, status="done")
    print(select_all(conn, "sales"))

    # usunięcie danych
    conn = create_connection("mojabaza.db")
    delete_where(conn, "sales", id=1)
    print(select_all(conn, "sales"))

    conn.close()

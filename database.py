import psycopg2

from payloads import payload_functions

# Database configuration
DATABASE_CONFIG = {
    'database': 'matrixssdb',
    'user': 'matrixss',
    'password': 'matrixss',
    'host': 'localhost',
    'port': 5432
}

def connect_db():
    """Connect to the PostgreSQL database."""
    conn = psycopg2.connect(database="matrixssdb",
                            user="matrixss",
                            password="matrixss",
                            host="localhost", port="5432")
    return conn

def initialize_db():
    """Create the payloads table if it does not exist."""
    print("test")
    conn = connect_db()
    print("Connection: " + conn)

    with conn.cursor() as cur:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS payloads (
            id SERIAL PRIMARY KEY,
            func_name VARCHAR(100) NOT NULL,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            payload TEXT NOT NULL
        );
        """)
        conn.commit()
    conn.close()

def insert_payload(func_name, title, description, payload):
    """Insert a new payload into the database."""
    conn = connect_db()
    with conn.cursor() as cur:
        cur.execute("""
        INSERT INTO payloads (func_name, title, description, payload)
        VALUES (%s, %s, %s, %s);
        """, (func_name, title, description, payload))
        conn.commit()
    conn.close()

def populate_payloads():
    """Populate the payloads table with predefined payloads."""
    for func_name, title, description, payload in payload_functions:
        insert_payload(func_name, title, description, payload)

def fetch_payloads():
    """Fetch all payloads from the database."""
    conn = connect_db()
    with conn.cursor() as cur:
        cur.execute("SELECT func_name, title, description, payload FROM payloads;")
        payloads = cur.fetchall()
    conn.close()
    return payloads

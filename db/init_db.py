from db.seeds import (
    seed_user_table,
    seed_experiment_table,
    seed_experiment_compound_table,
    seed_compound_table,
)

from db.util import db_connection


def is_db_initialized():
    """Checks that tables exist and contain data."""

    conn = db_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT EXISTS(SELECT 1 FROM pg_class WHERE relname = %s)", ("Users",)
    )
    relation_exists = cur.fetchone()[0]
    if relation_exists:
        cur.execute("SELECT EXISTS(SELECT * FROM Users)")
        data_exists = cur.fetchone()[0]
        return data_exists

    cur.close()
    conn.close()

    return False


def init_schema():
    print("Initializing database schema...")

    conn = db_connection()
    conn.autocommit = True
    cur = conn.cursor()

    # Experiment DATA
    cur.execute("DROP TABLE IF EXISTS Users CASCADE;")
    cur.execute(
        """CREATE TABLE Users (
        user_id INTEGER NOT NULL,
        name VARCHAR(50) NOT NULL, 
        email VARCHAR(50) NOT NULL,
        signup_date DATE NOT NULL, 
        PRIMARY KEY (user_id));"""
    )

    cur.execute("DROP TABLE IF EXISTS Experiment CASCADE;")
    cur.execute(
        """CREATE TABLE Experiment (
        experiment_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        experiment_run_time INTEGER NOT NULL, 
        FOREIGN KEY (user_id) REFERENCES Users(user_id),
        PRIMARY KEY (experiment_id));"""
    )

    cur.execute("DROP TABLE IF EXISTS Compound CASCADE;")
    cur.execute(
        """CREATE TABLE Compound (
        compound_id INTEGER NOT NULL,
        compound_name VARCHAR(50) NOT NULL, 
        compound_structure VARCHAR(50) NOT NULL,
        PRIMARY KEY (compound_id));"""
    )

    cur.execute("DROP TABLE IF EXISTS ExperimentCompound;")
    cur.execute(
        """CREATE TABLE ExperimentCompound (
        experiment_id INTEGER NOT NULL,
        compound_id INTEGER NOT NULL, 
        PRIMARY KEY (experiment_id, compound_id),
        FOREIGN KEY (experiment_id) REFERENCES Experiment(experiment_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE, 
        FOREIGN KEY (compound_id) REFERENCES Compound(compound_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE);"""
    )

    # Metrics
    cur.execute("DROP TABLE IF EXISTS UserMetric;")
    cur.execute(
        """CREATE TABLE UserMetric (
        id SERIAL PRIMARY KEY,
        user_id INTEGER NOT NULL,
        metric_name VARCHAR(50) NOT NULL, 
        metric_result FLOAT NOT NULL,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES Users(user_id)
        );"""
    )

    cur.execute("DROP TABLE IF EXISTS GlobalMetric;")
    cur.execute(
        """CREATE TABLE GlobalMetric (
        id SERIAL PRIMARY KEY,
        metric_name VARCHAR(50) NOT NULL, 
        metric_result FLOAT NOT NULL, 
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );"""
    )

    cur.close()
    conn.close()

    print("Database Schema Initialized")


def seed_db():
    connection = db_connection()
    seed_user_table(connection)
    seed_experiment_table(connection)
    seed_compound_table(connection)
    seed_experiment_compound_table(connection)
    connection.close()


def load_csv_data_into_db():
    db_initialized = is_db_initialized()
    if not db_initialized:
        init_schema()
        seed_db()

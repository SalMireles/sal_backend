from data.data_loader import (
    USER_DATA,
    USER_EXPERIMENT_DATA,
    COMPOUND_DATA,
    EXPERIMENT_COMPOUND_DATA,
)


def seed_user_table(connection):
    sql_command = (
        "INSERT INTO Users ("
        "user_id, "
        "name, "
        "email, "
        "signup_date "
        ") "
        "VALUES (%s, %s, %s, %s)"
    )

    # Add data
    cursor = connection.cursor()
    for data in USER_DATA:
        user_id, name, email, signup_date = data
        cursor.execute(
            sql_command,
            (
                int(user_id),
                name,
                email,
                signup_date,
            ),
        )

    connection.commit()
    cursor.close()


def seed_experiment_table(connection):
    sql_command = (
        "INSERT INTO Experiment ("
        "experiment_id, "
        "user_id, "
        "experiment_run_time"
        ") "
        "VALUES (%s, %s, %s)"
    )

    # Add data
    cursor = connection.cursor()
    for data in USER_EXPERIMENT_DATA:
        exp_id, user_id, run_time = data
        cursor.execute(
            sql_command,
            (
                int(exp_id),
                int(user_id),
                int(run_time),
            ),
        )

    connection.commit()
    cursor.close()


def seed_experiment_compound_table(connection):
    sql_command = (
        "INSERT INTO ExperimentCompound ("
        "experiment_id, "
        "compound_id"
        ") "
        "VALUES (%s, %s)"
    )

    # Add data
    cursor = connection.cursor()
    for data in EXPERIMENT_COMPOUND_DATA:
        exp_id, compound_id = data
        cursor.execute(
            sql_command,
            (
                int(exp_id),
                int(compound_id),
            ),
        )

    connection.commit()
    cursor.close()


def seed_compound_table(connection):
    sql_command = (
        "INSERT INTO Compound ("
        "compound_id, "
        "compound_name, "
        "compound_structure"
        ") "
        "VALUES (%s, %s, %s)"
    )

    # Add data
    cursor = connection.cursor()
    for data in COMPOUND_DATA:
        compound_id, compound_name, compound_structure = data
        cursor.execute(
            sql_command,
            (
                int(compound_id),
                compound_name,
                compound_structure,
            ),
        )

    connection.commit()
    cursor.close()

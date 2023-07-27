from db.metric_insert_strings import (
    insert_total_user_experiments_sql,
    insert_average_experiments_per_user_sql,
    insert_most_commonly_used_compound_sql,
)

from db.util import db_transaction


@db_transaction
def insert_metrics_total_user_experiments(
    cur, user_id, metric_name, metric_result
):
    cur.execute(
        insert_total_user_experiments_sql,
        (
            user_id,
            metric_name,
            metric_result,
        ),
    )


@db_transaction
def insert_metrics_average_experiments_per_user(
    cur, metric_name, metric_result
):
    cur.execute(
        insert_average_experiments_per_user_sql,
        (
            metric_name,
            metric_result,
        ),
    )


@db_transaction
def insert_metrics_most_commonly_used_compound(cur, metric_name, metric_result):
    cur.execute(
        insert_most_commonly_used_compound_sql,
        (
            metric_name,
            metric_result,
        ),
    )

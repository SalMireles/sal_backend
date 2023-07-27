from db.metric_query_strings import (
    query_total_user_experiments_sql,
    query_average_experiments_per_user_sql,
    query_most_commonly_used_compound_sql,
)
from db.util import db_transaction


@db_transaction
def query_metrics_total_user_experiments(cur, user_id):
    cur.execute(query_total_user_experiments_sql, (user_id,))


@db_transaction
def query_metrics_average_experiments_per_user(cur):
    cur.execute(query_average_experiments_per_user_sql)


@db_transaction
def query_metrics_most_commonly_used_compound(cur):
    cur.execute(query_most_commonly_used_compound_sql)

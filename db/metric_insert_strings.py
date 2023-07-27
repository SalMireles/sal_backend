"""SQL metric inserts with psycopg param interpolation: (%s)"""

USER_METRIC_SQL = """
INSERT INTO UserMetric (user_id, metric_name, metric_result)
VALUES (
    (%s),
    (%s),
    (%s));
"""
GLOBAL_METRIC_SQL = """
INSERT INTO GlobalMetric (metric_name, metric_result)
VALUES (
    (%s),
    (%s));
"""

insert_total_user_experiments_sql = USER_METRIC_SQL
insert_average_experiments_per_user_sql = GLOBAL_METRIC_SQL
insert_most_commonly_used_compound_sql = GLOBAL_METRIC_SQL

"""SQL queries with psycopg param interpolation: (%s)"""


query_total_user_experiments_sql = """
SELECT COUNT(*) AS total_experiments
FROM Experiment
WHERE user_id = (%s);
"""

query_average_experiments_per_user_sql = """
SELECT AVG(experiment_count) AS average_experiments_per_user
FROM (
    SELECT COUNT(*) AS experiment_count
    FROM Experiment
    GROUP BY user_id
) AS subquery;
"""

query_most_commonly_used_compound_sql = """
SELECT compound_id, COUNT(*) AS compound_count
FROM ExperimentCompound
GROUP BY compound_id
ORDER BY compound_count DESC
LIMIT 1;
"""

from flask import Flask, render_template, jsonify, request, g
from db import init_db, metric_queries, metric_inserts

app = Flask(__name__)

init_db.init_schema()
# Load CSV files into the database
init_db.seed_db()


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, "psql_conn"):
        g.psql_conn.cursor().close()
        g.psql_conn.close()


def build_responses(query_results):
    for query_result in query_results:
        if query_result["status"] != "success":
            return jsonify({"status": 400, "data": query_result})
    return jsonify({"status": 200, "data": [q for q in query_results]})


@app.route("/")
def index():
    message = (
        "To trigger the pipline run `curl http://localhost:5000/etl-trigger`"
    )
    return render_template("index.html", message=message)


def etl():
    # Process files to derive features - make sql queries to get the data we want
    total_experiments_ran_response = (
        metric_queries.query_metrics_total_user_experiments(user_id=1)
    )
    average_experiments_per_user_response = (
        metric_queries.query_metrics_average_experiments_per_user()
    )
    most_commonly_used_compound_response = (
        metric_queries.query_metrics_most_commonly_used_compound()
    )
    # Upload processed data into a database
    total_experiments_ran = total_experiments_ran_response.get("data")
    average_experiments_per_user = average_experiments_per_user_response.get(
        "data"
    )
    most_commonly_used_compound = most_commonly_used_compound_response.get(
        "data"
    )
    response_1 = metric_inserts.insert_metrics_total_user_experiments(
        user_id=1,
        metric_name="total_experiments_ran",
        metric_result=int(total_experiments_ran),
    )
    response_2 = metric_inserts.insert_metrics_average_experiments_per_user(
        metric_name="average_experiments_per_user",
        metric_result=float(average_experiments_per_user),
    )
    response_3 = metric_inserts.insert_metrics_most_commonly_used_compound(
        metric_name="most_commonly_used_compound_id",
        metric_result=int(most_commonly_used_compound),
    )

    return build_responses([response_1, response_2, response_3])


@app.route("/etl-trigger")
def trigger_etl():
    # Trigger your ETL process here
    response = etl()
    return response


if __name__ == "__main__":
    etl()

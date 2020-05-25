import psycopg2.extras


def insert_webpage_metrics(connection, metrics, table):
    cursor = None

    insert_query = (
        "INSERT INTO {} "
        "(httpResponseTime, httpStatusCode, errorCode, patternFound) VALUES %s"
    ).format(table)

    rows = [
        (m.http_response_time, m.http_status_code, m.error_code, m.pattern_found)
        for m in metrics
    ]

    try:
        cursor = connection.cursor()
        psycopg2.extras.execute_values(cursor, insert_query, rows, page_size=1000)
    finally:
        if cursor:
            cursor.close()

from src.database.connection import get_connection


def start_pipeline_run(pipeline_name):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO metadata.pipeline_runs
        (
            pipeline_name,
            status
        )
        VALUES
        (
            %s,
            %s
        )
        RETURNING id;
        """,
        (
            pipeline_name,
            "RUNNING"
        )
    )

    run_id = cur.fetchone()[0]

    conn.commit()

    cur.close()
    conn.close()

    return run_id



def finish_pipeline_run(
    run_id,
    status,
    records_processed=None,
    error_message=None
):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE metadata.pipeline_runs
        SET
            finished_at = CURRENT_TIMESTAMP,
            status = %s,
            records_processed = %s,
            error_message = %s
        WHERE id = %s;
        """,
        (
            status,
            records_processed,
            error_message,
            run_id
        )
    )

    conn.commit()

    cur.close()
    conn.close()

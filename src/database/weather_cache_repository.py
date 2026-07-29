from src.database.connection import get_connection


def get_weather_cache(
    latitude,
    longitude,
    data,
    hora
):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT
            temperature_2m,
            precipitation,
            wind_speed_10m
        FROM silver.weather_cache
        WHERE latitude=%s
        AND longitude=%s
        AND data=%s
        AND hora=%s
        """,
        (
            latitude,
            longitude,
            data,
            hora
        )
    )


    result = cur.fetchone()

    cur.close()
    conn.close()

    if result:
        return {
            "temperature_2m": result[0],
            "precipitation": result[1],
            "wind_speed_10m": result[2]
        }

    return None



def save_weather_cache(
    latitude,
    longitude,
    data,
    hora,
    temperature,
    precipitation,
    wind
):

    conn = get_connection()
    cur = conn.cursor()


    cur.execute(
        """
        INSERT INTO silver.weather_cache
        (
            latitude,
            longitude,
            data,
            hora,
            temperature_2m,
            precipitation,
            wind_speed_10m
        )

        VALUES
        (%s,%s,%s,%s,%s,%s,%s)

        ON CONFLICT DO NOTHING
        """,
        (
            latitude,
            longitude,
            data,
            hora,
            temperature,
            precipitation,
            wind
        )
    )


    conn.commit()

    cur.close()
    conn.close()

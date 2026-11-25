import json
import os
import random
import time
from datetime import datetime, timezone
import snowflake.connector
from dotenv import load_dotenv

load_dotenv()

MARKETS = ["MUMBAI", "VASHI", "KALYAN", "THANE"]
STORAGE_ZONES = ["COLD_ROOM_A", "COLD_ROOM_B", "AMBIENT_SHED_1"]


def get_snowflake_connection():
    return snowflake.connector.connect(
        account=os.environ["SNOWFLAKE_ACCOUNT"],
        user=os.environ["SNOWFLAKE_USER"],
        password=os.environ["SNOWFLAKE_PASSWORD"],
        role="ACCOUNTADMIN",
        warehouse="COMPUTE_WH",
        database="ATMOSYNC_DB",
        schema="RAW",
    )


def generate_sensor_reading() -> dict:
    market = random.choice(MARKETS)
    zone = random.choice(STORAGE_ZONES)
    # Simulate occasional heat spikes in ambient sheds to trigger arbitrage alerts
    is_heat_spike = zone == "AMBIENT_SHED_1" and random.random() < 0.35
    temp_c = round(random.uniform(32.5, 38.0) if is_heat_spike else random.uniform(12.0, 26.0), 2)
    humidity_pct = round(random.uniform(75.0, 92.0) if is_heat_spike else random.uniform(55.0, 74.0), 2)

    return {
        "sensor_id": f"{market[:3]}_APMC_{random.randint(1, 5):02d}",
        "market": market,
        "recorded_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
        "temp_c": temp_c,
        "humidity_pct": humidity_pct,
        "storage_zone": zone,
    }


def stream_telemetry(interval_seconds: int = 15, max_events: int = 20):
    conn = get_snowflake_connection()
    cursor = conn.cursor()
    insert_sql = """
        INSERT INTO ATMOSYNC_DB.RAW.IOT_TELEMETRY (RAW_PAYLOAD)
        SELECT PARSE_JSON(%s)
    """
    try:
        for i in range(1, max_events + 1):
            payload = generate_sensor_reading()
            cursor.execute(insert_sql, (json.dumps(payload),))
            print(f"[{i}/{max_events}] Sent telemetry: {payload}")
            if i < max_events:
                time.sleep(interval_seconds)
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    stream_telemetry(interval_seconds=15, max_events=20)

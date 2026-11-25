# AtmoSync: Micro-Climate Arbitrage Analytics

**AtmoSync** is a real-time data engineering and analytics platform built on **Snowflake** that correlates wholesale agricultural commodity pricing (Mumbai APMC tomato markets) with live IoT storage micro-climate telemetry (temperature and humidity) to detect spoilage-driven price volatility and spatial arbitrage opportunities.

---

## Architecture Overview

* **Historical Market Pipeline:** `TOMATO DAILY MARKET PRICES MUMBAI (CSV File).csv` ➔ `RAW.TOMATO_PRICES` ➔ `ANALYTICS.TOMATO_MARKET_DAILY`
* **Real-Time IoT Pipeline:** Live JSON Sensor Telemetry ➔ `RAW.IOT_TELEMETRY` ➔ `IOT_TELEMETRY_STREAM` (CDC) ➔ `TASK_PROCESS_IOT_TELEMETRY` ➔ `ANALYTICS.IOT_MICROCLIMATE_CLEAN`
* **Unified Arbitrage Layer:** Both `ANALYTICS` tables join into `ANALYTICS.MARKET_ARBITRAGE_MICROCLIMATE` to flag `HIGH_HEAT_ARBITRAGE_RISK` and `HIGH_SPREAD_OPPORTUNITY` events.

---

## Repository Structure

* **`sql/01_snowflake_setup.sql`** — Initializes `COMPUTE_WH`, `ATMOSYNC_DB`, `RAW`, and `ANALYTICS`, and creates the base landing tables.
* **`sql/02_transform_tomato_prices.sql`** — Cleans historical market prices and computes `DAILY_PRICE_SPREAD` and `VOLATILITY_PCT`.
* **`sql/03_flatten_iot_telemetry.sql`** — Flattens semi-structured `VARIANT` JSON sensor payloads into typed columns.
* **`sql/04_market_arbitrage_view.sql`** — Joins market prices with sensor readings and computes arbitrage signals.
* **`sql/05_iot_stream_and_task.sql`** — Sets up the append-only CDC Stream and automated 1-minute Task.
* **`TOMATO DAILY MARKET PRICES MUMBAI (CSV File).csv`** — Historical Mumbai APMC tomato market dataset (3,517 rows).
* **`README.md`** — Project architecture and setup documentation.

---

## Setup & Execution Order

Run the SQL scripts in your Snowflake worksheet in strict numerical order:

1. **`sql/01_snowflake_setup.sql`** — Creates the warehouse, database, schemas, and `RAW` tables.
2. **Load Historical CSV** — Ingest `TOMATO DAILY MARKET PRICES MUMBAI (CSV File).csv` into `ATMOSYNC_DB.RAW.TOMATO_PRICES`.
3. **`sql/02_transform_tomato_prices.sql`** — Populates `ANALYTICS.TOMATO_MARKET_DAILY`.
4. **`sql/03_flatten_iot_telemetry.sql`** — Creates `ANALYTICS.IOT_MICROCLIMATE_CLEAN`.
5. **`sql/04_market_arbitrage_view.sql`** — Builds the `ANALYTICS.MARKET_ARBITRAGE_MICROCLIMATE` analytical view.
6. **`sql/05_iot_stream_and_task.sql`** — Activates `IOT_TELEMETRY_STREAM` and resumes `TASK_PROCESS_IOT_TELEMETRY`.

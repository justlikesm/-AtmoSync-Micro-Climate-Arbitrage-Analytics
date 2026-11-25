USE ROLE ACCOUNTADMIN;
USE WAREHOUSE COMPUTE_WH;

-- 1. Create the main project database
CREATE DATABASE IF NOT EXISTS ATMOSYNC_DB;
USE DATABASE ATMOSYNC_DB;

-- 2. Create two folders (schemas): RAW for untouched data, ANALYTICS for cleaned data
CREATE SCHEMA IF NOT EXISTS RAW;
CREATE SCHEMA IF NOT EXISTS ANALYTICS;

-- 3. Create Table 1 to hold your Mumbai Tomato Excel/CSV data (11 columns)
CREATE OR REPLACE TABLE ATMOSYNC_DB.RAW.TOMATO_PRICES (
    Arrival_Date DATE,
    Commodity STRING,
    Commodity_Code INT,
    District STRING,
    Grade STRING,
    Market STRING,
    Max_Price FLOAT,
    Min_Price FLOAT,
    Modal_Price FLOAT,
    State STRING,
    Variety STRING
);

-- 4. Create Table 2 to hold live JSON IoT sensor readings from Kafka
CREATE OR REPLACE TABLE ATMOSYNC_DB.RAW.IOT_TELEMETRY (
    RAW_PAYLOAD VARIANT,
    INGESTED_AT TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);IMESTAMP()
);

-- Creates the table for storing the transformed data
-- Run in terminal: psql -U postgres -d weather_analytics -f db/schema.sql

CREATE TABLE weather_data (
    weather_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    city VARCHAR(100) NOT NULL,
    temperature NUMERIC(5,2) NOT NULL,
    humidity INTEGER NOT NULL CHECK (humidity BETWEEN 0 AND 100),
    description VARCHAR(100) NOT NULL,
    observed_at TIMESTAMPTZ NOT NULL,
    loaded_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    -- UNIQUE prevents duplicate records with identical city and observation time,
    -- while allowing multiple cities with a shared observation time or multiple
    -- observation times for the same city
    UNIQUE (city, observed_at)
);

CREATE INDEX idx_weather_data_loaded_at ON weather_data (loaded_at DESC);
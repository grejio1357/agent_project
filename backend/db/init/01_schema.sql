CREATE TABLE agricultural_production (
    id SERIAL PRIMARY KEY,
    year INT NOT NULL,
    region VARCHAR(50) NOT NULL,
    crop VARCHAR(50) NOT NULL,
    cultivation_type VARCHAR(20),
    yield_kg_10a NUMERIC(8, 2),
    production_ton NUMERIC(12, 2)
)
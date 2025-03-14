-----------------object-------------------------------
CREATE TABLE object (
    object_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(50) NOT NULL, -- building, floor, room, device, etc.
    parent_id INTEGER REFERENCES object(object_id),
    location_details JSONB, -- flexible storage for address, coordinates, etc.
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    attributes JSONB -- for additional flexible attributes
);

-- Index for faster hierarchical queries
CREATE INDEX idx_object_parent_id ON object(parent_id);
CREATE INDEX idx_object_type ON object(type);


-----------------------datapoint--------------------------------
CREATE TABLE datapoint (
    datapoint_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    unit VARCHAR(50), -- e.g., "°C", "kWh", "m²"
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    value TEXT -- added as requested
);

-- Index for faster lookups
CREATE INDEX idx_datapoint_name ON datapoint(name);


-----------object_datapoint-----------------
CREATE TABLE object_datapoint (
    object_datapoint_id SERIAL PRIMARY KEY,
    object_id INTEGER REFERENCES object(object_id) ON DELETE CASCADE,
    datapoint_id INTEGER REFERENCES datapoint(datapoint_id) ON DELETE CASCADE,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_fresh BOOLEAN DEFAULT TRUE, -- flag for data freshness
    metadata JSONB, -- additional data like confidence scores, source information

    CONSTRAINT unique_object_datapoint UNIQUE (object_id, datapoint_id)
);

-- Indexes for faster queries
CREATE INDEX idx_od_object_id ON object_datapoint(object_id);
CREATE INDEX idx_od_datapoint_id ON object_datapoint(datapoint_id);
CREATE INDEX idx_od_last_updated ON object_datapoint(last_updated);
CREATE INDEX idx_od_is_fresh ON object_datapoint(is_fresh);
CREATE TABLE objects (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(50) NOT NULL CHECK (type IN ('building', 'floor', 'room', 'device')),
    location_details JSONB,
    parent_object_id BIGINT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_parent_object FOREIGN KEY (parent_object_id)
        REFERENCES objects(object_id) ON DELETE CASCADE
);


CREATE TABLE datapoints (
    datapoint_id BIGSERIAL PRIMARY KEY,
    object_FK BIGINT NOT NULL,
    value VARCHAR(255) NOT NULL,
    unit VARCHAR(50),
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT object_FK FOREIGN KEY (object_FK)
        REFERENCES objects(id) ON DELETE CASCADE
);

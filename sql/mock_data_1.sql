INSERT INTO objects (name, type, location_details, parent_object_id) VALUES
    -- Building (top-level)
    ('Grand Hotel', 'building', '{"lat": 40.7128, "lon": -74.0060, "address": "123 Main St"}', NULL),

    -- Floors (children of Grand Hotel, id = 1)
    ('Floor 1', 'floor', '{"number": 1}', 1),
    ('Floor 2', 'floor', '{"number": 2}', 1),

    -- Rooms (children of Floor 1, id = 2)
    ('Room 101', 'room', '{"number": "101", "size": "30m2"}', 2),
    ('Room 102', 'room', '{"number": "102", "size": "25m2"}', 2),

    -- Rooms (children of Floor 2, id = 3)
    ('Room 201', 'room', '{"number": "201", "size": "35m2"}', 3),

    -- Devices (children of Room 101, id = 4)
    ('Thermostat 101', 'device', '{"model": "Nest123", "serial": "T101"}', 4),
    ('Meter 101', 'device', '{"model": "E-MeterX", "serial": "M101"}', 4),

    -- Device (child of Room 201, id = 6)
    ('Thermostat 201', 'device', '{"model": "Nest123", "serial": "T201"}', 6);


INSERT INTO datapoints (object_FK, value, unit, timestamp) VALUES
    -- Datapoints for Room 101 (id = 4)
    (4, '23.5', 'Celsius', '2025-03-13 08:00:00+00'),  -- Room temperature
    (4, '45', '%', '2025-03-13 08:00:00+00'),          -- Room humidity

    -- Datapoints for Thermostat 101 (id = 7)
    (7, '24.0', 'Celsius', '2025-03-13 08:05:00+00'),  -- Thermostat setpoint

    -- Datapoints for Meter 101 (id = 8)
    (8, '120.5', 'kWh', '2025-03-13 08:00:00+00'),     -- Energy consumption
    (8, '118.0', 'kWh', '2025-03-12 08:00:00+00'),    -- Older energy reading

    -- Datapoints for Room 201 (id = 6)
    (6, '22.8', 'Celsius', '2025-03-13 08:00:00+00'),  -- Room temperature

    -- Datapoints for Thermostat 201 (id = 9)
    (9, '23.0', 'Celsius', '2025-03-13 08:05:00+00');  -- Thermostat setpo  -- Thermostat setpoint
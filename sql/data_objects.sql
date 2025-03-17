-- Truncate and reset id for table:
--TRUNCATE TABLE public."object" RESTART identity Cascade;

-- Insert multiple buildings (root level, parent_id = NULL)
INSERT INTO public."object" (name, type, parent_id, location_details) VALUES
('Grand Hotel', 'building', NULL, '{"address": "123 Main St, Cityville", "zipcode": "12345"}'),
('Ocean Resort', 'building', NULL, '{"address": "456 Beach Rd, Seaside", "zipcode": "67890"}'),
('Mountain Lodge', 'building', NULL, '{"address": "789 Hilltop Ln, Ridgeview", "zipcode": "54321"}');

-- Insert floors for Grand Hotel (parent_id = 1)
INSERT INTO public."object" (name, type, parent_id, location_details) VALUES
('Floor 1', 'floor', 1, '{"elevation": "0 meters", "description": "Ground floor with lobby"}'),
('Floor 2', 'floor', 1, '{"elevation": "5 meters", "description": "Guest rooms"}'),
('Floor 3', 'floor', 1, '{"elevation": "10 meters", "description": "Suites and conference rooms"}'),
('Floor 4', 'floor', 1, '{"elevation": "15 meters", "description": "Premium suites"}');

-- Insert floors for Ocean Resort (parent_id = 2)
INSERT INTO public."object" (name, type, parent_id, location_details) VALUES
('Floor 1', 'floor', 2, '{"elevation": "0 meters", "description": "Lobby and dining"}'),
('Floor 2', 'floor', 2, '{"elevation": "4 meters", "description": "Standard rooms"}'),
('Floor 3', 'floor', 2, '{"elevation": "8 meters", "description": "Ocean view rooms"}'),
('Floor 4', 'floor', 2, '{"elevation": "12 meters", "description": "Penthouse level"}');

-- Insert floors for Mountain Lodge (parent_id = 3)
INSERT INTO public."object" (name, type, parent_id, location_details) VALUES
('Floor 1', 'floor', 3, '{"elevation": "0 meters", "description": "Lobby and recreation"}'),
('Floor 2', 'floor', 3, '{"elevation": "6 meters", "description": "Cozy rooms"}'),
('Floor 3', 'floor', 3, '{"elevation": "12 meters", "description": "Luxury cabins"}');

-- Insert rooms for Grand Hotel floors
-- Floor 1 (parent_id = 4)
INSERT INTO public."object" (name, type, parent_id, location_details) VALUES
('Lobby', 'room', 4, '{"size": "200 sqm", "purpose": "reception area"}'),
('Restaurant', 'room', 4, '{"size": "150 sqm", "purpose": "dining area"}'),
('Gift Shop', 'room', 4, '{"size": "50 sqm", "purpose": "retail"}');
-- Floor 2 (parent_id = 5)
INSERT INTO public."object" (name, type, parent_id, location_details) VALUES
('Room 201', 'room', 5, '{"size": "30 sqm", "bed_type": "queen", "view": "city"}'),
('Room 202', 'room', 5, '{"size": "35 sqm", "bed_type": "king", "view": "garden"}'),
('Room 203', 'room', 5, '{"size": "32 sqm", "bed_type": "double", "view": "courtyard"}');
-- Floor 3 (parent_id = 6)
INSERT INTO public."object" (name, type, parent_id, location_details) VALUES
('Suite 301', 'room', 6, '{"size": "50 sqm", "bed_type": "king", "amenities": ["jacuzzi", "minibar"]}'),
('Conference Room A', 'room', 6, '{"size": "100 sqm", "capacity": 50, "equipment": ["projector", "whiteboard"]}'),
('Suite 302', 'room', 6, '{"size": "55 sqm", "bed_type": "king", "amenities": ["balcony", "minibar"]}');
-- Floor 4 (parent_id = 7)
INSERT INTO public."object" (name, type, parent_id, location_details) VALUES
('Penthouse 401', 'room', 7, '{"size": "80 sqm", "bed_type": "king", "amenities": ["terrace", "private lounge"]}'),
('Penthouse 402', 'room', 7, '{"size": "85 sqm", "bed_type": "king", "amenities": ["terrace", "jacuzzi"]}');

-- Insert rooms for Ocean Resort floors
-- Floor 1 (parent_id = 8)
INSERT INTO public."object" (name, type, parent_id, location_details) VALUES
('Lobby', 'room', 8, '{"size": "180 sqm", "purpose": "reception and lounge"}'),
('Beach Cafe', 'room', 8, '{"size": "120 sqm", "purpose": "casual dining"}');
-- Floor 2 (parent_id = 9)
INSERT INTO public."object" (name, type, parent_id, location_details) VALUES
('Room 201', 'room', 9, '{"size": "28 sqm", "bed_type": "queen", "view": "pool"}'),
('Room 202', 'room', 9, '{"size": "30 sqm", "bed_type": "double", "view": "garden"}'),
('Room 203', 'room', 9, '{"size": "29 sqm", "bed_type": "queen", "view": "pool"}');
-- Floor 3 (parent_id = 10)
INSERT INTO public."object" (name, type, parent_id, location_details) VALUES
('Room 301', 'room', 10, '{"size": "35 sqm", "bed_type": "king", "view": "ocean"}'),
('Room 302', 'room', 10, '{"size": "38 sqm", "bed_type": "king", "view": "ocean"}'),
('Room 303', 'room', 10, '{"size": "36 sqm", "bed_type": "queen", "view": "ocean"}');
-- Floor 4 (parent_id = 11)
INSERT INTO public."object" (name, type, parent_id, location_details) VALUES
('Penthouse 401', 'room', 11, '{"size": "90 sqm", "bed_type": "king", "amenities": ["ocean terrace", "private pool"]}');

-- Insert rooms for Mountain Lodge floors
-- Floor 1 (parent_id = 12)
INSERT INTO public."object" (name, type, parent_id, location_details) VALUES
('Lobby', 'room', 12, '{"size": "160 sqm", "purpose": "reception and fireplace lounge"}'),
('Rec Room', 'room', 12, '{"size": "80 sqm", "purpose": "games and entertainment"}');
-- Floor 2 (parent_id = 13)
INSERT INTO public."object" (name, type, parent_id, location_details) VALUES
('Room 201', 'room', 13, '{"size": "25 sqm", "bed_type": "queen", "view": "forest"}'),
('Room 202', 'room', 13, '{"size": "27 sqm", "bed_type": "double", "view": "mountain"}');
-- Floor 3 (parent_id = 14)
INSERT INTO public."object" (name, type, parent_id, location_details) VALUES
('Cabin 301', 'room', 14, '{"size": "40 sqm", "bed_type": "king", "amenities": ["fireplace", "balcony"]}'),
('Cabin 302', 'room', 14, '{"size": "45 sqm", "bed_type": "king", "amenities": ["fireplace", "hot tub"]}');

-- Insert devices across various rooms
INSERT INTO public."object" (name, type, parent_id, location_details) VALUES
('HVAC Unit - GH Lobby', 'hvac', 15, '{"model": "ACME-123", "power": "5kW", "status": "active"}'),
('Meter - GH Restaurant', 'meter', 16, '{"type": "electricity", "reading": 4500, "unit": "kWh"}'),
('HVAC Unit - Room 201 GH', 'hvac', 18, '{"model": "ACME-200", "power": "3kW", "status": "active"}'),
('HVAC Unit - Suite 301 GH', 'hvac', 21, '{"model": "ACME-300", "power": "4kW", "status": "standby"}'),
('HVAC Unit - OR Lobby', 'hvac', 26, '{"model": "ACME-150", "power": "6kW", "status": "active"}'),
('Meter - OR Beach Cafe', 'meter', 27, '{"type": "water", "reading": 1200, "unit": "liters"}'),
('HVAC Unit - Room 301 OR', 'hvac', 31, '{"model": "ACME-250", "power": "3.5kW", "status": "active"}'),
('HVAC Unit - ML Lobby', 'hvac', 36, '{"model": "ACME-180", "power": "5.5kW", "status": "active"}'),
('Meter - ML Rec Room', 'meter', 37, '{"type": "electricity", "reading": 3200, "unit": "kWh"}'),
('HVAC Unit - Cabin 301 ML', 'hvac', 39, '{"model": "ACME-220", "power": "4kW", "status": "standby"}');
-- Truncate and reset id for table:
--TRUNCATE TABLE public."datapoint" RESTART identity Cascade;

INSERT INTO public.datapoint (name, value, unit, created_at, updated_at, is_fresh, type) VALUES
-- Temperature-related datapoints
('Temperature', '22.5', 'Celsius', '2025-03-16 08:00:00+00', '2025-03-16 08:00:00+00', true, 'temperature'),
('Temperature', '23.0', 'Celsius', '2025-03-16 08:05:00+00', '2025-03-16 08:05:00+00', true, 'temperature'),
('Temperature', '21.8', 'Celsius', '2025-03-16 08:10:00+00', '2025-03-16 08:10:00+00', true, 'temperature'),
('Temperature', '24.2', 'Celsius', '2025-03-16 08:15:00+00', '2025-03-16 08:15:00+00', true, 'temperature'),
('Temperature', '19.5', 'Celsius', '2025-03-16 08:20:00+00', '2025-03-16 08:20:00+00', true, 'temperature'),
-- Humidity-related datapoints
('Humidity', '45', '%', '2025-03-16 08:00:00+00', '2025-03-16 08:00:00+00', true, 'humidity'),
('Humidity', '50', '%', '2025-03-16 08:05:00+00', '2025-03-16 08:05:00+00', true, 'humidity'),
('Humidity', '42', '%', '2025-03-16 08:10:00+00', '2025-03-16 08:10:00+00', true, 'humidity'),
-- Power consumption datapoints (for HVAC units)
('Power Consumption', '4.8', 'kW', '2025-03-16 08:00:00+00', '2025-03-16 08:00:00+00', true, 'powerConsumption'),
('Power Consumption', '3.2', 'kW', '2025-03-16 08:05:00+00', '2025-03-16 08:05:00+00', true, 'powerConsumption'),
('Power Consumption', '5.1', 'kW', '2025-03-16 08:10:00+00', '2025-03-16 08:10:00+00', true, 'powerConsumption'),
-- Energy usage datapoints (for meters)
('Energy Usage', '4550', 'kWh', '2025-03-16 08:00:00+00', '2025-03-16 08:00:00+00', true, 'energyUsage'),
('Energy Usage', '1200', 'liters', '2025-03-16 08:05:00+00', '2025-03-16 08:05:00+00', true, 'energyUsage'),
('Energy Usage', '3250', 'kWh', '2025-03-16 08:10:00+00', '2025-03-16 08:10:00+00', true, 'energyUsage'),
-- Miscellaneous datapoints
('CO2 Level', '400', 'ppm', '2025-03-16 08:00:00+00', '2025-03-16 08:00:00+00', true, 'co2Level'),
('Occupancy', '1', 'people', '2025-03-16 08:05:00+00', '2025-03-16 08:05:00+00', true, 'occupancy');


INSERT INTO public.object_datapoint ("object_FK", "datapoint_FK", "last_updated") VALUES
(15, 1, '2025-03-16 08:00:00'),  -- Lobby (GH) -> Temperature: 22.5°C
(15, 6, '2025-03-16 08:00:00'),  -- Lobby (GH) -> Humidity: 45%
(18, 2, '2025-03-16 08:05:00'),  -- Room 201 (GH) -> Temperature: 23.0°C
(18, 7, '2025-03-16 08:05:00'),  -- Room 201 (GH) -> Humidity: 50%
(21, 3, '2025-03-16 08:10:00'),  -- Suite 301 (GH) -> Temperature: 21.8°C
(21, 15, '2025-03-16 08:00:00'), -- Suite 301 (GH) -> CO2 Level: 400 ppm
(38, 9, '2025-03-16 08:00:00'),  -- HVAC Unit - GH Lobby -> Power Consumption: 4.8 kW
(39, 12, '2025-03-16 08:00:00'), -- Meter - GH Restaurant -> Energy Usage: 4550 kWh
(40, 10, '2025-03-16 08:05:00'), -- HVAC Unit - Room 201 GH -> Power Consumption: 3.2 kW
(41, 11, '2025-03-16 08:10:00'), -- HVAC Unit - Suite 301 GH -> Power Consumption: 5.1 kW

-- Ocean Resort objects
(26, 4, '2025-03-16 08:15:00'),  -- Lobby (OR) -> Temperature: 24.2°C
(26, 8, '2025-03-16 08:10:00'),  -- Lobby (OR) -> Humidity: 42%
(31, 5, '2025-03-16 08:20:00'),  -- Room 301 (OR) -> Temperature: 19.5°C
(31, 16, '2025-03-16 08:05:00'), -- Room 301 (OR) -> Occupancy: 1 person
(42, 9, '2025-03-16 08:00:00'),  -- HVAC Unit - OR Lobby -> Power Consumption: 4.8 kW
(43, 13, '2025-03-16 08:05:00'), -- Meter - OR Beach Cafe -> Energy Usage: 1200 liters
(44, 10, '2025-03-16 08:05:00'), -- HVAC Unit - Room 301 OR -> Power Consumption: 3.2 kW

-- Mountain Lodge objects
(36, 1, '2025-03-16 08:00:00'),  -- Lobby (ML) -> Temperature: 22.5°C
(36, 6, '2025-03-16 08:00:00'),  -- Lobby (ML) -> Humidity: 45%
(39, 2, '2025-03-16 08:05:00'),  -- Cabin 301 (ML) -> Temperature: 23.0°C
(45, 11, '2025-03-16 08:10:00'), -- HVAC Unit - ML Lobby -> Power Consumption: 5.1 kW
(46, 14, '2025-03-16 08:10:00'), -- Meter - ML Rec Room -> Energy Usage: 3250 kWh
(47, 10, '2025-03-16 08:05:00'); -- HVAC Unit - Cabin 301 ML -> Power Consumption: 3.2 kW



INSERT INTO public.datapoint (name, value, unit, created_at, updated_at, is_fresh, type) VALUES
-- Building-specific datapoints
('Solar Energy Consumption', '2500', 'kWh', '2025-03-16 08:00:00+00', '2025-03-16 08:00:00+00', true, 'solarEnergyConsumption'), -- Grand Hotel
('Solar Energy Consumption', '1800', 'kWh', '2025-03-16 08:05:00+00', '2025-03-16 08:05:00+00', true, 'solarEnergyConsumption'), -- Ocean Resort
('Solar Energy Consumption', '1200', 'kWh', '2025-03-16 08:10:00+00', '2025-03-16 08:10:00+00', true, 'solarEnergyConsumption'), -- Mountain Lodge
('HVAC Efficiency', '85', '%', '2025-03-16 08:00:00+00', '2025-03-16 08:00:00+00', true, 'hvacEfficiency'),                  -- Grand Hotel
('HVAC Efficiency', '90', '%', '2025-03-16 08:05:00+00', '2025-03-16 08:05:00+00', true, 'hvacEfficiency'),                  -- Ocean Resort
('HVAC Efficiency', '78', '%', '2025-03-16 08:10:00+00', '2025-03-16 08:10:00+00', true, 'hvacEfficiency'),                  -- Mountain Lodge
('Structural Load', '1500', 'tons', '2025-03-16 08:00:00+00', '2025-03-16 08:00:00+00', true, 'structuralLoad'),             -- Grand Hotel
('Structural Load', '1200', 'tons', '2025-03-16 08:05:00+00', '2025-03-16 08:05:00+00', true, 'structuralLoad'),             -- Ocean Resort
('Structural Load', '900', 'tons', '2025-03-16 08:10:00+00', '2025-03-16 08:10:00+00', true, 'structuralLoad'),              -- Mountain Lodge

-- Floor-specific datapoints (for Grand Hotel floors)
('Communal Taps Water Consumption', '500', 'liters', '2025-03-16 08:00:00+00', '2025-03-16 08:00:00+00', true, 'communalTapsWaterConsumption'), -- Floor 1 GH
('Communal Taps Water Consumption', '450', 'liters', '2025-03-16 08:05:00+00', '2025-03-16 08:05:00+00', true, 'communalTapsWaterConsumption'), -- Floor 2 GH
('Communal Taps Water Consumption', '600', 'liters', '2025-03-16 08:10:00+00', '2025-03-16 08:10:00+00', true, 'communalTapsWaterConsumption'), -- Floor 3 GH
('Lighting Energy Usage', '800', 'kWh', '2025-03-16 08:00:00+00', '2025-03-16 08:00:00+00', true, 'lightingEnergyUsage'),                     -- Floor 1 GH
('Lighting Energy Usage', '650', 'kWh', '2025-03-16 08:05:00+00', '2025-03-16 08:05:00+00', true, 'lightingEnergyUsage'),                     -- Floor 2 GH
('Lighting Energy Usage', '900', 'kWh', '2025-03-16 08:10:00+00', '2025-03-16 08:10:00+00', true, 'lightingEnergyUsage'),                     -- Floor 3 GH
('Noise Level', '45', 'dB', '2025-03-16 08:00:00+00', '2025-03-16 08:00:00+00', true, 'noiseLevel'),                                       -- Floor 1 GH
('Noise Level', '50', 'dB', '2025-03-16 08:05:00+00', '2025-03-16 08:05:00+00', true, 'noiseLevel'),                                       -- Floor 2 GH
('Noise Level', '40', 'dB', '2025-03-16 08:10:00+00', '2025-03-16 08:10:00+00', true, 'noiseLevel');                                       -- Floor 3 GH

INSERT INTO public.object_datapoint ("object_FK", "datapoint_FK", last_updated) VALUES
-- Buildings
(1, 17, '2025-03-16 08:00:00'),  -- Grand Hotel -> Solar Energy Consumption: 2500 kWh
(2, 18, '2025-03-16 08:05:00'),  -- Ocean Resort -> Solar Energy Consumption: 1800 kWh
(3, 19, '2025-03-16 08:10:00'),  -- Mountain Lodge -> Solar Energy Consumption: 1200 kWh
(1, 20, '2025-03-16 08:00:00'),  -- Grand Hotel -> HVAC Efficiency: 85%
(2, 21, '2025-03-16 08:05:00'),  -- Ocean Resort -> HVAC Efficiency: 90%
(3, 22, '2025-03-16 08:10:00'),  -- Mountain Lodge -> HVAC Efficiency: 78%
(1, 23, '2025-03-16 08:00:00'),  -- Grand Hotel -> Structural Load: 1500 tons
(2, 24, '2025-03-16 08:05:00'),  -- Ocean Resort -> Structural Load: 1200 tons
(3, 25, '2025-03-16 08:10:00'),  -- Mountain Lodge -> Structural Load: 900 tons

-- Floors (Grand Hotel)
(4, 26, '2025-03-16 08:00:00'),  -- Floor 1 GH -> Communal Taps Water Consumption: 500 liters
(5, 27, '2025-03-16 08:05:00'),  -- Floor 2 GH -> Communal Taps Water Consumption: 450 liters
(6, 28, '2025-03-16 08:10:00'),  -- Floor 3 GH -> Communal Taps Water Consumption: 600 liters
(4, 29, '2025-03-16 08:00:00'),  -- Floor 1 GH -> Lighting Energy Usage: 800 kWh
(5, 30, '2025-03-16 08:05:00'),  -- Floor 2 GH -> Lighting Energy Usage: 650 kWh
(6, 31, '2025-03-16 08:10:00'),  -- Floor 3 GH -> Lighting Energy Usage: 900 kWh
(4, 32, '2025-03-16 08:00:00'),  -- Floor 1 GH -> Noise Level: 45 dB
(5, 33, '2025-03-16 08:05:00'),  -- Floor 2 GH -> Noise Level: 50 dB
(6, 34, '2025-03-16 08:10:00');  -- Floor 3 GH -> Noise Level: 40 dB

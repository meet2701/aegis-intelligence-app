-- populate.sql
-- Project Phase 4: Aegis Intelligence Database (AID)
-- Data Source: One Piece Wiki (CP0, Marines, Pirates, Arcs)

-- Note: Make sure to run schema.sql first to create the database structure
USE mini_world_db;

-- Disable FK checks temporarily to allow insertion in any order if needed
-- SET FOREIGN_KEY_CHECKS = 0;

-- =========================================
-- 1. Reference Data (Regions, Events, Fruits)
-- =========================================

INSERT INTO Sea_Region (Region_Name, Threat_Level) VALUES 
('East Blue', 'Low'),
('Grand Line - Paradise', 'High'),
('New World', 'Extreme'),
('West Blue', 'Medium'),
('South Blue', 'Medium'),
('North Blue', 'Medium');

INSERT INTO Event (Event_Name, Start_Date, End_Date) VALUES 
('Summit War of Marineford', '1522-01-01', '1522-01-05'),
('Raid on Onigashima', '1524-05-10', '1524-05-11'),
('Egghead Incident', '1524-06-01', NULL),
('Dressrosa Arc', '1523-08-01', '1523-09-15'),
('Whole Cake Island Arc', '1523-11-01', '1523-12-20');

INSERT INTO Devil_Fruit (Fruit_Name, Type, Description, is_Awakened) VALUES 
('Hito Hito no Mi, Model: Nika', 'Zoan', 'Grants the user the properties of rubber and the power of the Sun God.', TRUE),
('Magu Magu no Mi', 'Logia', 'Allows the user to create, control, and transform into magma.', FALSE),
('Ope Ope no Mi', 'Paramecia', 'Allows the user to create a spherical space or "room" to manipulate anything inside.', TRUE),
('Pika Pika no Mi', 'Logia', 'Allows the user to create, control, and transform into light.', FALSE),
('Neko Neko no Mi, Model: Leopard', 'Zoan', 'Allows the user to transform into a leopard hybrid.', TRUE),
('Uo Uo no Mi, Model: Seiryu', 'Zoan', 'Allows the user to transform into a giant azure dragon.', FALSE),
('Moku Moku no Mi', 'Logia', 'Allows the user to create, control, and transform into smoke.', FALSE),
('Hana Hana no Mi', 'Paramecia', 'Allows the user to sprout replicas of their body parts on any surface.', FALSE),
('Yomi Yomi no Mi', 'Paramecia', 'Grants second life and allows user to interact with souls.', FALSE),
('Mera Mera no Mi', 'Logia', 'Allows the user to create, control, and transform into fire.', FALSE),
('Soru Soru no Mi', 'Paramecia', 'Allows user to manipulate souls and create homies.', TRUE),
('Mochi Mochi no Mi', 'Paramecia', 'Allows user to create, control and transform into mochi.', TRUE),
('Ryu Ryu no Mi, Model: Pteranodon', 'Zoan', 'Ancient Zoan allowing transformation into pteranodon.', FALSE),
('Ryu Ryu no Mi, Model: Brachiosaurus', 'Zoan', 'Ancient Zoan allowing transformation into brachiosaurus.', FALSE),
('Zou Zou no Mi, Model: Mammoth', 'Zoan', 'Ancient Zoan allowing transformation into mammoth.', FALSE),
('Ito Ito no Mi', 'Paramecia', 'Allows user to create and manipulate strings.', TRUE),
('Tori Tori no Mi, Model: Phoenix', 'Zoan', 'Mythical Zoan allowing transformation into phoenix with regeneration.', TRUE),
('Jiki Jiki no Mi', 'Paramecia', 'Allows user to manipulate magnetic forces.', FALSE),
('Toshi Toshi no Mi', 'Paramecia', 'Allows user to manipulate age of themselves and others.', FALSE);

-- =========================================
-- 2. Locations (Islands)
-- =========================================

INSERT INTO Island (Island_Name, Climate, Population, Latitude, Longitude, Region_ID) VALUES 
('Dawn Island', 'Tropical', 10000, 10.500000, 45.300000, 1),    -- East Blue
('Marineford', 'Temperate', 50000, 35.200000, 139.600000, 2),   -- Paradise
('Wano Country', 'Variable', 200000, 40.700000, -74.000000, 3), -- New World
('Egghead', 'Winter', 5000, 65.100000, -18.500000, 3),          -- New World
('Whole Cake Island', 'Tropical', 150000, 25.000000, 70.000000, 3), -- New World
('Loguetown', 'Temperate', 100000, 31.200000, 62.700000, 1),    -- East Blue
('Dressrosa', 'Tropical', 2500000, 11.200000, -150.700000, 3),  -- New World
('Elbaf', 'Temperate', 500000, 40.000000, -79.200000, 3),       -- New World
('Little Garden', 'Prehistoric Jungle', 5, 5.200000, 16.700000, 2), -- Paradise
('Cocoyasi Village', 'Tropical', 8000, 12.300000, 47.100000, 1), -- East Blue (Nami's home)
('Syrup Village', 'Temperate', 15000, 13.100000, 48.200000, 1), -- East Blue (Usopp's home)
('Lvneel', 'Temperate', 30000, 22.400000, -65.300000, 6),       -- North Blue (Noland's kingdom)
('Flevance', 'Temperate', 80000, 20.100000, -62.800000, 6),     -- North Blue (White City, Law's home)
('Spider Miles', 'Temperate', 45000, 21.500000, -64.200000, 6), -- North Blue (Infamous island)
('Baterilla', 'Tropical', 12000, -8.300000, 35.700000, 5),      -- South Blue (Ace's birthplace)
('Karate Island', 'Temperate', 25000, -10.100000, 38.200000, 5), -- South Blue (Martial arts hub)
('Toroa', 'Tropical', 20000, -9.500000, 36.900000, 5),          -- South Blue
('Ohara', 'Temperate', 50000, 15.200000, -80.100000, 4),        -- West Blue (Robin's home, destroyed)
('Ilusia Kingdom', 'Temperate', 120000, 18.700000, -85.300000, 4), -- West Blue (Revolutionary Army activity)
('Kano Country', 'Temperate', 90000, 17.400000, -82.600000, 4); -- West Blue

-- =========================================
-- 3. Persons (Base Table)
-- =========================================

INSERT INTO Person (First_Name, Last_Name, Date_of_Birth, Status, Home_Island_ID) VALUES 
('Monkey D.', 'Luffy', '2005-05-05', 'Active', 1),          -- ID 1
('Roronoa', 'Zoro', '2003-11-11', 'Active', 1),             -- ID 2
('Sakazuki', NULL, '1969-08-16', 'Active', 2),              -- ID 3 (Akainu - Fleet Admiral)
('Trafalgar D. Water', 'Law', '1998-10-06', 'Active', 2),   -- ID 4
('Kaido', NULL, '1960-05-01', 'Deceased', 3),               -- ID 5
('Rob', 'Lucci', '1994-06-02', 'Active', 2),                -- ID 6 (CP0)
('Borsalino', NULL, '1966-11-23', 'Active', 2),             -- ID 7 (Kizaru - Admiral)
('Stussy', NULL, '1980-01-01', 'Active', 4),                -- ID 8 (CP0/Clone)
('Vegapunk', NULL, '1958-01-01', 'Deceased', 4),            -- ID 9 (Civilian/Scientist)
('Smoker', NULL, '1981-03-14', 'Active', 6),                -- ID 10 (Vice Admiral)
('Vinsmoke', 'Sanji', '1999-03-02', 'Active', 5),           -- ID 11
('Eustass', 'Kid', '1997-01-10', 'Active', 6),              -- ID 12
('X', 'Drake', '1990-10-24', 'Active', 2),                  -- ID 13
('Nami', NULL, '2002-07-03', 'Active', 1),                  -- ID 14
('Nico', 'Robin', '1994-02-06', 'Active', 7),               -- ID 15
('Franky', NULL, '1988-03-09', 'Active', 2),                -- ID 16
('Charlotte', 'Linlin', '1948-02-15', 'Active', 5),         -- ID 17 (Big Mom)
('Charlotte', 'Katakuri', '1979-11-25', 'Active', 5),       -- ID 18
('King', NULL, '1970-12-01', 'Captured', 3),                -- ID 19
('Queen', NULL, '1965-07-13', 'Captured', 3),               -- ID 20
('Jack', NULL, '1990-09-28', 'Captured', 3),                -- ID 21
('Gol D.', 'Roger', '1476-12-31', 'Deceased', 6),           -- ID 22
('Shanks', NULL, '1981-03-09', 'Active', 1),                -- ID 23
('Marco', NULL, '1975-10-05', 'Active', 2),                 -- ID 24
('Monkey D.', 'Garp', '1956-05-02', 'Active', 1),           -- ID 25
('Monkey D.', 'Dragon', '1959-10-05', 'Active', 1),         -- ID 26
('Sabo', NULL, '2007-03-20', 'Active', 1),                  -- ID 27
('Portgas D.', 'Ace', '2000-01-01', 'Deceased', 1),         -- ID 28
('Koby', NULL, '2005-05-13', 'Active', 1),                  -- ID 29
('Brook', NULL, '1935-04-03', 'Active', 1),                 -- ID 30
('Usopp', NULL, '2003-04-01', 'Active', 1),                 -- ID 31
('Jinbe', NULL, '1976-04-02', 'Active', 2),                 -- ID 32
('Donquixote', 'Doflamingo', '1983-10-23', 'Captured', 7),  -- ID 33
('S-Hawk', NULL, '2024-01-01', 'Active', 4),                -- ID 34 (Seraphim)
('Jaygarcia', 'Saturn', '1700-01-01', 'Active', 2),         -- ID 35 (Gorosei 1)
('Marcus', 'Mars', '1695-01-01', 'Active', 2),              -- ID 36 (Gorosei 2)
('Topman', 'Warcury', '1690-01-01', 'Active', 2),           -- ID 37 (Gorosei 3)
('Ethanbaron V.', 'Nusjuro', '1685-01-01', 'Active', 2),    -- ID 38 (Gorosei 4)
('Shepherd Ju', 'Peter', '1680-01-01', 'Active', 2),        -- ID 39 (Gorosei 5)
('Jewelry', 'Bonney', '2008-09-01', 'Active', 5),           -- ID 40
-- New additions from Four Blues
('Bellemere', NULL, '1980-04-03', 'Deceased', 10),          -- ID 41 (Nami's adoptive mother, Cocoyasi)
('Arlong', NULL, '1978-05-03', 'Captured', 10),             -- ID 42 (Fish-man pirate, terrorized Cocoyasi)
('Kaya', NULL, '2001-08-24', 'Active', 11),                 -- ID 43 (Syrup Village heiress)
('Merry', NULL, '1965-03-10', 'Deceased', 11),              -- ID 44 (Kaya's butler)
('Montblanc', 'Noland', '1050-01-01', 'Deceased', 12),      -- ID 45 (Explorer from Lvneel)
('Lami', NULL, '2004-09-08', 'Deceased', 13),               -- ID 46 (Law's sister, Flevance)
('Corazon', NULL, '1983-07-15', 'Deceased', 13),            -- ID 47 (Donquixote Rosinante, saved Law)
('Diez', 'Barrels', '1960-04-12', 'Deceased', 14),          -- ID 48 (Former Marine, Spider Miles)
('Rouge', NULL, '1982-01-01', 'Deceased', 15),              -- ID 49 (Ace's mother, Baterilla)
('Hack', NULL, '1985-06-09', 'Active', 16),                 -- ID 50 (Fish-man martial artist, Karate Island)
('Koala', NULL, '1998-02-23', 'Active', 16),                -- ID 51 (Revolutionary Army, trained on Karate Island)
('Boa', 'Hancock', '1995-09-02', 'Active', 17),             -- ID 52 (Pirate Empress, originally from South Blue)
('Nico', 'Olvia', '1969-02-06', 'Deceased', 18),            -- ID 53 (Robin's mother, Ohara)
('Professor', 'Clover', '1935-02-05', 'Deceased', 18),      -- ID 54 (Ohara scholar)
('Sai', NULL, '1995-08-13', 'Active', 20),                  -- ID 55 (Happo Navy leader, Kano Country)
('Chinjao', 'Don', '1940-09-30', 'Active', 20),             -- ID 56 (Former Happo Navy Don, Kano Country)
('Stelly', NULL, '2007-03-05', 'Active', 19);               -- ID 57 (King of Goa Kingdom, Ilusia ties)

-- =========================================
-- 4. Subclasses & Attributes
-- =========================================

-- Pirates
INSERT INTO Pirate (Person_ID, Infamy_Level) VALUES 
(1, 'Emperor of the Sea'),
(2, 'Supernova'),
(4, 'Warlord (Former)'),
(5, 'Emperor (Former)'),
(11, 'Supernova'),           -- Sanji
(12, 'Supernova'),           -- Kid
(13, 'Supernova'),           -- X Drake
(14, 'Notorious'),           -- Nami
(15, 'Most Wanted'),         -- Robin
(16, 'Notorious'),           -- Franky
(17, 'Emperor'),             -- Big Mom
(18, 'Sweet Commander'),     -- Katakuri
(19, 'All-Star'),            -- King
(20, 'All-Star'),            -- Queen
(21, 'All-Star'),            -- Jack
(22, 'Pirate King'),         -- Roger
(23, 'Emperor'),             -- Shanks
(24, 'Emperor Commander'),   -- Marco
(28, 'Division Commander'),  -- Ace
(30, 'Soul King'),           -- Brook
(31, 'Regional Menace'),     -- Usopp
(32, 'Warlord (Former)'),    -- Jinbe
(33, 'Warlord (Former)'),    -- Doflamingo
(40, 'Supernova'),           -- Bonney
(42, 'Regional Menace'),     -- Arlong
(45, 'Explorer'),            -- Noland
(52, 'Warlord'),             -- Boa Hancock
(55, 'Regional Menace'),     -- Sai
(56, 'Legendary');           -- Don Chinjao

-- Marines / CP0 (Mapped as Officers for system simplicity)
INSERT INTO Marine_Officer (Person_ID, `Rank`, Service_Number) VALUES 
(3, 'Fleet Admiral', 'MA-001'),
(6, 'CP0 Masked Agent', 'CP-099'),
(7, 'Admiral', 'MA-003'),
(8, 'CP0 Agent', 'CP-102'),
(10, 'Vice Admiral', 'M-008'),       -- Smoker
(25, 'Vice Admiral', 'M-002'),       -- Garp
(29, 'Captain', 'M-011'),            -- Koby
(34, 'Special Weapon', 'S-001'),     -- Seraphim S-Hawk
(41, 'Lieutenant', 'M-034'),         -- Bellemere
(47, 'Commander', 'M-019'),          -- Corazon (undercover)
(48, 'Commodore (Former)', 'M-025'), -- Diez Barrels
(50, 'Revolutionary Ally', 'RA-008'), -- Hack
(51, 'Revolutionary', 'RA-012');     -- Koala

-- Civilians
INSERT INTO Civilian (Person_ID, Occupation) VALUES 
(9, 'Head Scientist'),
(26, 'Revolutionary Leader'),          -- Dragon
(27, 'Revolutionary Chief of Staff'),  -- Sabo
(35, 'Gorosei - Warrior God of Science'),    -- Saturn
(36, 'Gorosei - Warrior God of Environment'), -- Mars
(37, 'Gorosei - Warrior God of Justice'),     -- Warcury
(38, 'Gorosei - Warrior God of Finance'),     -- Nusjuro
(39, 'Gorosei - Warrior God of Agriculture'), -- Peter
(43, 'Heiress'),                       -- Kaya
(44, 'Butler'),                        -- Merry
(46, 'Student'),                       -- Lami
(49, 'Mother'),                        -- Rouge
(53, 'Archaeologist'),                 -- Olvia
(54, 'Professor'),                     -- Clover
(57, 'King');                          -- Stelly

-- Person Abilities
INSERT INTO Person_Abilities (Person_ID, Ability) VALUES 
(1, 'Conquerors Haki'), (1, 'Armament Haki'), (1, 'Observation Haki'),
(2, 'Santoryu'), (2, 'Armament Haki'), (2, 'Conquerors Haki'),
(3, 'Magma Manipulation'), (3, 'Absolute Justice'),
(4, 'Swordsmanship'), (4, 'Medical Knowledge'),
(6, 'Rokushiki'), (6, 'Armament Haki'),
(10, 'Smoke Manipulation'), (10, 'Armament Haki'),  -- Smoker
(11, 'Black Leg Style'), (11, 'Observation Haki'), (11, 'Armament Haki'), -- Sanji
(12, 'Magnetic Manipulation'), (12, 'Conquerors Haki'), -- Kid
(13, 'X Caliber'), (13, 'Armament Haki'),            -- X Drake
(14, 'Clima-Tact'), (14, 'Zeus'),                    -- Nami
(15, 'Archaeologist'), (15, 'Armament Haki'),        -- Robin
(16, 'Cyborg Enhancements'), (16, 'Franky Shogun'),  -- Franky
(17, 'Conquerors Haki'), (17, 'Armament Haki'), (17, 'Observation Haki'), -- Big Mom
(18, 'Conquerors Haki'), (18, 'Future Sight'),       -- Katakuri
(19, 'Ancient Zoan'), (19, 'Fire Manipulation'),     -- King
(20, 'Ancient Zoan'), (20, 'Plague Manipulation'),   -- Queen
(21, 'Ancient Zoan'), (21, 'Armament Haki'),         -- Jack
(22, 'Conquerors Haki'), (22, 'Voice of All Things'), (22, 'Supreme Swordsmanship'), -- Roger
(23, 'Conquerors Haki'), (23, 'Supreme Swordsmanship'), -- Shanks
(24, 'Regeneration'), (24, 'Flight'),                -- Marco
(25, 'Conquerors Haki'), (25, 'Fist of Love'),       -- Garp
(26, 'Wind Manipulation'), (26, 'Conquerors Haki'),  -- Dragon
(27, 'Dragon Claw'), (27, 'Armament Haki'),          -- Sabo
(28, 'Fire Manipulation'), (28, 'Conquerors Haki'),  -- Ace
(29, 'Observation Haki'), (29, 'Armament Haki'),     -- Koby
(30, 'Soul Solid'), (30, 'Music Swordsmanship'),     -- Brook
(31, 'Marksmanship'), (31, 'Observation Haki'),      -- Usopp
(32, 'Fish-Man Karate'), (32, 'Armament Haki'),      -- Jinbe
(33, 'String Manipulation'), (33, 'Conquerors Haki'), -- Doflamingo
(34, 'Laser Beams'), (34, 'Lunarian DNA'),           -- S-Hawk
(40, 'Age Manipulation'),                             -- Bonney
(41, 'Marksmanship'), (41, 'Tactical Leadership'),   -- Bellemere
(42, 'Fish-Man Karate'), (42, 'Saw Nose'),           -- Arlong
(45, 'Navigation'), (45, 'Botany'),                  -- Noland
(47, 'Calm Calm Fruit'), (47, 'Undercover Skills'),  -- Corazon
(50, 'Fish-Man Karate'), (50, 'Armament Haki'),      -- Hack
(51, 'Fish-Man Karate'), (51, 'Navigation'),         -- Koala
(52, 'Conquerors Haki'), (52, 'Armament Haki'), (52, 'Mero Mero Powers'), -- Hancock
(53, 'Archaeology'), (53, 'Scholar'),                -- Olvia
(54, 'Ancient Knowledge'), (54, 'Poneglyph Reading'), -- Clover
(55, 'Hasshoken'), (55, 'Armament Haki'),            -- Sai
(56, 'Hasshoken'), (56, 'Conquerors Haki'), (56, 'Drill Head'); -- Don Chinjao

-- Devil Fruit Possession (1:1)
INSERT INTO Devil_Fruit_Possession (Fruit_ID, Person_ID) VALUES 
(1, 1),   -- Luffy has Nika
(2, 3),   -- Akainu has Magu Magu
(3, 4),   -- Law has Ope Ope
(4, 7),   -- Kizaru has Pika Pika
(5, 6),   -- Lucci has Leopard
(6, 5),   -- Kaido has Seiryu
(7, 10),  -- Smoker has Moku Moku
(8, 15),  -- Robin has Hana Hana
(9, 30),  -- Brook has Yomi Yomi
(10, 28), -- Ace has Mera Mera
(11, 17), -- Big Mom has Soru Soru
(12, 18), -- Katakuri has Mochi Mochi
(13, 19), -- King has Pteranodon
(14, 20), -- Queen has Brachiosaurus
(15, 21), -- Jack has Mammoth
(16, 33), -- Doflamingo has Ito Ito
(17, 24), -- Marco has Phoenix
(18, 12), -- Kid has Jiki Jiki
(19, 40); -- Bonney has Toshi Toshi

-- =========================================
-- 5. Organizations (Factions & Crews)
-- =========================================

INSERT INTO Faction (Faction_Name, Ideology, Leader_ID) VALUES 
('World Government', 'Absolute Justice and Order', 3), -- Leader Akainu (functionally)
('Four Emperors', 'Freedom and Domination', 1);        -- Loose coalition

INSERT INTO Crew (Crew_Name, Date_Formed, Status) VALUES 
('Straw Hat Pirates', '1522-05-05', 'Active'),
('Heart Pirates', '1520-01-01', 'Active'),
('Beasts Pirates', '1500-01-01', 'Disbanded'),
('Big Mom Pirates', '1980-01-01', 'Active'),
('Red Hair Pirates', '2000-01-01', 'Active'),
('Whitebeard Pirates', '1974-01-01', 'Dissolved'),
('Roger Pirates', '1475-01-01', 'Dissolved'),
('Revolutionary Army', '2000-01-01', 'Active'),
('Kid Pirates', '2015-01-01', 'Active'),
('Donquixote Pirates', '2005-01-01', 'Dissolved');

-- =========================================
-- 6. Relationships (Membership, Allegiance, Territory)
-- =========================================

-- Membership (Pirates only)
INSERT INTO Membership (Person_ID, Crew_ID, Role) VALUES 
(1, 1, 'Captain'),
(2, 1, 'Swordsman'),
(4, 2, 'Captain'),
(5, 3, 'Governor-General'),
(11, 1, 'Cook'),              -- Sanji in Straw Hats
(14, 1, 'Navigator'),         -- Nami in Straw Hats
(15, 1, 'Archaeologist'),     -- Robin in Straw Hats
(16, 1, 'Shipwright'),        -- Franky in Straw Hats
(30, 1, 'Musician'),          -- Brook in Straw Hats
(31, 1, 'Sniper'),            -- Usopp in Straw Hats
(32, 1, 'Helmsman'),          -- Jinbe in Straw Hats
(17, 4, 'Captain'),           -- Big Mom
(18, 4, 'Sweet Commander'),   -- Katakuri in Big Mom Pirates
(19, 3, 'All-Star'),          -- King in Beasts Pirates
(20, 3, 'All-Star'),          -- Queen in Beasts Pirates
(21, 3, 'All-Star'),          -- Jack in Beasts Pirates
(22, 7, 'Captain'),           -- Roger in Roger Pirates
(23, 5, 'Captain'),           -- Shanks in Red Hair Pirates
(24, 6, '1st Division Commander'), -- Marco in Whitebeard Pirates
(28, 6, '2nd Division Commander'), -- Ace in Whitebeard Pirates
(26, 8, 'Supreme Commander'),  -- Dragon in Revolutionary Army
(27, 8, 'Chief of Staff'),     -- Sabo in Revolutionary Army
(50, 8, 'Fish-Man Karate Instructor'), -- Hack in Revolutionary Army
(51, 8, 'Assistant Fish-Man Karate Instructor'), -- Koala in Revolutionary Army
(12, 9, 'Captain'),            -- Kid in Kid Pirates
(13, 9, 'Combatant'),          -- X Drake in Kid Pirates (former)
(33, 10, 'Captain'),           -- Doflamingo in Donquixote Pirates
(47, 10, 'Executive'),         -- Corazon in Donquixote Pirates (undercover)
(45, 7, 'Explorer');           -- Noland in Roger Pirates era (historical)

-- Allegiance
INSERT INTO Allegiance (Crew_ID, Faction_ID) VALUES 
(1, 2), -- Straw Hats (Yonko status)
(3, 2), -- Beasts Pirates (Yonko status)
(4, 2), -- Big Mom Pirates (Yonko status)
(5, 2), -- Red Hair Pirates (Yonko status)
(8, 1); -- Revolutionary Army opposes World Govt (loose allegiance)

-- Territory (Exclusive-OR Check)
-- Rule: Either Faction_ID OR Crew_ID is NULL, never both, never neither.
INSERT INTO Territory (Island_ID, Faction_ID, Crew_ID, Date_Acquired, Control_Level) VALUES 
(1, 1, NULL, '1500-01-01', 'Loose'),        -- Dawn Island controlled by World Govt
(2, 1, NULL, '1400-01-01', 'Absolute'),     -- Marineford controlled by World Govt
(3, NULL, 3, '1504-01-01', 'Totalitarian'), -- Wano controlled by Beasts Pirates (Historical)
(4, 1, NULL, '1520-01-01', 'High Security'),-- Egghead controlled by World Govt
(5, NULL, 4, '1980-01-01', 'Complete'),     -- Whole Cake Island controlled by Big Mom Pirates
(6, 1, NULL, '1400-01-01', 'High'),         -- Loguetown controlled by World Govt
(7, NULL, 10, '2014-01-01', 'Absolute'),    -- Dressrosa controlled by Donquixote Pirates (Historical)
(8, NULL, NULL, '0001-01-01', 'Independent'); -- Elbaf is independent (note: both NULL for independence)

-- =========================================
-- 7. Ships & Weak Entities
-- =========================================

INSERT INTO Ship (Ship_Name, Class, Commission_Date, Owning_Crew_ID, Captain_ID) VALUES 
('Thousand Sunny', 'Brigantine', '1522-10-10', 1, 1),
('Polar Tang', 'Submarine', '1520-05-05', 2, 4),
('Queen Mama Chanter', 'Galleon', '1980-05-05', 4, 17),
('Red Force', 'Galleon', '2000-01-01', 5, 23),
('Moby Dick', 'Galleon', '1974-01-01', 6, 24),
('Oro Jackson', 'Galleon', '1475-01-01', 7, 22),
('Victoria Punk', 'Ship', '2015-01-01', 9, 12),
('Going Merry', 'Caravel', '1522-05-05', 1, 1),
('Numancia Flamingo', 'Galleon', '2005-01-01', 10, 33);

-- Weak Entity: Bounty_Record (Historical data for pirates)
INSERT INTO Bounty_Record (Person_ID, Record_Version, Issue_Date, Amount, Last_Seen_Location, Photo_URL) VALUES 
(1, 1, '1522-06-01', 30000000, 'East Blue', 'img_luffy_v1.jpg'),
(1, 2, '1523-01-01', 1500000000, 'Whole Cake Island', 'img_luffy_v2.jpg'),
(1, 3, '1524-06-01', 3000000000, 'Wano Country', 'img_luffy_gear5.jpg'),
(2, 1, '1524-06-01', 1111000000, 'Wano Country', 'img_zoro_v1.jpg'),
(4, 1, '1521-02-05', 200000000, 'Sabaody', 'img_law_v1.jpg'),
(4, 2, '1524-06-01', 3000000000, 'Wano Country', 'img_law_v2.jpg'),
(11, 1, '1524-06-01', 1032000000, 'Wano Country', 'img_sanji_v1.jpg'),
(12, 1, '1521-02-05', 315000000, 'Sabaody', 'img_kid_v1.jpg'),
(12, 2, '1524-06-01', 3000000000, 'Wano Country', 'img_kid_v2.jpg'),
(14, 1, '1524-06-01', 366000000, 'Wano Country', 'img_nami_v1.jpg'),
(15, 1, '1500-01-01', 79000000, 'Ohara', 'img_robin_v1.jpg'),
(15, 2, '1524-06-01', 930000000, 'Wano Country', 'img_robin_v2.jpg'),
(16, 1, '1524-06-01', 394000000, 'Wano Country', 'img_franky_v1.jpg'),
(17, 1, '1980-01-01', 4388000000, 'Whole Cake Island', 'img_bigmom_v1.jpg'),
(18, 1, '1980-01-01', 1057000000, 'Whole Cake Island', 'img_katakuri_v1.jpg'),
(19, 1, '1500-01-01', 1390000000, 'Wano Country', 'img_king_v1.jpg'),
(20, 1, '1500-01-01', 1320000000, 'Wano Country', 'img_queen_v1.jpg'),
(21, 1, '1500-01-01', 1000000000, 'Wano Country', 'img_jack_v1.jpg'),
(22, 1, '1498-01-01', 5564800000, 'Laugh Tale', 'img_roger_v1.jpg'),
(23, 1, '2000-01-01', 4048900000, 'New World', 'img_shanks_v1.jpg'),
(24, 1, '1974-01-01', 1374000000, 'Marineford', 'img_marco_v1.jpg'),
(28, 1, '2020-01-01', 550000000, 'Marineford', 'img_ace_v1.jpg'),
(30, 1, '1524-06-01', 383000000, 'Wano Country', 'img_brook_v1.jpg'),
(31, 1, '1524-06-01', 500000000, 'Wano Country', 'img_usopp_v1.jpg'),
(32, 1, '1509-01-15', 438000000, 'Fish-Man Island', 'img_jinbe_v1.jpg'),
(32, 2, '1524-06-01', 1100000000, 'Wano Country', 'img_jinbe_v2.jpg'),
(33, 1, '2005-01-01', 340000000, 'Dressrosa', 'img_doffy_v1.jpg'),
(40, 1, '2024-01-01', 320000000, 'Egghead', 'img_bonney_v1.jpg'),
(42, 1, '2000-01-01', 20000000, 'Cocoyasi Village', 'img_arlong_v1.jpg'),
(45, 1, '1120-01-01', 50000000, 'Lvneel', 'img_noland_v1.jpg'),
(52, 1, '2009-01-01', 80000000, 'Amazon Lily', 'img_hancock_v1.jpg'),
(52, 2, '2022-01-01', 1659000000, 'Amazon Lily', 'img_hancock_v2.jpg'),
(55, 1, '2015-01-01', 210000000, 'Kano Country', 'img_sai_v1.jpg'),
(56, 1, '1970-01-01', 542000000, 'Kano Country', 'img_chinjao_v1.jpg');

-- Weak Entity: Log_Entry (Ship Logs)
INSERT INTO Log_Entry (Ship_ID, Log_Timestamp, Entry_Text, Latitude, Longitude) VALUES 
(1, '1524-06-02 08:00:00', 'Departed Wano Country. Conditions foggy.', 40.700000, -74.000000),
(1, '1524-06-05 12:30:00', 'Encountered mechanical shark near Egghead.', 64.000000, -18.000000),
(2, '1524-06-01 10:00:00', 'Submerged to avoid Marine detection.', 40.500000, -73.500000),
(3, '1523-11-15 14:00:00', 'Arrived at Whole Cake Island. Wedding preparations visible.', 25.000000, 70.000000),
(4, '2020-01-01 09:00:00', 'Sailing through New World. Calm seas.', 30.000000, -80.000000),
(7, '2021-01-01 15:30:00', 'Engaged with Marine battleship near Sabaody.', 41.000000, 106.800000),
(8, '1522-05-10 11:00:00', 'Setting sail from Syrup Village. Crew morale high.', 21.300000, 53.800000),
(9, '2014-05-05 16:00:00', 'Approaching Dressrosa. String barriers detected.', 11.200000, -150.700000);

-- 4-ary Relationship: Encounter
INSERT INTO Encounter (Event_ID, Crew_ID, Marine_ID, Island_ID, Description) VALUES 
(3, 1, 7, 4, 'Admiral Kizaru intercepts Straw Hat Pirates at Egghead Island.'),
(1, 6, 3, 2, 'Fleet Admiral Akainu battles Whitebeard Pirates at Marineford Summit War.'),
(4, 10, 10, 7, 'Vice Admiral Smoker confronts Donquixote Pirates in Dressrosa.'),
(5, 4, 8, 5, 'CP0 Agent Stussy infiltrates Big Mom Pirates territory at Whole Cake Island.');

-- 5-ary Relationship: Intelligence Report
INSERT INTO Intelligence_Report (Marine_ID, Target_Person_ID, Island_ID, Ship_ID, Log_Timestamp, Report_Content) VALUES 
(8, 1, 4, 1, '1524-06-05 12:30:00', 'Emperor Straw Hat Luffy confirmed on Egghead. Engaged with Seraphim unit.'),
(6, 4, 3, 2, '1524-06-01 10:00:00', 'Trafalgar Law detected near Wano. Heart Pirates submarine submerged.'),
(10, 33, 7, 9, '2014-05-05 16:00:00', 'Donquixote Doflamingo has complete control over Dressrosa. String barriers active.'),
(8, 17, 5, 3, '1523-11-15 14:00:00', 'Big Mom confirmed at Whole Cake Island. Wedding ceremony in progress.');

-- SET FOREIGN_KEY_CHECKS = 1;

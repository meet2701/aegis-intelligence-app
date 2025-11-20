-- populate.sql
-- Project Phase 4: Aegis Intelligence Database (AID)
-- Data Source: One Piece Wiki (CP0, Marines, Pirates, Arcs)

-- Note: Make sure to run schema.sql first to create the database structure
USE mini_world_db;

-- Disable FK checks temporarily to allow insertion in any order if needed
SET FOREIGN_KEY_CHECKS = 0;

-- =========================================
-- 1. Reference Data (Regions, Events, Fruits)
-- =========================================

INSERT INTO Sea_Region (Region_Name, Threat_Level) VALUES 
('East Blue', 'Low'),
('Grand Line - Paradise', 'High'),
('New World', 'Extreme'),
('West Blue', 'Medium');

INSERT INTO Event (Event_Name, Start_Date, End_Date) VALUES 
('Summit War of Marineford', '1522-01-01', '1522-01-05'),
('Raid on Onigashima', '1524-05-10', '1524-05-11'),
('Egghead Incident', '1524-06-01', NULL),
('God Valley Incident', '1484-01-01', '1484-01-01'),
('Rocky Port Incident', '1520-08-01', '1520-08-01'),
('Whole Cake Island Arc', '1523-04-01', '1523-04-15'),
('Paramount War Preparation', '1521-12-01', '1521-12-31');

INSERT INTO Devil_Fruit (Fruit_Name, Type, Description, is_Awakened) VALUES 
('Hito Hito no Mi, Model: Nika', 'Zoan', 'Grants the user the properties of rubber and the power of the Sun God.', TRUE),
('Magu Magu no Mi', 'Logia', 'Allows the user to create, control, and transform into magma.', FALSE),
('Ope Ope no Mi', 'Paramecia', 'Allows the user to create a spherical space or "room" to manipulate anything inside.', TRUE),
('Pika Pika no Mi', 'Logia', 'Allows the user to create, control, and transform into light.', FALSE),
('Neko Neko no Mi, Model: Leopard', 'Zoan', 'Allows the user to transform into a leopard hybrid.', TRUE),
('Uo Uo no Mi, Model: Seiryu', 'Zoan', 'Allows the user to transform into a giant azure dragon.', FALSE),
('Yami Yami no Mi', 'Logia', 'Allows the user to create and control darkness, and nullify Devil Fruit powers.', FALSE),
('Soru Soru no Mi', 'Paramecia', 'Allows the user to interact with and manipulate souls.', TRUE),
('Mochi Mochi no Mi', 'Paramecia', 'Allows the user to create, control, and transform into mochi.', TRUE),
('Mera Mera no Mi', 'Logia', 'Allows the user to create, control, and transform into fire.', FALSE),
('Hana Hana no Mi', 'Paramecia', 'Allows the user to sprout duplicates of their body parts on any surface.', FALSE),
('Gura Gura no Mi', 'Paramecia', 'Allows the user to create earthquakes and shockwaves.', FALSE);

-- =========================================
-- 2. Locations (Islands)
-- =========================================

INSERT INTO Island (Island_Name, Climate, Population, Latitude, Longitude, Region_ID) VALUES 
('Dawn Island', 'Tropical', 10000, 10.500000, 45.300000, 1),    -- East Blue
('Marineford', 'Temperate', 50000, 35.200000, 139.600000, 2),   -- Paradise
('Wano Country', 'Variable', 200000, 40.700000, -74.000000, 3), -- New World
('Egghead', 'Winter', 5000, 65.100000, -18.500000, 3),          -- New World
('Whole Cake Island', 'Tropical', 150000, 25.000000, 70.000000, 3); -- New World

-- =========================================
-- 3. Persons (Base Table)
-- =========================================

INSERT INTO Person (First_Name, Last_Name, Date_of_Birth, Status, Home_Island_ID) VALUES 
('Monkey D.', 'Luffy', '2005-05-05', 'Active', 1),      -- ID 1
('Roronoa', 'Zoro', '2003-11-11', 'Active', 1),         -- ID 2
('Sakazuki', 'Akainu', '1969-08-16', 'Active', 2),      -- ID 3 (Marine Fleet Admiral)
('Trafalgar', 'Law', '1998-10-06', 'Active', 2),        -- ID 4
('Kaido', 'The Beast', '1960-05-01', 'Deceased', 3),    -- ID 5
('Rob', 'Lucci', '1994-06-02', 'Active', 2),            -- ID 6 (CP0)
('Borsalino', 'Kizaru', '1966-11-23', 'Active', 2),     -- ID 7 (Admiral)
('Stussy', NULL, '1980-01-01', 'Active', 4),            -- ID 8 (CP0/Clone)
('Vegapunk', 'Stella', '1958-01-01', 'Deceased', 4),    -- ID 9 (Civilian/Scientist)
('Shanks', 'Red Hair', '1982-03-09', 'Active', 1),      -- ID 10 (Emperor)
('Marshall D.', 'Teach', '1980-08-03', 'Active', 2),    -- ID 11 (Blackbeard)
('Charlotte', 'Linlin', '1966-02-15', 'Deceased', 5),   -- ID 12 (Big Mom)
('Eustass', 'Kid', '2003-01-10', 'Active', 3),          -- ID 13 (Supernova Captain)
('Buggy', 'The Clown', '1982-08-08', 'Active', 1),      -- ID 14 (Cross Guild Leader)
('Monkey D.', 'Dragon', '1977-10-05', 'Active', 1),     -- ID 15 (Revolutionary Leader)
('Nami', NULL, '2002-07-03', 'Active', 1),              -- ID 16 (Straw Hat Navigator)
('Nico', 'Robin', '1998-02-06', 'Active', 2),           -- ID 17 (Straw Hat Archaeologist)
('Dracule', 'Mihawk', '1981-03-09', 'Active', 2),       -- ID 18 (Worlds Greatest Swordsman)
('Crocodile', 'Sir', '1979-09-05', 'Active', 2),        -- ID 19 (Cross Guild)
('Killer', 'Massacre Soldier', '2003-02-02', 'Active', 3), -- ID 20 (Kid Pirates)
('Ben', 'Beckman', '1979-11-09', 'Active', 1),          -- ID 21 (Red Hair First Mate)
('Charlotte', 'Katakuri', '1992-11-25', 'Active', 5),   -- ID 22 (Big Mom Commander)
('King', 'The Wildfire', '1975-12-01', 'Deceased', 3),  -- ID 23 (Beasts Pirates)
('Sabo', 'Flame Emperor', '2003-03-20', 'Active', 1),   -- ID 24 (Revolutionary)
('Issho', 'Fujitora', '1969-08-10', 'Active', 2);       -- ID 25 (Admiral)

-- =========================================
-- 4. Subclasses & Attributes
-- =========================================

-- Pirates
INSERT INTO Pirate (Person_ID, Infamy_Level) VALUES 
(1, 'Emperor of the Sea'),
(2, 'Supernova'),
(4, 'Warlord (Former)'),
(5, 'Emperor (Former)'),
(10, 'Emperor of the Sea'),
(11, 'Emperor of the Sea'),
(12, 'Emperor (Former)'),
(13, 'Supernova'),
(14, 'Warlord (Former)'),
(16, 'Supernova'),
(17, 'Supernova'),
(18, 'Warlord (Former)'),
(19, 'Warlord (Former)'),
(20, 'Supernova'),
(21, 'Notorious'),
(22, 'Sweet Commander'),
(23, 'All-Star');

-- Marines / CP0 (Mapped as Officers for system simplicity)
INSERT INTO Marine_Officer (Person_ID, `Rank`, Service_Number) VALUES 
(3, 'Fleet Admiral', 'MA-001'),
(6, 'CP0 Masked Agent', 'CP-099'),
(7, 'Admiral', 'MA-003'),
(8, 'CP0 Agent', 'CP-102'),
(25, 'Admiral', 'MA-004');

-- Civilians
INSERT INTO Civilian (Person_ID, Occupation) VALUES 
(9, 'Head Scientist');

-- Revolutionary Army Members (stored as Pirates for system purposes)
INSERT INTO Pirate (Person_ID, Infamy_Level) VALUES 
(15, 'Most Wanted Man'),
(24, 'Revolutionary Chief of Staff');

-- Person Abilities
INSERT INTO Person_Abilities (Person_ID, Ability) VALUES 
(1, 'Conquerors Haki'), (1, 'Armament Haki'), (1, 'Observation Haki'),
(2, 'Santoryu'), (2, 'Armament Haki'),
(3, 'Magma Manipulation'), (3, 'Absolute Justice'),
(4, 'Swordsmanship'), (4, 'Medical Knowledge'),
(6, 'Rokushiki'), (6, 'Armament Haki');

-- Devil Fruit Possession (1:1)
INSERT INTO Devil_Fruit_Possession (Fruit_ID, Person_ID) VALUES 
(1, 1), -- Luffy has Nika
(2, 3), -- Akainu has Magu
(3, 4), -- Law has Ope
(4, 7), -- Kizaru has Pika
(5, 6), -- Lucci has Leopard
(6, 5), -- Kaido has Dragon
(7, 11), -- Blackbeard has Yami
(8, 12), -- Big Mom has Soru
(9, 22), -- Katakuri has Mochi
(10, 24), -- Sabo has Mera
(11, 17); -- Robin has Hana

-- =========================================
-- 5. Organizations (Factions & Crews)
-- =========================================

INSERT INTO Faction (Faction_Name, Ideology, Leader_ID) VALUES 
('World Government', 'Absolute Justice and Order', 3), -- Leader Akainu (functionally)
('Four Emperors', 'Freedom and Domination', 1),        -- Loose coalition
('Revolutionary Army', 'Overthrowing the World Government', NULL), -- Leader added later
('Cross Guild', 'Mercenary Organization for Marines', NULL);       -- Leader added later

-- Update faction leaders after persons are inserted
UPDATE Faction SET Leader_ID = 15 WHERE Faction_Name = 'Revolutionary Army';
UPDATE Faction SET Leader_ID = 14 WHERE Faction_Name = 'Cross Guild';

INSERT INTO Crew (Crew_Name, Date_Formed, Status) VALUES 
('Straw Hat Pirates', '1522-05-05', 'Active'),
('Heart Pirates', '1520-01-01', 'Active'),
('Beasts Pirates', '1500-01-01', 'Disbanded'),
('Red Hair Pirates', '1505-01-01', 'Active'),
('Blackbeard Pirates', '1519-01-01', 'Active'),
('Big Mom Pirates', '1495-01-01', 'Disbanded'),
('Kid Pirates', '1520-01-01', 'Active'),
("Buggy's Delivery", '1522-01-01', 'Active');

-- =========================================
-- 6. Relationships (Membership, Allegiance, Territory)
-- =========================================

-- Membership (Pirates only)
INSERT INTO Membership (Person_ID, Crew_ID, Role) VALUES 
(1, 1, 'Captain'),
(2, 1, 'Swordsman'),
(16, 1, 'Navigator'),
(17, 1, 'Archaeologist'),
(4, 2, 'Captain'),
(5, 3, 'Governor-General'),
(23, 3, 'All-Star'),
(10, 4, 'Captain'),
(21, 4, 'First Mate'),
(11, 5, 'Admiral'),
(12, 6, 'Captain'),
(22, 6, 'Sweet Commander'),
(13, 7, 'Captain'),
(20, 7, 'Combatant'),
(14, 8, 'President'),
(18, 8, 'Executive'),
(19, 8, 'Executive');

-- Allegiance
INSERT INTO Allegiance (Crew_ID, Faction_ID) VALUES 
(1, 2), -- Straw Hats (Yonko status)
(2, 2), -- Heart Pirates (Allied with Luffy)
(3, 2), -- Beasts Pirates (Former Yonko)
(4, 2), -- Red Hair Pirates (Yonko)
(5, 2), -- Blackbeard Pirates (Yonko)
(6, 2), -- Big Mom Pirates (Former Yonko)
(8, 4); -- Buggy's Delivery → Cross Guild

-- Territory (Exclusive-OR Check)
-- Rule: Either Faction_ID OR Crew_ID is NULL, never both, never neither.
INSERT INTO Territory (Island_ID, Faction_ID, Crew_ID, Date_Acquired, Control_Level) VALUES 
(1, 1, NULL, '1500-01-01', 'Loose'),        -- Dawn Island controlled by World Govt
(2, 1, NULL, '1400-01-01', 'Absolute'),     -- Marineford controlled by World Govt
(3, NULL, 1, '1524-05-11', 'Liberation'),   -- Wano controlled by Straw Hats (post-Kaido)
(4, 1, NULL, '1520-01-01', 'High Security'),-- Egghead controlled by World Govt
(5, NULL, 6, '1495-01-01', 'Totalitarian'); -- Whole Cake Island controlled by Big Mom Pirates

-- =========================================
-- 7. Ships & Weak Entities
-- =========================================

INSERT INTO Ship (Ship_Name, Class, Commission_Date, Owning_Crew_ID, Captain_ID) VALUES 
('Thousand Sunny', 'Brigantine', '1522-10-10', 1, 1),
('Polar Tang', 'Submarine', '1520-05-05', 2, 4),
('Onigashima', 'Island Ship', '1510-01-01', 3, 5),
('Red Force', 'Galleon', '1505-01-01', 4, 10),
('Saber of Xebec', 'Raft', '1519-01-01', 5, 11),
('Queen Mama Chanter', 'Singing Ship', '1495-01-01', 6, 12),
('Victoria Punk', 'Battleship', '1520-01-01', 7, 13),
('Big Top', 'Circus Ship', '1522-01-01', 8, 14);

-- Weak Entity: Bounty_Record (Historical data for Luffy)
-- Person 1 = Luffy
INSERT INTO Bounty_Record (Person_ID, Record_Version, Issue_Date, Amount, Last_Seen_Location, Photo_URL) VALUES 
(1, 1, '1522-06-01', 30000000, 'East Blue', 'img_luffy_v1.jpg'),
(1, 2, '1523-01-01', 1500000000, 'Whole Cake Island', 'img_luffy_v2.jpg'),
(1, 3, '1524-06-01', 3000000000, 'Wano Country', 'img_luffy_gear5.jpg'),
(2, 1, '1524-06-01', 1111000000, 'Wano Country', 'img_zoro_v1.jpg'),
(4, 1, '1524-06-01', 3000000000, 'Wano Country', 'img_law_v1.jpg'),
(5, 1, '1520-01-01', 4611100000, 'Wano Country', 'img_kaido.jpg'),
(10, 1, '1520-01-01', 4048900000, 'Elbaf', 'img_shanks.jpg'),
(11, 1, '1524-01-01', 3996000000, 'Beehive Island', 'img_blackbeard.jpg'),
(12, 1, '1523-01-01', 4388000000, 'Whole Cake Island', 'img_bigmom.jpg'),
(13, 1, '1524-06-01', 3000000000, 'Elbaf', 'img_kid.jpg'),
(14, 1, '1523-01-01', 3189000000, 'Karai Bari Island', 'img_buggy.jpg'),
(15, 1, '1522-01-01', 5000000000, 'Baltigo', 'img_dragon.jpg'),
(16, 1, '1524-06-01', 366000000, 'Egghead', 'img_nami.jpg'),
(17, 1, '1524-06-01', 930000000, 'Egghead', 'img_robin.jpg'),
(18, 1, '1520-01-01', 3590000000, 'Kuraigana Island', 'img_mihawk.jpg'),
(19, 1, '1523-01-01', 1965000000, 'Karai Bari Island', 'img_crocodile.jpg'),
(20, 1, '1524-06-01', 200000000, 'Elbaf', 'img_killer.jpg'),
(21, 1, '1520-01-01', 1000000000, 'Elbaf', 'img_beckman.jpg'),
(22, 1, '1523-01-01', 1057000000, 'Whole Cake Island', 'img_katakuri.jpg'),
(23, 1, '1520-01-01', 1390000000, 'Wano Country', 'img_king.jpg'),
(24, 1, '1524-01-01', 602000000, 'Momoiro Island', 'img_sabo.jpg');

-- Weak Entity: Log_Entry (Ship Logs)
-- Ship 1 = Sunny
INSERT INTO Log_Entry (Ship_ID, Log_Timestamp, Entry_Text, Latitude, Longitude) VALUES 
(1, '1524-06-02 08:00:00', 'Departed Wano Country. Conditions foggy.', 40.700000, -74.000000),
(1, '1524-06-05 12:30:00', 'Encountered mechanical shark near Egghead.', 64.000000, -18.000000),
(2, '1524-06-01 10:00:00', 'Submerged to avoid Marine detection.', 40.500000, -73.500000);

-- 4-ary Relationship: Encounter
INSERT INTO Encounter (Event_ID, Crew_ID, Marine_ID, Island_ID, Description) VALUES 
(3, 1, 7, 4, 'Admiral Kizaru intercepts Straw Hat Pirates at Egghead Island.'),
(1, 1, 3, 2, 'Straw Hat Pirates invade Marineford to rescue Ace.'),
(1, 4, 3, 2, 'Red Hair Pirates arrive to end the war.'),
(2, 1, NULL, 3, 'Straw Hat-Heart-Kid alliance raids Onigashima.'),
(2, 2, NULL, 3, 'Heart Pirates support the raid on Kaido.'),
(2, 7, NULL, 3, 'Kid Pirates challenge Big Mom at Onigashima.'),
(4, 4, NULL, 2, 'God Valley Incident involves Roger, Garp, and Rocks.'),
(5, 2, 3, 2, 'Rocky Port Incident: Law causes chaos to become Warlord.'),
(6, 1, NULL, 5, 'Straw Hats clash with Big Mom Pirates at Whole Cake Island.');

-- 5-ary Relationship: Intelligence Report
INSERT INTO Intelligence_Report (Marine_ID, Target_Person_ID, Island_ID, Ship_ID, Log_Timestamp, Report_Content) VALUES 
(8, 1, 4, 1, '1524-06-05 12:30:00', 'Emperor Straw Hat Luffy confirmed on Egghead. Engaged with Seraphim unit.');

SET FOREIGN_KEY_CHECKS = 1;
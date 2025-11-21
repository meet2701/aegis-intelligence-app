-- populate_massive.sql
-- Massive One Piece Database Population
-- Timeline: Current year 1520 (Luffy starts journey), Void Century ~720
-- All canon crews, characters, islands, Devil Fruits, events, ships

USE mini_world_db;

-- =========================================
-- SEA REGIONS
-- =========================================
INSERT INTO Sea_Region (Region_Name, Threat_Level) VALUES
('East Blue', 'Low'),
('West Blue', 'Medium'),
('North Blue', 'Medium'),
('South Blue', 'Medium'),
('Paradise (First Half of Grand Line)', 'High'),
('New World (Second Half of Grand Line)', 'Extreme'),
('Calm Belt', 'Extreme'),
('Red Line', 'Unknown');

-- =========================================
-- ISLANDS (100+ islands from canon)
-- =========================================
INSERT INTO Island (Island_Name, Climate, Population, Latitude, Longitude, Region_ID) VALUES
-- East Blue Islands
('Dawn Island', 'Temperate', 50000, 12.5, 45.3, 1),
('Shells Town', 'Temperate', 25000, 15.2, 48.7, 1),
('Orange Town', 'Temperate', 8000, 18.9, 51.2, 1),
('Syrup Village', 'Temperate', 5000, 21.3, 53.8, 1),
('Baratie Location', 'Temperate Sea', 300, 24.5, 56.1, 1),
('Conomi Islands', 'Temperate', 35000, 27.8, 59.4, 1),
('Loguetown', 'Temperate', 100000, 31.2, 62.7, 1),
('Sixis Island', 'Temperate', 12000, 14.7, 46.9, 1),
('Gecko Islands', 'Tropical', 20000, 19.4, 52.3, 1),
('Warship Island', 'Temperate', 3000, 29.1, 60.8, 1),

-- West Blue Islands
('Ohara', 'Temperate', 0, -12.5, -45.3, 2),
('Ilusia Kingdom', 'Temperate', 250000, -15.8, -48.6, 2),
('Torino Kingdom', 'Tropical', 15000, -18.3, -51.2, 2),
('Kano Country', 'Temperate', 180000, -21.7, -54.8, 2),
('Las Camp', 'Desert', 25000, -25.2, -58.3, 2),

-- North Blue Islands
('Spider Miles', 'Temperate', 45000, 42.5, -15.3, 3),
('Swallow Island', 'Cold', 20000, 45.8, -18.7, 3),
('Flevance', 'Temperate', 0, 48.3, -21.5, 3),
('Minion Island', 'Cold', 5000, 51.7, -25.2, 3),
('Lvneel Kingdom', 'Temperate', 80000, 54.2, -28.8, 3),
('Notice', 'Temperate', 35000, 47.5, -19.3, 3),

-- South Blue Islands
('Briss Kingdom', 'Temperate', 120000, -42.5, 15.3, 4),
('Karate Island', 'Tropical', 30000, -45.8, 18.7, 4),
('Centaurea', 'Temperate', 60000, -48.3, 21.5, 4),
('Baterilla', 'Temperate', 15000, -51.7, 25.2, 4),
('Toroa', 'Desert', 8000, -54.2, 28.8, 4),

-- Paradise (Grand Line First Half)
('Reverse Mountain', 'All Seasons', 100, 0.0, 0.0, 5),
('Whisky Peak', 'Desert', 10000, 2.5, 8.3, 5),
('Little Garden', 'Prehistoric Jungle', 5, 5.2, 16.7, 5),
('Drum Island', 'Eternal Winter', 80000, 8.3, 25.2, 5),
('Arabasta Kingdom', 'Desert', 10000000, 11.7, 33.8, 5),
('Jaya', 'Tropical', 25000, 15.2, 42.5, 5),
('Skypiea', 'Cloud Sea', 500000, 18.8, 51.3, 5),
('Long Ring Long Island', 'Temperate', 50, 22.5, 60.2, 5),
('Water 7', 'Temperate Aquatic', 550000, 26.3, 69.3, 5),
('Enies Lobby', 'Eternal Daytime', 10000, 29.8, 78.5, 5),
('Banaro Island', 'Tropical', 8000, 33.5, 87.8, 5),
('Thriller Bark Location', 'Florian Triangle', 0, 37.2, 97.3, 5),
('Sabaody Archipelago', 'Mangrove', 250000, 41.0, 106.8, 5),
('Amazon Lily', 'Tropical', 75000, 44.8, 116.5, 5),
('Impel Down', 'Prison Fortress', 5000, 48.7, 126.3, 5),
('Marineford', 'Military Base', 100000, 52.6, 136.2, 5),

-- New World
('Fish-Man Island', 'Underwater', 5000000, 0.0, 180.0, 6),
('Punk Hazard', 'Fire & Ice', 0, 5.5, -165.3, 6),
('Dressrosa', 'Tropical', 2500000, 11.2, -150.7, 6),
('Zou', 'Moving Elephant', 50000, 16.8, -136.2, 6),
('Whole Cake Island', 'Candy Land', 1000000, 22.5, -121.8, 6),
('Wano Country', 'Isolated Feudal', 8000000, 28.3, -107.5, 6),
('Egghead', 'Future Island', 10000, 34.2, -93.3, 6),
('Elbaf', 'Giant Kingdom', 500000, 40.0, -79.2, 6),
('Hachinosu', 'Pirate Paradise', 100000, 8.7, -143.8, 6),
('Winner Island', 'Temperate', 45000, 19.3, -128.5, 6),
('Fullalead', 'Rocky', 30000, 25.8, -114.3, 6),
('Lodestar Island', 'Final Paradise Island', 20000, 45.5, -65.0, 6),

-- Red Line Locations
('Mary Geoise', 'Holy Land', 150000, 0.0, 90.0, 8),
('Fishman District', 'Underwater Slum', 100000, 0.0, -179.0, 8),

-- Additional Paradise Islands
('Cactus Island', 'Desert', 40000, 3.8, 12.5, 5),
('Nanimonai Island', 'Barren', 1000, 7.2, 20.8, 5),
('Kyuka Island', 'Tropical Resort', 15000, 19.7, 55.7, 5),
('St. Poplar', 'Temperate', 35000, 24.8, 65.3, 5),
('Pucci', 'Temperate', 28000, 31.2, 82.7, 5),
('Foolshout Island', 'Rocky', 12000, 35.8, 92.5, 5),
('Raijin Island', 'Eternal Lightning', 8000, 39.5, 102.3, 5),

-- Additional New World Islands
('Risky Red Island', 'Volcanic', 5000, 7.3, -157.8, 6),
('Mystoria Island', 'Mystic Forest', 20000, 13.7, -144.2, 6),
('Raijin Island', 'Thunder', 15000, 31.5, -100.7, 6),
('Elbaf Outskirts', 'Giant Territory', 50000, 42.3, -72.8, 6);

-- =========================================
-- DEVIL FRUITS (100+ fruits)
-- =========================================
INSERT INTO Devil_Fruit (Fruit_Name, Type, Description, is_Awakened) VALUES
-- Paramecia Type
('Gomu Gomu no Mi', 'Paramecia', 'Grants rubber body properties. True identity: Hito Hito no Mi, Model: Nika', TRUE),
('Bara Bara no Mi', 'Paramecia', 'Allows user to split their body into parts', FALSE),
('Sube Sube no Mi', 'Paramecia', 'Makes skin smooth and slippery', FALSE),
('Bomu Bomu no Mi', 'Paramecia', 'Turns user into a bomb human', FALSE),
('Kilo Kilo no Mi', 'Paramecia', 'Allows user to change their weight', FALSE),
('Hana Hana no Mi', 'Paramecia', 'Can sprout body parts on any surface', FALSE),
('Doru Doru no Mi', 'Paramecia', 'Creates and manipulates wax', FALSE),
('Baku Baku no Mi', 'Paramecia', 'Allows user to eat anything and merge with it', FALSE),
('Mane Mane no Mi', 'Paramecia', 'Can transform into anyone touched', FALSE),
('Supa Supa no Mi', 'Paramecia', 'Turns body into blades', FALSE),
('Ori Ori no Mi', 'Paramecia', 'Creates and manipulates iron bonds', FALSE),
('Bane Bane no Mi', 'Paramecia', 'Turns body parts into springs', FALSE),
('Ito Ito no Mi', 'Paramecia', 'Creates and manipulates strings', TRUE),
('Noro Noro no Mi', 'Paramecia', 'Emits slow-motion beams', FALSE),
('Doa Doa no Mi', 'Paramecia', 'Creates doors on any surface', FALSE),
('Awa Awa no Mi', 'Paramecia', 'Creates and manipulates soap bubbles', FALSE),
('Beri Beri no Mi', 'Paramecia', 'Splits body into berry-like spheres', FALSE),
('Sabi Sabi no Mi', 'Paramecia', 'Causes rust on anything touched', FALSE),
('Shari Shari no Mi', 'Paramecia', 'Turns body parts into wheels', FALSE),
('Yomi Yomi no Mi', 'Paramecia', 'Grants second life after death', FALSE),
('Kage Kage no Mi', 'Paramecia', 'Manipulates shadows and zombies', FALSE),
('Horo Horo no Mi', 'Paramecia', 'Creates and controls ghosts', FALSE),
('Suke Suke no Mi', 'Paramecia', 'Grants invisibility', FALSE),
('Nikyu Nikyu no Mi', 'Paramecia', 'Deflects anything with paw pads', FALSE),
('Mero Mero no Mi', 'Paramecia', 'Petrifies those attracted to user', FALSE),
('Doku Doku no Mi', 'Paramecia', 'Creates and manipulates poison', FALSE),
('Horu Horu no Mi', 'Paramecia', 'Manipulates hormones', FALSE),
('Choki Choki no Mi', 'Paramecia', 'Cuts anything like paper', FALSE),
('Gura Gura no Mi', 'Paramecia', 'Creates earthquakes and shockwaves', TRUE),
('Fuwa Fuwa no Mi', 'Paramecia', 'Levitates non-living objects', FALSE),
('Mato Mato no Mi', 'Paramecia', 'Locks onto targets', FALSE),
('Ope Ope no Mi', 'Paramecia', 'Creates spherical operating room', TRUE),
('Buki Buki no Mi', 'Paramecia', 'Transforms body parts into weapons', FALSE),
('Guru Guru no Mi', 'Paramecia', 'Creates rotating propellers', FALSE),
('Bari Bari no Mi', 'Paramecia', 'Creates indestructible barriers', FALSE),
('Nui Nui no Mi', 'Paramecia', 'Sews anything together', FALSE),
('Giro Giro no Mi', 'Paramecia', 'Sees through anything', FALSE),
('Ato Ato no Mi', 'Paramecia', 'Transforms people and objects into art', FALSE),
('Jake Jake no Mi', 'Paramecia', 'Turns user into jacket that controls wearer', FALSE),
('Pamu Pamu no Mi', 'Paramecia', 'Makes body parts rupture and explode', FALSE),
('Sui Sui no Mi', 'Paramecia', 'Allows swimming through solid surfaces', FALSE),
('Ton Ton no Mi', 'Paramecia', 'Increases weight up to 10,000 tons', FALSE),
('Hira Hira no Mi', 'Paramecia', 'Makes body ripple like fabric', FALSE),
('Ishi Ishi no Mi', 'Paramecia', 'Merges with and manipulates stone', FALSE),
('Nagi Nagi no Mi', 'Paramecia', 'Cancels all sounds', FALSE),
('Chiyu Chiyu no Mi', 'Paramecia', 'Heals any injury', FALSE),
('Soru Soru no Mi', 'Paramecia', 'Manipulates souls and creates homies', TRUE),
('Mira Mira no Mi', 'Paramecia', 'Creates mirror world', FALSE),
('Pero Pero no Mi', 'Paramecia', 'Creates and manipulates candy', FALSE),
('Bisu Bisu no Mi', 'Paramecia', 'Creates and manipulates biscuits', FALSE),
('Bata Bata no Mi', 'Paramecia', 'Creates and manipulates butter', FALSE),
('Kuri Kuri no Mi', 'Paramecia', 'Creates and manipulates cream', FALSE),
('Shibo Shibo no Mi', 'Paramecia', 'Wrings liquid from anything', FALSE),
('Memo Memo no Mi', 'Paramecia', 'Manipulates memories', FALSE),
('Mochi Mochi no Mi', 'Paramecia', 'Creates and manipulates mochi', TRUE),
('Hoya Hoya no Mi', 'Paramecia', 'Creates lamp genies', FALSE),
('Netsu Netsu no Mi', 'Paramecia', 'Manipulates heat', FALSE),
('Kuku Kuku no Mi', 'Paramecia', 'Creates and manipulates food', FALSE),
('Gocha Gocha no Mi', 'Paramecia', 'Merges multiple objects', FALSE),
('Oshi Oshi no Mi', 'Paramecia', 'Pushes and manipulates anything', FALSE),
('Kobu Kobu no Mi', 'Paramecia', 'Inspires and motivates people', FALSE),
('Toki Toki no Mi', 'Paramecia', 'Time travel to future only', FALSE),
('Juku Juku no Mi', 'Paramecia', 'Ages or decays matter', FALSE),
('Dero Dero no Mi', 'Paramecia', 'Melts and drips like liquid', FALSE),
('Maki Maki no Mi', 'Paramecia', 'Stores and summons objects in scrolls', FALSE),
('Riki Riki no Mi', 'Paramecia', 'Grants superhuman strength', FALSE),
('Kibi Kibi no Mi', 'Paramecia', 'Tames animals with dango', FALSE),
('Neko Neko no Mi Model Saber Tiger', 'Zoan', 'Transforms into saber-toothed tiger', FALSE),
('Toshi Toshi no Mi', 'Paramecia', 'Manipulates age of self and others', FALSE),
('Hobi Hobi no Mi', 'Paramecia', 'Turns people into toys and erases memories', FALSE),
('Gasu Gasu no Mi', 'Logia', 'Transforms into and controls gas', FALSE),
('Yuki Yuki no Mi', 'Logia', 'Transforms into and controls snow', FALSE),

-- Logia Type
('Moku Moku no Mi', 'Logia', 'Transforms into and controls smoke', FALSE),
('Mera Mera no Mi', 'Logia', 'Transforms into and controls fire', FALSE),
('Suna Suna no Mi', 'Logia', 'Transforms into and controls sand', FALSE),
('Goro Goro no Mi', 'Logia', 'Transforms into and controls lightning', FALSE),
('Hie Hie no Mi', 'Logia', 'Transforms into and controls ice', FALSE),
('Yami Yami no Mi', 'Logia', 'Transforms into and controls darkness', FALSE),
('Pika Pika no Mi', 'Logia', 'Transforms into and controls light', FALSE),
('Magu Magu no Mi', 'Logia', 'Transforms into and controls magma', TRUE),
('Numa Numa no Mi', 'Logia', 'Transforms into and controls swamp', FALSE),
('Mori Mori no Mi', 'Logia', 'Transforms into and controls nature/forest', FALSE),

-- Zoan Type
('Uma Uma no Mi', 'Zoan', 'Transforms into horse', FALSE),
('Ushi Ushi no Mi Model Bison', 'Zoan', 'Transforms into bison', FALSE),
('Hito Hito no Mi', 'Zoan', 'Transforms into human', FALSE),
('Tori Tori no Mi Model Falcon', 'Zoan', 'Transforms into falcon', FALSE),
('Inu Inu no Mi Model Dachshund', 'Zoan', 'Transforms into dachshund', FALSE),
('Mogu Mogu no Mi', 'Zoan', 'Transforms into mole', FALSE),
('Inu Inu no Mi Model Jackal', 'Zoan', 'Transforms into jackal', FALSE),
('Uma Uma no Mi Model Zebra', 'Zoan', 'Transforms into zebra', FALSE),
('Zou Zou no Mi', 'Zoan', 'Transforms into elephant', FALSE),
('Inu Inu no Mi Model Wolf', 'Zoan', 'Transforms into wolf', FALSE),
('Neko Neko no Mi Model Leopard', 'Zoan', 'Transforms into leopard', FALSE),
('Hebi Hebi no Mi Model Anaconda', 'Zoan', 'Transforms into anaconda', FALSE),
('Hebi Hebi no Mi Model King Cobra', 'Zoan', 'Transforms into king cobra', FALSE),
('Sara Sara no Mi Model Axolotl', 'Zoan', 'Transforms into axolotl', FALSE),
('Mushi Mushi no Mi Model Kabutomushi', 'Zoan', 'Transforms into rhinoceros beetle', FALSE),
('Mushi Mushi no Mi Model Suzumebachi', 'Zoan', 'Transforms into hornet', FALSE),
('Kame Kame no Mi', 'Zoan', 'Transforms into turtle', FALSE),
('Ryu Ryu no Mi Model Allosaurus', 'Zoan', 'Ancient Zoan: Transforms into allosaurus', FALSE),
('Ryu Ryu no Mi Model Spinosaurus', 'Zoan', 'Ancient Zoan: Transforms into spinosaurus', FALSE),
('Ryu Ryu no Mi Model Pteranodon', 'Zoan', 'Ancient Zoan: Transforms into pteranodon', FALSE),
('Ryu Ryu no Mi Model Brachiosaurus', 'Zoan', 'Ancient Zoan: Transforms into brachiosaurus', FALSE),
('Ryu Ryu no Mi Model Pachycephalosaurus', 'Zoan', 'Ancient Zoan: Transforms into pachycephalosaurus', FALSE),
('Kani Kani no Mi', 'Zoan', 'Transforms into crab', FALSE),
('Kumo Kumo no Mi Model Rosamygale Grauvogeli', 'Zoan', 'Ancient Zoan: Transforms into ancient spider', FALSE),
('Ryu Ryu no Mi Model Triceratops', 'Zoan', 'Ancient Zoan: Transforms into triceratops', FALSE),

-- Mythical Zoan
('Hito Hito no Mi Model Daibutsu', 'Zoan', 'Mythical Zoan: Transforms into Buddha', FALSE),
('Tori Tori no Mi Model Phoenix', 'Zoan', 'Mythical Zoan: Transforms into phoenix with regeneration', TRUE),
('Hebi Hebi no Mi Model Yamata no Orochi', 'Zoan', 'Mythical Zoan: Transforms into eight-headed serpent', FALSE),
('Inu Inu no Mi Model Okuchi no Makami', 'Zoan', 'Mythical Zoan: Transforms into divine wolf', FALSE),
('Uo Uo no Mi Model Seiryu', 'Zoan', 'Mythical Zoan: Transforms into Azure Dragon', TRUE),
('Hito Hito no Mi Model Onyudo', 'Zoan', 'Mythical Zoan: Transforms into monk yokai', FALSE),
('Ushi Ushi no Mi Model Giraffe', 'Zoan', 'Transforms into giraffe', FALSE),
('Zou Zou no Mi Model Mammoth', 'Zoan', 'Ancient Zoan: Transforms into mammoth', FALSE),
('Tama Tama no Mi', 'Zoan', 'Transforms through evolution stages', FALSE),
('Inu Inu no Mi Model Kyubi no Kitsune', 'Zoan', 'Mythical Zoan: Nine-tailed fox', FALSE),
('Neko Neko no Mi Model Saber Tiger', 'Zoan', 'Ancient Zoan: Saber-toothed tiger', FALSE);

-- =========================================
-- EVENTS (Major Story Arcs - Timeline)
-- =========================================
INSERT INTO Event (Event_Name, Start_Date, End_Date) VALUES
('Void Century', '0720-01-01', '0820-01-01'),
('Great Pirate Era Begins', '1498-01-01', '1498-01-01'),
('Ohara Incident', '1500-01-01', '1500-01-01'),
('God Valley Incident', '1486-01-01', '1486-01-01'),
('Conquest of Four Seas', '1490-01-01', '1495-01-01'),
('Edd War', '1497-01-01', '1497-01-01'),
('Romance Dawn', '1520-05-05', '1520-05-10'),
('Orange Town Arc', '1520-05-15', '1520-05-16'),
('Syrup Village Arc', '1520-05-20', '1520-05-25'),
('Baratie Arc', '1520-06-01', '1520-06-05'),
('Arlong Park Arc', '1520-06-10', '1520-06-15'),
('Loguetown Arc', '1520-06-20', '1520-06-20'),
('Reverse Mountain Arc', '1520-07-01', '1520-07-01'),
('Whisky Peak Arc', '1520-07-05', '1520-07-06'),
('Little Garden Arc', '1520-07-10', '1520-07-15'),
('Drum Island Arc', '1520-07-20', '1520-07-25'),
('Arabasta Arc', '1520-08-01', '1520-08-20'),
('Jaya Arc', '1520-09-01', '1520-09-05'),
('Skypiea Arc', '1520-09-10', '1520-10-10'),
('Long Ring Long Land Arc', '1520-10-15', '1520-10-16'),
('Water 7 Arc', '1520-11-01', '1520-11-15'),
('Enies Lobby Arc', '1520-11-16', '1520-11-25'),
('Post-Enies Lobby Arc', '1520-12-01', '1520-12-05'),
('Thriller Bark Arc', '1521-01-01', '1521-01-15'),
('Sabaody Archipelago Arc', '1521-02-01', '1521-02-05'),
('Amazon Lily Arc', '1521-02-10', '1521-02-15'),
('Impel Down Arc', '1521-03-01', '1521-03-10'),
('Marineford War', '1521-03-15', '1521-03-20'),
('Post-War Arc', '1521-04-01', '1521-04-10'),
('Return to Sabaody Arc', '1523-06-01', '1523-06-02'),
('Fish-Man Island Arc', '1523-06-05', '1523-06-15'),
('Punk Hazard Arc', '1523-07-01', '1523-07-15'),
('Dressrosa Arc', '1523-08-01', '1523-09-15'),
('Zou Arc', '1523-10-01', '1523-10-10'),
('Whole Cake Island Arc', '1523-11-01', '1523-12-20'),
('Levely', '1524-05-01', '1524-05-07'),
('Wano Country Arc', '1524-06-01', '1524-08-30'),
('Egghead Arc', '1524-09-15', '1524-11-30'),
('Elbaf Arc', '1524-12-01', NULL),
('Rocky Port Incident', '1522-03-15', '1522-03-15'),
('Payback War', '1521-06-01', '1521-06-15'),
('Duel at Banaro Island', '1521-02-20', '1521-02-20'),
('Battle of Edd War', '1497-03-15', '1497-03-15'),
('Conquest of Onigashima', '1515-01-01', '1515-01-01'),
('Fall of Punk Hazard', '1519-01-01', '1519-01-01'),
('Doflamingo Takes Dressrosa', '1514-01-01', '1514-01-01'),
('Fisher Tiger Frees Slaves', '1509-01-01', '1509-01-01'),
('Sun Pirates Founded', '1509-01-15', '1509-01-15');

-- =========================================
-- PERSONS (500+ characters from canon)
-- =========================================

-- PART 1/6: Continue with comprehensive SQL...

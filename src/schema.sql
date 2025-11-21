-- schema.sql
-- Project Phase 4: Aegis Intelligence Database (AID)
-- Team: Big Three

DROP DATABASE IF EXISTS mini_world_db;
CREATE DATABASE mini_world_db;
USE mini_world_db;

-- =========================================
-- 1. Independent Entities (Lookups & Locations)
-- =========================================

CREATE TABLE Sea_Region (
    Region_ID INT AUTO_INCREMENT PRIMARY KEY,
    Region_Name VARCHAR(100) NOT NULL UNIQUE,
    Threat_Level VARCHAR(50)
);

CREATE TABLE Island (
    Island_ID INT AUTO_INCREMENT PRIMARY KEY,
    Island_Name VARCHAR(100) NOT NULL,
    Climate VARCHAR(100),
    Population INT,
    Latitude DECIMAL(10, 6),
    Longitude DECIMAL(10, 6),
    Region_ID INT NOT NULL,
    FOREIGN KEY (Region_ID) REFERENCES Sea_Region(Region_ID) ON UPDATE CASCADE
);

CREATE TABLE Devil_Fruit (
    Fruit_ID INT AUTO_INCREMENT PRIMARY KEY,
    Fruit_Name VARCHAR(100) NOT NULL UNIQUE,
    Type ENUM('Paramecia', 'Zoan', 'Logia') NOT NULL,
    Description TEXT,
    is_Awakened BOOLEAN DEFAULT FALSE
);

CREATE TABLE Event (
    Event_ID INT AUTO_INCREMENT PRIMARY KEY,
    Event_Name VARCHAR(150) NOT NULL,
    Start_Date DATE,
    End_Date DATE
);

-- =========================================
-- 2. Main Entities (Person & Organizations)
-- =========================================

CREATE TABLE Person (
    Person_ID INT AUTO_INCREMENT PRIMARY KEY,
    First_Name VARCHAR(100) NOT NULL,
    Last_Name VARCHAR(100),
    Date_of_Birth DATE,
    Status ENUM('Active', 'Deceased', 'Captured', 'Unknown') NOT NULL DEFAULT 'Unknown',
    Home_Island_ID INT,
    FOREIGN KEY (Home_Island_ID) REFERENCES Island(Island_ID) ON DELETE SET NULL
);

-- Junction Table for Multi-valued Attribute: Known Abilities
CREATE TABLE Person_Abilities (
    Person_ID INT,
    Ability VARCHAR(100),
    PRIMARY KEY (Person_ID, Ability),
    FOREIGN KEY (Person_ID) REFERENCES Person(Person_ID) ON DELETE CASCADE
);

-- Subclass: Pirate
CREATE TABLE Pirate (
    Person_ID INT PRIMARY KEY,
    Infamy_Level VARCHAR(50),
    FOREIGN KEY (Person_ID) REFERENCES Person(Person_ID) ON DELETE CASCADE
);

-- Subclass: Marine_Officer
CREATE TABLE Marine_Officer (
    Person_ID INT PRIMARY KEY,
    `Rank` VARCHAR(50) NOT NULL,
    Service_Number VARCHAR(50) UNIQUE,
    FOREIGN KEY (Person_ID) REFERENCES Person(Person_ID) ON DELETE CASCADE
);

-- Subclass: Civilian
CREATE TABLE Civilian (
    Person_ID INT PRIMARY KEY,
    Occupation VARCHAR(100),
    FOREIGN KEY (Person_ID) REFERENCES Person(Person_ID) ON DELETE CASCADE
);

CREATE TABLE Faction (
    Faction_ID INT AUTO_INCREMENT PRIMARY KEY,
    Faction_Name VARCHAR(100) NOT NULL UNIQUE,
    Ideology TEXT,
    Leader_ID INT,
    FOREIGN KEY (Leader_ID) REFERENCES Person(Person_ID) ON DELETE SET NULL
);

CREATE TABLE Crew (
    Crew_ID INT AUTO_INCREMENT PRIMARY KEY,
    Crew_Name VARCHAR(100) NOT NULL UNIQUE,
    Date_Formed DATE,
    Status VARCHAR(50)
);

CREATE TABLE Ship (
    Ship_ID INT AUTO_INCREMENT PRIMARY KEY,
    Ship_Name VARCHAR(100) NOT NULL,
    Class VARCHAR(50),
    Commission_Date DATE,
    Owning_Crew_ID INT,
    Captain_ID INT,
    FOREIGN KEY (Owning_Crew_ID) REFERENCES Crew(Crew_ID) ON DELETE SET NULL,
    FOREIGN KEY (Captain_ID) REFERENCES Person(Person_ID) ON DELETE SET NULL
);

-- =========================================
-- 3. Weak Entities
-- =========================================

CREATE TABLE Bounty_Record (
    Person_ID INT,
    Record_Version INT,
    Issue_Date DATE NOT NULL,
    Amount BIGINT NOT NULL CHECK (Amount >= 0),
    Last_Seen_Location VARCHAR(255),
    Photo_URL VARCHAR(255),
    PRIMARY KEY (Person_ID, Record_Version),
    FOREIGN KEY (Person_ID) REFERENCES Person(Person_ID) ON DELETE CASCADE
);

CREATE TABLE Log_Entry (
    Ship_ID INT,
    Log_Timestamp DATETIME,
    Entry_Text TEXT,
    Latitude DECIMAL(10, 6),
    Longitude DECIMAL(10, 6),
    PRIMARY KEY (Ship_ID, Log_Timestamp),
    FOREIGN KEY (Ship_ID) REFERENCES Ship(Ship_ID) ON DELETE CASCADE
);

-- =========================================
-- 4. Relationships & Junction Tables
-- =========================================

-- Relationship: MEMBERSHIP (Person <-> Crew)
CREATE TABLE Membership (
    Person_ID INT,
    Crew_ID INT,
    Role VARCHAR(50), -- Added based on Phase 2 changes
    PRIMARY KEY (Person_ID, Crew_ID),
    FOREIGN KEY (Person_ID) REFERENCES Person(Person_ID) ON DELETE CASCADE,
    FOREIGN KEY (Crew_ID) REFERENCES Crew(Crew_ID) ON DELETE CASCADE
);

-- Relationship: POSSESSES (Person <-> Devil Fruit) 1:1
-- Note: UNIQUE constraint on Fruit_ID ensures 1 fruit per person logic globally
CREATE TABLE Devil_Fruit_Possession (
    Fruit_ID INT PRIMARY KEY,
    Person_ID INT UNIQUE,
    FOREIGN KEY (Fruit_ID) REFERENCES Devil_Fruit(Fruit_ID) ON DELETE CASCADE,
    FOREIGN KEY (Person_ID) REFERENCES Person(Person_ID) ON DELETE CASCADE
);

-- Relationship: ALLEGIANCE (Crew <-> Faction)
CREATE TABLE Allegiance (
    Crew_ID INT,
    Faction_ID INT,
    PRIMARY KEY (Crew_ID, Faction_ID),
    FOREIGN KEY (Crew_ID) REFERENCES Crew(Crew_ID) ON DELETE CASCADE,
    FOREIGN KEY (Faction_ID) REFERENCES Faction(Faction_ID) ON DELETE CASCADE
);

-- Relationship: TERRITORY (The tricky Exclusive-OR one)
-- Rule: A territory is controlled by EITHER a Faction OR a Crew.
-- Note: XOR constraint enforced at application level due to MySQL CHECK constraint limitations with foreign keys
CREATE TABLE Territory (
    Island_ID INT PRIMARY KEY,
    Faction_ID INT DEFAULT NULL,
    Crew_ID INT DEFAULT NULL,
    Date_Acquired DATE,
    Control_Level VARCHAR(50),
    FOREIGN KEY (Island_ID) REFERENCES Island(Island_ID) ON DELETE CASCADE,
    FOREIGN KEY (Faction_ID) REFERENCES Faction(Faction_ID) ON DELETE SET NULL,
    FOREIGN KEY (Crew_ID) REFERENCES Crew(Crew_ID) ON DELETE SET NULL
    -- CHECK constraint removed: MySQL doesn't support CHECK on columns with ON DELETE SET NULL
    -- XOR logic: (Faction_ID IS NOT NULL AND Crew_ID IS NULL) OR (Faction_ID IS NULL AND Crew_ID IS NOT NULL)
);

-- Relationship: ENCOUNTER (N-ary: Crew, Marine, Island, Event)
CREATE TABLE Encounter (
    Encounter_ID INT AUTO_INCREMENT PRIMARY KEY, -- Surrogate key for simplicity
    Event_ID INT,
    Crew_ID INT,
    Marine_ID INT,
    Island_ID INT,
    Description TEXT,
    FOREIGN KEY (Event_ID) REFERENCES Event(Event_ID) ON DELETE CASCADE,
    FOREIGN KEY (Crew_ID) REFERENCES Crew(Crew_ID) ON DELETE CASCADE,
    FOREIGN KEY (Marine_ID) REFERENCES Marine_Officer(Person_ID) ON DELETE CASCADE,
    FOREIGN KEY (Island_ID) REFERENCES Island(Island_ID) ON DELETE CASCADE
);

-- Relationship: INTELLIGENCE_REPORT (N-ary)
CREATE TABLE Intelligence_Report (
    Report_ID INT AUTO_INCREMENT PRIMARY KEY,
    Marine_ID INT, -- The reporter (CP Agent)
    Target_Person_ID INT,
    Island_ID INT,
    Ship_ID INT, -- For linking to Log Entry
    Log_Timestamp DATETIME, -- For linking to Log Entry
    Report_Content TEXT,
    FOREIGN KEY (Marine_ID) REFERENCES Marine_Officer(Person_ID) ON DELETE CASCADE,
    FOREIGN KEY (Target_Person_ID) REFERENCES Person(Person_ID) ON DELETE CASCADE,
    FOREIGN KEY (Island_ID) REFERENCES Island(Island_ID) ON DELETE CASCADE,
    FOREIGN KEY (Ship_ID, Log_Timestamp) REFERENCES Log_Entry(Ship_ID, Log_Timestamp) ON DELETE SET NULL
);
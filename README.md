# Aegis Intelligence Database (AID)

**World Government Intelligence Terminal - One Piece Universe**

DnA Course Project, for application interface to interact with the data of our selected mini world "One Piece".

**Team Big Three** | Phase 4 Final Submission | November 2025

**Members:** Meet Parekh (2024101122), Jainam Modi (2024101057), Divya Padariya (2024113010)

---

## 🚀 Installation & Setup

### Prerequisites

- Python 3.8+
- MySQL Server 8.0+
- pip (Python package manager)

### Step 1: Install Dependencies

```bash
pip install -r src/requirements.txt
```

### Step 2: Setup Database

```bash
# Login to MySQL
mysql -u root -p

# Execute schema and populate scripts
source src/schema.sql
source src/populate.sql
```

### Step 3: Run Application

```bash
cd src
python app.py
```

When prompted, enter your MySQL root password.

### Step 4: Access Application

Open your browser and navigate to:

```
http://127.0.0.1:5000
```

---

## 🔐 Login Credentials

| Role | Username | Password | Access |
|------|----------|----------|--------|
| Marine Officer | `MARINE_HQ` | `SEAGULL` | 7 Intel + 3 Tactical + 9 Operations |

---

## 📋 Complete Application Features - 19 Operations

This list matches the video demonstration order and provides a clear numbered list of all commands/features.

### 🔵 INTELLIGENCE HUB - 7 Query Operations

#### **1. Pirate Search**
- **Description:** Search pirates by name, bounty range, or sea region with detailed crew affiliations
- **SQL Operation:** `SELECT` with `JOIN` (Person, Pirate, Crew, Membership, Bounty_Record, Island, Sea_Region)
- **Input:** Name filter (partial match), bounty min/max, region dropdown
- **Output:** Table showing Person_ID, Name, Bounty, Infamy Level, Status, Crew, Home Island, Region

#### **2. Devil Fruit Encyclopedia**
- **Description:** Browse all Devil Fruits with filtering by type and awakened status, shows current possessor
- **SQL Operation:** `SELECT` with `LEFT JOIN` (Devil_Fruit, Devil_Fruit_Possession, Person)
- **Input:** Type filter (Paramecia/Zoan/Logia), awakened status checkbox
- **Output:** Table showing Fruit_ID, Name, Type, Description, Awakened Status, Current Owner

#### **3. Marine Directory**
- **Description:** Search Marine officers by rank, status, or stationed island
- **SQL Operation:** `SELECT` with `JOIN` (Person, Marine_Officer, Island, Sea_Region)
- **Input:** Rank dropdown (Admiral/Vice Admiral/etc.), status filter, island selection
- **Output:** Table showing Officer_ID, Name, Rank, Status, Stationed Island, Region

#### **4. Bounty Index**
- **Description:** Complete list of all bounty records with version history and status tracking
- **SQL Operation:** `SELECT` with `JOIN` (Bounty_Record, Person, Pirate) ordered by amount descending
- **Input:** None (displays all)
- **Output:** Table showing Person_ID, Name, Bounty Amount, Record Version, Issue Date, Status

#### **5. Will of D Search**
- **Description:** Find all individuals with the "D" initial in their name (the mysterious Will of D lineage)
- **SQL Operation:** `SELECT` with `WHERE` clause using `LIKE '%D.%'` pattern matching
- **Input:** None (automatic pattern search)
- **Output:** Table showing Person_ID, Full Name, Status, Person Type (Pirate/Marine/Civilian)

#### **6. Ability Search**
- **Description:** Search characters by their special abilities or powers
- **SQL Operation:** `SELECT` with `JOIN` (Person_Abilities, Person, Abilities) using ability name filter
- **Input:** Ability dropdown selector
- **Output:** Table showing all people possessing the selected ability

#### **7. Ship Log Decrypter**
- **Description:** View ship log entries with timestamps and coordinates
- **SQL Operation:** `SELECT` with `JOIN` (Log_Entry, Ship, Crew) filtered by ship selection
- **Input:** Ship dropdown
- **Output:** Chronological log entries with Timestamp, Entry Text, GPS Coordinates

---

### 📊 TACTICAL ANALYSIS HUB - 3 Aggregate Queries

#### **8. Crew Valuation**
- **Description:** Calculate total combined bounty of all crew members for threat assessment
- **SQL Operation:** `SELECT` with `JOIN` and `SUM` aggregation (Crew, Membership, Person, Bounty_Record)
- **Input:** Crew dropdown selection
- **Output:** Crew info card + members table with individual bounties + total crew bounty sum

#### **9. Island Census**
- **Description:** Count islands per sea region with population statistics and climate diversity
- **SQL Operation:** `SELECT` with `GROUP BY` using `COUNT`, `SUM`, `AVG`, `GROUP_CONCAT` functions
- **Input:** None (automatically processes all regions)
- **Output:** Table showing Region, Island Count, Total Population, Average Population, Climate Types

#### **10. Most Wanted**
- **Description:** Display the single highest bounty in the entire database (simplest query)
- **SQL Operation:** `SELECT` with `MAX` subquery - returns only pirate name and bounty amount
- **Input:** None (automatic)
- **Output:** Dramatic "WANTED" poster showing Pirate Name and Bounty Amount

---

### ⚔️ COMMAND OPERATIONS HUB - 9 CRUD Operations

#### **INSERT Operations (3)**

#### **11. Register Criminal**
- **Description:** Add a new pirate to the database with personal details and optional crew membership
- **SQL Operation:** `INSERT INTO Person`, `INSERT INTO Pirate`, `INSERT INTO Membership` (transaction)
- **Input:** First/Last name, DOB, status dropdown, home island dropdown, infamy level, crew (optional), role (optional)
- **Output:** Success message with new Person_ID, confirmation in MySQL database

#### **12. Issue Bounty**
- **Description:** Create a new bounty record for an existing person with automatic version tracking
- **SQL Operation:** `INSERT INTO Bounty_Record` with automatic Record_Version increment
- **Input:** Person dropdown, bounty amount (numeric), issue date, reasoning (text)
- **Output:** Success message, new bounty record visible in Bounty Index

#### **13. Log Devil Fruit**
- **Description:** Register a new Devil Fruit in the encyclopedia database
- **SQL Operation:** `INSERT INTO Devil_Fruit`
- **Input:** Fruit name, type dropdown (Paramecia/Zoan/Logia), description (text), awakened status (checkbox)
- **Output:** Success message, new fruit appears in Devil Fruit Encyclopedia

---

#### **UPDATE Operations (3)**

#### **14. Update Person Status**
- **Description:** Change operational status of any person (Active/Captured/Deceased/Unknown)
- **SQL Operation:** `UPDATE Person SET Status = ? WHERE Person_ID = ?`
- **Input:** Person dropdown (shows current status), new status dropdown
- **Output:** Success message, updated status reflected in all queries

#### **15. Update Bounty Amount**
- **Description:** Modify existing bounty or create new version for bounty increase (preserves history)
- **SQL Operation:** `INSERT INTO Bounty_Record` with incremented Record_Version
- **Input:** Person dropdown (must have existing bounty), new bounty amount, update date, reasoning
- **Output:** Success message, new record version created, history preserved

#### **16. Update Fruit Possession**
- **Description:** Transfer Devil Fruit from current owner to new person (UPDATE operation, not INSERT)
- **SQL Operation:** `UPDATE Devil_Fruit_Possession SET Person_ID = ? WHERE Fruit_ID = ?`
- **Input:** Fruit dropdown (only shows currently possessed fruits), new person dropdown
- **Output:** Success message, fruit possession transferred in database

---

#### **DELETE Operations (3)**

#### **17. Revoke Bounty**
- **Description:** Delete all bounty records for a specific person (complete bounty removal)
- **SQL Operation:** `DELETE FROM Bounty_Record WHERE Person_ID = ?`
- **Input:** Shows table of all people with bounties, click delete button
- **Output:** Confirmation dialog, then success message, all bounty versions removed

#### **18. Remove Log Entry**
- **Description:** Delete specific ship log entry using composite primary key (Ship_ID + Log_Timestamp)
- **SQL Operation:** `DELETE FROM Log_Entry WHERE Ship_ID = ? AND Log_Timestamp = ?`
- **Input:** Shows table of all log entries, click delete button for specific entry
- **Output:** Confirmation dialog, then success message, log entry removed

#### **19. Remove Fruit Possession**
- **Description:** Delete Devil Fruit possession record (simulates fruit reincarnation after user death)
- **SQL Operation:** `DELETE FROM Devil_Fruit_Possession WHERE Fruit_ID = ?`
- **Input:** Shows table of all current possessions, click delete button
- **Output:** Confirmation dialog, then success message (fruit and person remain, only link deleted)


## 🎨 Special Features

### Theme Toggle
- **Dark Mode (Tactical):** Navy background, cyan text, holographic borders
- **Light Mode (HQ):** Cream background, gold accents, navy text
- Toggle switch in navigation bar
- Persistent across sessions (localStorage)

### Easter Eggs
- Console messages with One Piece quotes
- Loading animations: "Connecting to Den Den Mushi..."
- Success messages: "Database Synchronized", "Justice Served"
- Animated scanline effect on all pages
- Skull animation on Admin Console

### Security Features
- Parameterized queries (prevents SQL injection)
- Role-based access control (Marine vs. Admin)
- Session management
- Password masking on login
- Confirmation dialogs for destructive operations

---

## 📁 File Structure

```
aegis-intelligence-app/
├── src/
│   ├── app.py                          # Main Flask application (1485 lines)
│   ├── db_utils.py                     # Database utility functions
│   ├── schema.sql                      # Database schema creation (19 tables)
│   ├── populate.sql                    # Database population (57 people, 20 islands)
│   ├── requirements.txt                # Python dependencies
│   ├── media/
│   │   └── Marines_Logo.jpeg           # Logo image
│   └── templates/
│       ├── base.html                   # Base template with theme toggle
│       ├── login.html                  # Login page
│       ├── dashboard.html              # Marine dashboard
│       ├── admin_console.html          # CP0 admin console
│       ├── error.html                  # Error page template
│       ├── hubs/
│       │   ├── intelligence.html       # Intelligence hub (7 queries)
│       │   ├── analysis.html           # Tactical analysis hub (3 queries)
│       │   └── operations.html         # Command operations hub (9 operations)
│       ├── intel/
│       │   ├── pirate_search.html      # Query 1
│       │   ├── devil_fruits.html       # Query 2
│       │   ├── marine_directory.html   # Query 3
│       │   ├── bounty_index.html       # Query 4
│       │   ├── will_of_d.html          # Query 5
│       │   ├── ability_search.html     # Query 6
│       │   └── log_decrypter.html      # Query 7
│       ├── tactical/
│       │   ├── crew_valuation.html     # Query 8
│       │   ├── island_census.html      # Query 9
│       │   └── most_wanted.html        # Query 10 (simplified)
│       ├── operations/
│       │   ├── register_criminal.html  # INSERT 1 (Op 11)
│       │   ├── issue_bounty.html       # INSERT 2 (Op 12)
│       │   ├── log_fruit.html          # INSERT 3 (Op 13)
│       │   ├── change_status.html      # UPDATE 1 (Op 14)
│       │   ├── update_bounty.html      # UPDATE 2 (Op 15)
│       │   ├── consume_fruit.html      # UPDATE 3 (Op 16)
│       │   ├── revoke_bounty.html      # DELETE 1 (Op 17)
│       │   ├── remove_log_entry.html   # DELETE 2 (Op 18)
│       │   └── remove_fruit_possession.html  # DELETE 3 (Op 19)
│       └── admin/
│           └── view_tables.html        # Admin DDL operations
├── README.md                           # This file
└── phase3.pdf
└── team33.mp4

```

---

## 🗄️ Database Schema (19 Tables)

| Table | Description | Type |
|-------|-------------|------|
| Person | Superclass for all individuals | Strong Entity |
| Pirate | Pirate-specific attributes | Subclass (ISA) |
| Marine_Officer | Marine-specific attributes | Subclass (ISA) |
| Civilian | Civilian-specific attributes | Subclass (ISA) |
| Crew | Pirate crew information | Strong Entity |
| Faction | Major political powers | Strong Entity |
| Ship | Vessels for sea travel | Strong Entity |
| Island | Landmasses in the world | Strong Entity |
| Sea_Region | Major seas (6 regions) | Strong Entity |
| Devil_Fruit | Mystical fruits with powers | Strong Entity |
| Abilities | Special powers/skills | Strong Entity |
| Event | Major story arcs | Strong Entity |
| Territory | Island control (XOR constraint) | Strong Entity |
| Membership | Person-Crew relationship | Relationship |
| Person_Abilities | Multi-valued attribute | Relationship |
| Participation | Person-Event relationship | Relationship |
| Devil_Fruit_Possession | 1:1 Fruit-Person (PK on Fruit_ID) | Relationship |
| Bounty_Record | Wanted posters (Weak Entity) | Weak Entity |
| Log_Entry | Ship logs (Weak Entity, composite PK) | Weak Entity |

**Schema Highlights:**
- **Generalization:** Person → Pirate/Marine/Civilian (ISA hierarchy)
- **Weak Entities:** Bounty_Record, Log_Entry
- **XOR Constraint:** Territory controlled by Faction OR Crew (not both)
- **Multi-valued Attributes:** Person_Abilities
- **1:1 Relationship:** Devil_Fruit_Possession (one fruit, one person)
- **Composite Keys:** Log_Entry (Ship_ID + Log_Timestamp)
- **Version Tracking:** Bounty_Record (Person_ID + Record_Version)

---

## 🎯 Key Technical Features

- **19 Main Operations** - 7 Intel queries + 3 Tactical queries + 9 Command operations (INSERT/UPDATE/DELETE)
- **Raw SQL Queries** - No ORM, all queries written in pure SQL with parameterized inputs
- **Role-Based Access Control** - Multiple user roles with appropriate permissions
- **Theme Toggle** - Dark/Light mode with persistent localStorage state
- **Real-Time Feedback** - Inline success/error messages with color coding
- **Referential Integrity** - All foreign keys enforced with CASCADE options
- **XOR Constraint** - Territory table enforces Faction OR Crew control
- **Multi-Version Tracking** - Bounty_Record maintains complete history
- **Composite Keys** - Log_Entry demonstrates composite primary key handling
- **Transaction Safety** - Multi-table inserts wrapped in transactions

---

## 🎥 Video Demonstration Checklist

Use this checklist during your screen recording to demonstrate all 19 main operations:

### Marine Officer Demo (MARINE_HQ)
- [ ] 1. Login as MARINE_HQ
- [ ] 2. Dashboard Overview + Theme Toggle
- [ ] 3. Pirate Search (with filters)
- [ ] 4. Devil Fruit Encyclopedia
- [ ] 5. Marine Directory
- [ ] 6. Bounty Index
- [ ] 7. Will of D Search
- [ ] 8. Ability Search
- [ ] 9. Ship Log Decrypter
- [ ] 10. Crew Valuation (show aggregation)
- [ ] 11. Island Census (GROUP BY demo)
- [ ] 12. Most Wanted (simplest query)
- [ ] 13. Register Criminal - INSERT (MySQL before/after)
- [ ] 14. Issue Bounty - INSERT (MySQL before/after)
- [ ] 15. Log Devil Fruit - INSERT (MySQL before/after)
- [ ] 16. Update Person Status - UPDATE (MySQL before/after)
- [ ] 17. Update Bounty - UPDATE (MySQL before/after)
- [ ] 18. Update Fruit Possession - UPDATE (MySQL before/after)
- [ ] 19. Revoke Bounty - DELETE (MySQL before/after)
- [ ] 20. Remove Log Entry - DELETE (MySQL before/after)
- [ ] 21. Remove Fruit Possession - DELETE (MySQL before/after)

---

## 🐛 Troubleshooting

### Database Connection Issues
```bash
# Check MySQL service is running
sudo systemctl status mysql

# Verify credentials
mysql -u root -p
```

### Port 5000 Already in Use
```bash
# Find and kill process
lsof -ti:5000 | xargs kill -9
```

### Template Not Found Errors
```bash
# Ensure you're running from src/ directory
cd src
python app.py
```

### Schema Changes Not Reflecting
```bash
# Re-run schema and populate scripts
mysql -u root -p
source src/schema.sql
source src/populate.sql
```

---

## 📞 Contact

**Team Big Three** - DnA Course Project, Phase 4

For technical support or questions:
- Meet Parekh: 2024101122
- Jainam Modi: 2024101057
- Divya Padariya: 2024113010

---

## 🏴‍☠️ Easter Eggs & Quotes

Explore the application to find hidden One Piece references:
- Console messages with character quotes
- "Den Den Mushi" loading animations
- "Justice Served" success messages
- Animated skull effects
- Scanline CRT effect on all pages

---

**⚓ Justice Will Prevail ⚓**

*Aegis Intelligence Database - Phase 4 Final Submission*

**Total Operations Demonstrated: 19 (7 Intel + 3 Tactical + 9 Command Operations)**


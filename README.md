# Aegis Intelligence Database (AID)# AEGIS Intelligence Database (AID)# aegis-intelligence-app



**World Government Intelligence Terminal - One Piece Universe**DnA Course Project, for application interface to interact with the data of our selected mini world "One Piece".

**Members:** Meet Parekh (2024101122), Jainam Modi (2024101057), Divya Padariya (2024113010)

**Team Big Three** | Phase 4 Final Submission | November 2025

---

## 🚀 Installation

### Prerequisites

- Python 3.8+
- MySQL Server 8.0+

## 🚀 Quick Start

### Setup Steps

---

1. **Create Virtual Environment** (Optional but Recommended)

   ```bash

   python3 -m venv venv

   source venv/bin/activate  # On Windows: venv\Scripts\activate-

   ```

2. **Install Dependencies**
  ```bash
  
  pip install -r src/requirements.txt

  ```



3. **Setup Database**

   ```bash

   mysql -u root -p < src/schema.sql
   mysql -u root -p < src/populate.sql

   ```



4. **Run Application**

   ```bash

    cd src

   python3 app.py

   ```



Access at: `http://127.0.0.1:5000`mysql -u root -p- **Password:** `<your mysql password>`


| Role | Username | Password | Access |### CP0 Administrator (DBA)

|------|----------|----------|--------|

| Marine Officer | `MARINE_HQ` | `SEAGULL` | 5 Queries + 3 Updates |# Run application- **Username:** `ROB_LUCCI`

| CP0 Admin | `ROB_LUCCI` | `DARK_JUSTICE` | All + DDL Operations |

cd src- **Password:** `DARK_JUSTICE`

---

python app.py- **Access Level:** All Marine permissions + DDL operations (DROP, TRUNCATE, ALTER)

## 📋 Application Features

```

### READ OPERATIONS (Queries 1-5)

---

**1. Wanted Poster Search** - Search pirates by name, bounty, or region  

**2. Devil Fruit Encyclopedia** - Browse all Devil Fruits with filtering  Access at: `http://127.0.0.1:5000`

**3. Territory Control Map** - View island control (XOR: Faction OR Crew)  

**4. Crew Manifest** - Complete crew dossier with members and bounties  ## 🚀 Installation & Setup

**5. Regional Threat Report** - Pirate activity analysis per sea region

---

### WRITE OPERATIONS (Updates 1-3)

### Prerequisites

**6. Register New Criminal** - INSERT new pirate with crew membership  

**7. Update Person Status** - UPDATE operational status (Active/Captured/Deceased)  ## 🔐 Login Credentials- Python 3.8+

**8. Revoke Bounty** - DELETE bounty records

- MySQL Server 8.0+

### ADMIN OPERATIONS (DDL - CP0 Only)

| Role | Username | Password | Access |- pip (Python package manager)

**9. View All Tables** - Display database structure with row counts  

**10. Truncate Table** - Remove all data from specified table  |------|----------|----------|--------|

**11. Alter Schema** - Execute custom DDL (ALTER, CREATE INDEX)  

**12. Buster Call Protocol** - Drop all database tables| Marine Officer | `MARINE_HQ` | `SEAGULL` | 5 Queries + 3 Updates |### Step 1: Install Dependencies



---| CP0 Admin | `ROB_LUCCI` | `DARK_JUSTICE` | All + DDL Operations |```bash



## 📁 File Structurepip install flask pymysql



```---```

aegis-intelligence-app/

├── src/

│   ├── app.py              # Main Flask application (1426 lines, 28 routes)

│   ├── db_utils.py         # Database utilities## 📋 Application Features (Video Demo Order)### Step 2: Setup Database

│   ├── schema.sql          # CREATE TABLE statements

│   ├── populate.sql        # INSERT statements```bash

│   ├── requirements.txt    # Python dependencies

│   └── templates/          # 28 HTML templates### READ OPERATIONS (Queries 1-5)# Login to MySQL

│       ├── base.html       # Base template with theme toggle

│       ├── login.html      # Login pagemysql -u root -p

│       ├── dashboard.html  # Marine dashboard

│       ├── admin_console.html  # CP0 admin console**1. Wanted Poster Search**

│       ├── hubs/           # Intelligence/Tactical/Operations hubs

│       ├── intel/          # Query templates- Path: Intelligence Hub → Pirate Search# Execute schema and populate scripts

│       ├── tactical/       # Analysis templates

│       ├── operations/     # Update templates- Search pirates by name, bounty range, or sea regionsource src/schema.sql

│       └── admin/          # Admin templates

├── README.md- SQL: `SELECT` with `JOIN` (Person, Pirate, Crew, Membership, Bounty_Record)source src/populate.sql

└── media/

    └── Marines_Logo.jpeg```

```

**2. Devil Fruit Encyclopedia**

---

- Path: Intelligence Hub → Devil Fruit Encyclopedia### Step 3: Run Application

## 🗄️ Database Schema

- Browse all Devil Fruits with filtering (Type: Paramecia/Zoan/Logia, Awakened status)```bash

**19 Tables** implementing:

- Generalization (Person → Pirate/Marine/Civilian)- SQL: `SELECT` with `LEFT JOIN` (Devil_Fruit, Possession, Person)cd src

- Weak Entities (Bounty_Record, Log_Entry)

- XOR Constraint (Territory: Faction XOR Crew)python app.py

- Multi-valued Attributes (Person_Abilities)

- Complex Relationships (Membership, Participation, Possession)**3. Territory Control Map**```



---- Path: Tactical Analysis Hub → Island Census



## 🎥 Video Demo Checklist- View island control by Crews or Factions (XOR constraint demonstration)When prompted, enter your MySQL root password.



### Part 1: Marine Officer (MARINE_HQ)- SQL: `SELECT` with multiple `JOIN`s and `CASE` statements

- [ ] Login and Dashboard

- [ ] Query 1: Pirate Search### Step 4: Access Application

- [ ] Query 2: Devil Fruit Encyclopedia

- [ ] Query 3: Territory Control**4. Crew Manifest**Open your browser and navigate to:

- [ ] Query 4: Crew Manifest

- [ ] Query 5: Regional Threat Analysis- Path: Tactical Analysis Hub → Crew Valuation```

- [ ] Update 1: Register Criminal (INSERT) - show MySQL before/after

- [ ] Update 2: Update Status (UPDATE) - show MySQL before/after- Complete crew dossier: members, ship, total bounty calculationhttp://127.0.0.1:5000

- [ ] Update 3: Revoke Bounty (DELETE) - show MySQL before/after

- SQL: `SELECT` with aggregations (`COUNT`, `SUM`, `AVG`, `MAX`)```

### Part 2: CP0 Administrator (ROB_LUCCI)

- [ ] Logout and Login as Admin

- [ ] View All Tables

- [ ] Truncate Table - show MySQL before/after**5. Regional Threat Report**---

- [ ] Alter Schema - show MySQL before/after

- [ ] Buster Call Protocol (DROP ALL) - show MySQL before/after- Path: Tactical Analysis Hub → Regional Average



---- Pirate activity analysis per sea region## 📋 Application Features (Video Demonstration Order)



## 🎯 Key Features- SQL: `SELECT` with `GROUP BY` and aggregate functions



- **28 Unique Routes** - All functional requirements implemented### 🔵 PART 1: MARINE OFFICER OPERATIONS (User: MARINE_HQ)

- **Raw SQL Queries** - No ORM, parameterized queries for security

- **Role-Based Access** - Marine vs Admin permissions### WRITE OPERATIONS (Updates 1-3)

- **Theme Toggle** - Dark/Light mode with persistent state

- **Real-Time Feedback** - Inline success/error messages#### **1. LOGIN**

- **Referential Integrity** - All foreign keys enforced with CASCADE

**6. Register New Criminal (INSERT)**- Access the login page

---

- Path: Command Operations Hub → Register Criminal- Enter username: `MARINE_HQ`

## 🐛 Troubleshooting

- Add new pirate with crew membership- Enter password: `SEAGULL`

### Database Connection Issues

```bash- SQL: `INSERT INTO Person, Pirate, Membership`- Successfully authenticate and redirect to dashboard

# Check MySQL service

sudo systemctl status mysql- MySQL Verification:



# Test connection  ```sql#### **2. DASHBOARD OVERVIEW**

mysql -u root -p

```  -- Before/After- View the main operations dashboard



### Port 5000 Already in Use  SELECT * FROM Person ORDER BY Person_ID DESC LIMIT 1;- See all available query and update operations

```bash

# Kill process on port 5000  ```- Demonstrate theme toggle (Dark ↔ Light mode)

lsof -ti:5000 | xargs kill -9

```



---**7. Update Person Status (UPDATE)**---



**⚓ Justice Will Prevail ⚓**- Path: Command Operations Hub → Update Status



*Aegis Intelligence Database - Phase 4 Final Submission*- Change operational status (Active/Captured/Deceased/Unknown)### 📊 READ OPERATIONS (Queries)


- SQL: `UPDATE Person SET Status = ?`

- MySQL Verification:#### **3. WANTED POSTER SEARCH**

  ```sql- **Location:** Dashboard → "Wanted Poster Search"

  -- Before/After- **Functionality:** Search pirates by name or bounty range

  SELECT Person_ID, First_Name, Status FROM Person WHERE Person_ID = ?;- **SQL Operation:** `SELECT` with `JOIN` (Person, Pirate, Crew, Membership)

  ```- **Demo Steps:**

  1. Search without filters (show all pirates)

**8. Revoke Bounty (DELETE)**  2. Search by name (e.g., "Luffy")

- Path: Command Operations Hub → Revoke Bounty  3. Search by bounty range (e.g., 100,000,000 - 500,000,000)

- Remove all bounty records for a person- **Expected Output:** Table showing Person_ID, Name, Bounty, Infamy Level, Status, Crew

- SQL: `DELETE FROM Bounty_Record WHERE Person_ID = ?`

- MySQL Verification:#### **4. DEVIL FRUIT ENCYCLOPEDIA**

  ```sql- **Location:** Dashboard → "Devil Fruit Encyclopedia"

  -- Before/After- **Functionality:** List all Devil Fruits and their current users

  SELECT * FROM Bounty_Record WHERE Person_ID = ?;- **SQL Operation:** `SELECT` with `LEFT JOIN` (Devil_Fruit, Possesses, Person)

  ```- **Demo Steps:**

  1. Click to view all fruits

### ADMIN OPERATIONS (DDL)  2. Show fruits with users vs. unclaimed fruits

  3. Highlight awakened Devil Fruits

**9. View All Tables**- **Expected Output:** Table showing Fruit_ID, Name, Type, Description, Awakened Status, Current User

- Display database structure with row counts

- SQL: `SHOW TABLES`, `SELECT COUNT(*)`#### **5. TERRITORY CONTROL MAP**

- **Location:** Dashboard → "Territory Control Map"

**10. Truncate Table**- **Functionality:** Display islands and their controllers (XOR constraint: Faction OR Crew)

- Remove all data from specified table- **SQL Operation:** `SELECT` with multiple `JOIN`s and `CASE` statement

- SQL: `TRUNCATE TABLE ?`- **Demo Steps:**

  1. View all islands

**11. Alter Schema**  2. Show islands controlled by Factions

- Execute custom DDL (ALTER, CREATE INDEX, DROP INDEX)  3. Show islands controlled by Crews

- SQL: User-defined DDL commands  4. Show unclaimed territories

- **Expected Output:** Table showing Island, Region, Population, Controller Name, Controller Type

**12. Buster Call Protocol**

- Drop all database tables (requires confirmation: `EXECUTE_BUSTER_CALL`)#### **6. CREW MANIFEST**

- SQL: `DROP TABLE` (multiple)- **Location:** Dashboard → "Crew Manifest"

- **Functionality:** Detailed crew dossier with members, ship, and total bounty

---- **SQL Operation:** Multiple `SELECT` queries with aggregation

- **Demo Steps:**

## 📁 File Structure  1. Select a crew from dropdown

  2. View crew information and ship details

```  3. Show all crew members with their bounties

aegis-intelligence-app/  4. Display aggregated total bounty

├── src/- **Expected Output:** Crew info card + members table + total bounty calculation

│   ├── app.py              # Main Flask application (1426 lines)

│   ├── db_utils.py         # Database utilities#### **7. REGIONAL THREAT REPORT**

│   ├── schema.sql          # CREATE TABLE statements- **Location:** Dashboard → "Regional Threat Report"

│   ├── populate.sql        # INSERT statements- **Functionality:** Pirate activity analysis by sea region

│   └── templates/          # 28 HTML templates- **SQL Operation:** `SELECT` with `GROUP BY` and aggregate functions (COUNT, SUM, AVG, MAX)

│       ├── base.html- **Demo Steps:**

│       ├── login.html  1. View all regions summary

│       ├── dashboard.html  2. Select specific region for detailed analysis

│       ├── admin_console.html  3. Show pirate count, total bounties, and threat level

│       ├── hubs/           # Intelligence/Tactical/Operations hubs- **Expected Output:** Table showing Region, Threat Level, Pirate Count, Total/Avg/Max Bounties

│       ├── intel/          # Query templates

│       ├── tactical/       # Analysis templates---

│       ├── operations/     # Update templates

│       ├── updates/        # Status update template### ✏️ WRITE OPERATIONS (Updates)

│       └── admin/          # Admin templates

└── README.md#### **8. REGISTER NEW CRIMINAL (INSERT)**

```- **Location:** Dashboard → "Register Criminal"

- **Functionality:** Add a new pirate to the database

---- **SQL Operation:** `INSERT INTO Person` + `INSERT INTO Pirate`

- **Demo Steps:**

## 🎯 Key Features  1. Before: Run query in MySQL terminal to show current pirates

     ```sql

- **28 Unique Routes** - All functional requirements implemented     SELECT * FROM Person WHERE Person_ID = (SELECT MAX(Person_ID) FROM Person);

- **Raw SQL Queries** - No ORM, parameterized queries for security     ```

- **Role-Based Access** - Marine vs Admin permissions  2. In app: Fill form with new pirate details

- **Theme Toggle** - Dark/Light mode with persistent state     - First Name: Test

- **Real-Time Feedback** - Inline success/error messages     - Last Name: Pirate

- **Referential Integrity** - All foreign keys enforced with CASCADE     - Date of Birth: 2000-01-01

- **XOR Constraint** - Territory controlled by Faction OR Crew (not both)     - Bounty: 50000000

- **Multi-Version Bounties** - Historical bounty tracking system     - Infamy Level: Regional Menace

  3. Submit form

---  4. After: Re-run same query in MySQL terminal to confirm insertion



## 🗄️ Database Schema Highlights#### **9. UPDATE PERSON STATUS (UPDATE)**

- **Location:** Dashboard → "Update Status"

**19 Tables** implementing:- **Functionality:** Change a person's operational status

- Generalization (Person → Pirate/Marine/Civilian)- **SQL Operation:** `UPDATE Person SET Status = ?`

- Weak Entities (Bounty_Record, Log_Entry)- **Demo Steps:**

- XOR Constraint (Territory: Faction XOR Crew)  1. Before: Check person's current status in MySQL

- Multi-valued Attributes (Person_Abilities)     ```sql

- Complex Relationships (Membership, Participation, Possession)     SELECT Person_ID, First_Name, Last_Name, Status FROM Person WHERE Person_ID = 1;

     ```

---  2. In app: Select person and change status (e.g., Active → Captured)

  3. Submit update

## 🎥 Video Demo Checklist  4. After: Re-run query to confirm status change



- [ ] Login as MARINE_HQ → Show Dashboard#### **10. REVOKE BOUNTY RECORD (DELETE)**

- [ ] Query 1: Pirate Search- **Location:** Dashboard → "Revoke Bounty"

- [ ] Query 2: Devil Fruit Encyclopedia- **Functionality:** Delete a specific bounty record

- [ ] Query 3: Island Census- **SQL Operation:** `DELETE FROM Bounty_Record`

- [ ] Query 4: Crew Valuation- **Demo Steps:**

- [ ] Query 5: Regional Analysis  1. Before: Show all bounty records in MySQL

- [ ] **MySQL Terminal** → Before state     ```sql

- [ ] Update 1: Register Criminal (INSERT)     SELECT * FROM Bounty_Record;

- [ ] **MySQL Terminal** → After state (confirm insert)     ```

- [ ] **MySQL Terminal** → Before state  2. In app: View bounty records table

- [ ] Update 2: Update Status (UPDATE)  3. Click delete button on a specific record

- [ ] **MySQL Terminal** → After state (confirm update)  4. Confirm deletion

- [ ] **MySQL Terminal** → Before state  5. After: Re-run query to show record is removed

- [ ] Update 3: Revoke Bounty (DELETE)

- [ ] **MySQL Terminal** → After state (confirm delete)---

- [ ] Logout → Login as ROB_LUCCI

- [ ] Admin: View Tables### 🔴 PART 2: CP0 ADMINISTRATOR OPERATIONS (User: ROB_LUCCI)

- [ ] Admin: Truncate Table (with MySQL verification)

- [ ] Admin: Alter Schema (with MySQL verification)#### **11. LOGOUT & LOGIN AS ADMIN**

- Logout from Marine account

---- Login with CP0 credentials

  - Username: `ROB_LUCCI`

## 📞 Team Contact  - Password: `DARK_JUSTICE`

- Redirected to red-themed Admin Console

**Team Big Three**

- Meet Parekh (2024101122)#### **12. ADMIN CONSOLE OVERVIEW**

- Jainam Modi (2024101057)- View CP0 administrative interface

- Divya Padariya (2024113010)- Show red alert theme

- Explain DDL operation capabilities

---

---

**⚓ JUSTICE WILL PREVAIL ⚓**

### 🛠️ DDL OPERATIONS (Admin Only)

#### **13. VIEW ALL TABLES**
- **Location:** Admin Console → "View Tables"
- **Functionality:** Display all tables and row counts
- **SQL Operation:** `SHOW TABLES` + `SELECT COUNT(*)`
- **Demo Steps:**
  1. Click "View All Tables"
  2. Show complete table list with row counts
  3. Explain database structure

#### **14. TRUNCATE TABLE**
- **Location:** Admin Console → "Truncate Table"
- **Functionality:** Remove all data from a table while preserving structure
- **SQL Operation:** `TRUNCATE TABLE`
- **Demo Steps:**
  1. Before: Show table has data
     ```sql
     SELECT COUNT(*) FROM Log_Entry;
     ```
  2. In app: Enter table name (e.g., "Log_Entry")
  3. Submit truncation
  4. After: Confirm table is empty but still exists
     ```sql
     SELECT COUNT(*) FROM Log_Entry;
     SHOW TABLES LIKE 'Log_Entry';
     ```

#### **15. ALTER TABLE (Schema Alteration)**
- **Location:** Admin Console → "Schema Alteration"
- **Functionality:** Execute custom DDL commands
- **SQL Operation:** `ALTER TABLE`, `CREATE INDEX`, `DROP INDEX`
- **Demo Steps:**
  1. Before: Show table structure
     ```sql
     DESCRIBE Person;
     ```
  2. In app: Enter DDL command
     ```sql
     ALTER TABLE Person ADD COLUMN Execution_Date DATE
     ```
  3. Execute alteration
  4. After: Confirm column was added
     ```sql
     DESCRIBE Person;
     ```

#### **16. BUSTER CALL PROTOCOL (DROP ALL TABLES)**
- **Location:** Admin Console → "Buster Call Protocol"
- **Functionality:** Nuclear option - drop all tables
- **SQL Operation:** `DROP TABLE` (multiple)
- **Demo Steps:**
  1. Before: Show tables exist
     ```sql
     SHOW TABLES;
     ```
  2. In app: Enter confirmation code: `EXECUTE_BUSTER_CALL`
  3. Confirm in popup dialog
  4. Execute Buster Call
  5. After: Confirm all tables are gone
     ```sql
     SHOW TABLES;
     ```

---

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
│   ├── app.py                          # Main Flask application
│   ├── db_utils.py                     # Database utility functions
│   ├── schema.sql                      # Database schema creation
│   ├── populate.sql                    # Database population
│   └── templates/
│       ├── base.html                   # Base template with theme toggle
│       ├── login.html                  # Login page
│       ├── dashboard.html              # Marine dashboard
│       ├── admin_console.html          # CP0 admin console
│       ├── error.html                  # Error page template
│       ├── queries/
│       │   ├── wanted_poster.html      # Query 1: Pirate search
│       │   ├── devil_fruits.html       # Query 2: Devil Fruit encyclopedia
│       │   ├── territory_map.html      # Query 3: Territory control
│       │   ├── crew_manifest.html      # Query 4: Crew details
│       │   └── threat_report.html      # Query 5: Regional threats
│       ├── updates/
│       │   ├── register_criminal.html  # Update 1: INSERT
│       │   ├── change_status.html      # Update 2: UPDATE
│       │   └── revoke_bounty.html      # Update 3: DELETE
│       └── admin/
│           └── view_tables.html        # Admin: View tables
├── README.md                           # This file
└── media/
    └── Marines_Logo.jpeg               # (Optional) Logo image
```

---

## 🗄️ Database Schema (Key Tables)

| Table | Description | Type |
|-------|-------------|------|
| Person | Superclass for all individuals | Strong Entity |
| Pirate | Pirate-specific attributes | Subclass |
| Marine_Officer | Marine-specific attributes | Subclass |
| Civilian | Civilian-specific attributes | Subclass |
| Crew | Pirate crew information | Strong Entity |
| Faction | Major political powers | Strong Entity |
| Ship | Vessels for sea travel | Strong Entity |
| Island | Landmasses in the world | Strong Entity |
| Sea_Region | Major seas (East Blue, Grand Line, etc.) | Strong Entity |
| Devil_Fruit | Mystical fruits with powers | Strong Entity |
| Territory | Island control (XOR: Faction OR Crew) | Strong Entity |
| Event | Major story arcs | Strong Entity |
| Bounty_Record | Wanted posters | Weak Entity |
| Log_Entry | Ship's log records | Weak Entity |

---

## 🎥 Video Demonstration Checklist

Use this checklist during your screen recording:

- [ ] 1. Login as MARINE_HQ
- [ ] 2. Show Dashboard
- [ ] 3. Demonstrate Theme Toggle
- [ ] 4. Wanted Poster Search (before/after in MySQL)
- [ ] 5. Devil Fruit Encyclopedia
- [ ] 6. Territory Control Map
- [ ] 7. Crew Manifest
- [ ] 8. Regional Threat Report
- [ ] 9. Register Criminal - INSERT (MySQL before/after)
- [ ] 10. Update Status - UPDATE (MySQL before/after)
- [ ] 11. Revoke Bounty - DELETE (MySQL before/after)
- [ ] 12. Logout and Login as ROB_LUCCI
- [ ] 13. Admin Console Overview
- [ ] 14. View All Tables
- [ ] 15. Truncate Table (MySQL before/after)
- [ ] 16. Alter Schema (MySQL before/after)
- [ ] 17. Buster Call Protocol (MySQL before/after)

---

## 🐛 Troubleshooting

### Database Connection Issues
```python
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

---

## 📞 Contact

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
- Rob Lucci's "Dark Justice" theme
- Animated skull on Admin Console

---

**⚓ Justice Will Prevail ⚓**

*Aegis Intelligence Database - Phase 4 Final Submission*

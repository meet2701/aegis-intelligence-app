# aegis-intelligence-app
DnA Course Project, for application interface to interact with the data of our selected mini world "One Piece".
# Aegis Intelligence Database (AID) - Phase 4

**Team:** Big Three  
**Members:** Meet Parekh (2024101122), Jainam Modi (2024101057), Divya Padariya (2024113010)  
**Submission Date:** November 20, 2025

---

## 🎯 Project Overview

The **Aegis Intelligence Database (AID)** is a comprehensive intelligence management system for the World Government in the One Piece universe. This Flask-based application provides real-time access to pirate intelligence, territory control, Devil Fruit information, and operational data through an immersive military-grade terminal interface.

---

## 🔐 User Credentials

### Marine Officer (Standard User)
- **Username:** `MARINE_HQ`
- **Password:** `SEAGULL`
- **Access Level:** Read operations (5 queries) + Write operations (3 updates)

### CP0 Administrator (DBA)
- **Username:** `ROB_LUCCI`
- **Password:** `DARK_JUSTICE`
- **Access Level:** All Marine permissions + DDL operations (DROP, TRUNCATE, ALTER)

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- MySQL Server 8.0+
- pip (Python package manager)

### Step 1: Install Dependencies
```bash
pip install flask pymysql
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

## 📋 Application Features (Video Demonstration Order)

### 🔵 PART 1: MARINE OFFICER OPERATIONS (User: MARINE_HQ)

#### **1. LOGIN**
- Access the login page
- Enter username: `MARINE_HQ`
- Enter password: `SEAGULL`
- Successfully authenticate and redirect to dashboard

#### **2. DASHBOARD OVERVIEW**
- View the main operations dashboard
- See all available query and update operations
- Demonstrate theme toggle (Dark ↔ Light mode)

---

### 📊 READ OPERATIONS (Queries)

#### **3. WANTED POSTER SEARCH**
- **Location:** Dashboard → "Wanted Poster Search"
- **Functionality:** Search pirates by name or bounty range
- **SQL Operation:** `SELECT` with `JOIN` (Person, Pirate, Crew, Membership)
- **Demo Steps:**
  1. Search without filters (show all pirates)
  2. Search by name (e.g., "Luffy")
  3. Search by bounty range (e.g., 100,000,000 - 500,000,000)
- **Expected Output:** Table showing Person_ID, Name, Bounty, Infamy Level, Status, Crew

#### **4. DEVIL FRUIT ENCYCLOPEDIA**
- **Location:** Dashboard → "Devil Fruit Encyclopedia"
- **Functionality:** List all Devil Fruits and their current users
- **SQL Operation:** `SELECT` with `LEFT JOIN` (Devil_Fruit, Possesses, Person)
- **Demo Steps:**
  1. Click to view all fruits
  2. Show fruits with users vs. unclaimed fruits
  3. Highlight awakened Devil Fruits
- **Expected Output:** Table showing Fruit_ID, Name, Type, Description, Awakened Status, Current User

#### **5. TERRITORY CONTROL MAP**
- **Location:** Dashboard → "Territory Control Map"
- **Functionality:** Display islands and their controllers (XOR constraint: Faction OR Crew)
- **SQL Operation:** `SELECT` with multiple `JOIN`s and `CASE` statement
- **Demo Steps:**
  1. View all islands
  2. Show islands controlled by Factions
  3. Show islands controlled by Crews
  4. Show unclaimed territories
- **Expected Output:** Table showing Island, Region, Population, Controller Name, Controller Type

#### **6. CREW MANIFEST**
- **Location:** Dashboard → "Crew Manifest"
- **Functionality:** Detailed crew dossier with members, ship, and total bounty
- **SQL Operation:** Multiple `SELECT` queries with aggregation
- **Demo Steps:**
  1. Select a crew from dropdown
  2. View crew information and ship details
  3. Show all crew members with their bounties
  4. Display aggregated total bounty
- **Expected Output:** Crew info card + members table + total bounty calculation

#### **7. REGIONAL THREAT REPORT**
- **Location:** Dashboard → "Regional Threat Report"
- **Functionality:** Pirate activity analysis by sea region
- **SQL Operation:** `SELECT` with `GROUP BY` and aggregate functions (COUNT, SUM, AVG, MAX)
- **Demo Steps:**
  1. View all regions summary
  2. Select specific region for detailed analysis
  3. Show pirate count, total bounties, and threat level
- **Expected Output:** Table showing Region, Threat Level, Pirate Count, Total/Avg/Max Bounties

---

### ✏️ WRITE OPERATIONS (Updates)

#### **8. REGISTER NEW CRIMINAL (INSERT)**
- **Location:** Dashboard → "Register Criminal"
- **Functionality:** Add a new pirate to the database
- **SQL Operation:** `INSERT INTO Person` + `INSERT INTO Pirate`
- **Demo Steps:**
  1. Before: Run query in MySQL terminal to show current pirates
     ```sql
     SELECT * FROM Person WHERE Person_ID = (SELECT MAX(Person_ID) FROM Person);
     ```
  2. In app: Fill form with new pirate details
     - First Name: Test
     - Last Name: Pirate
     - Date of Birth: 2000-01-01
     - Bounty: 50000000
     - Infamy Level: Regional Menace
  3. Submit form
  4. After: Re-run same query in MySQL terminal to confirm insertion

#### **9. UPDATE PERSON STATUS (UPDATE)**
- **Location:** Dashboard → "Update Status"
- **Functionality:** Change a person's operational status
- **SQL Operation:** `UPDATE Person SET Status = ?`
- **Demo Steps:**
  1. Before: Check person's current status in MySQL
     ```sql
     SELECT Person_ID, First_Name, Last_Name, Status FROM Person WHERE Person_ID = 1;
     ```
  2. In app: Select person and change status (e.g., Active → Captured)
  3. Submit update
  4. After: Re-run query to confirm status change

#### **10. REVOKE BOUNTY RECORD (DELETE)**
- **Location:** Dashboard → "Revoke Bounty"
- **Functionality:** Delete a specific bounty record
- **SQL Operation:** `DELETE FROM Bounty_Record`
- **Demo Steps:**
  1. Before: Show all bounty records in MySQL
     ```sql
     SELECT * FROM Bounty_Record;
     ```
  2. In app: View bounty records table
  3. Click delete button on a specific record
  4. Confirm deletion
  5. After: Re-run query to show record is removed

---

### 🔴 PART 2: CP0 ADMINISTRATOR OPERATIONS (User: ROB_LUCCI)

#### **11. LOGOUT & LOGIN AS ADMIN**
- Logout from Marine account
- Login with CP0 credentials
  - Username: `ROB_LUCCI`
  - Password: `DARK_JUSTICE`
- Redirected to red-themed Admin Console

#### **12. ADMIN CONSOLE OVERVIEW**
- View CP0 administrative interface
- Show red alert theme
- Explain DDL operation capabilities

---

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

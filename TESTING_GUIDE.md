# Quick Testing Guide - Phase 4 Features

## 🚀 Setup Instructions

### 1. Reinitialize Database
```bash
cd /home/meet27/Desktop/SEM_3/DnA/Project/APP/aegis-intelligence-app

# Drop and recreate database
mysql -u root -e "DROP DATABASE IF EXISTS mini_world_db; CREATE DATABASE mini_world_db;"

# Load schema
mysql -u root mini_world_db < src/schema.sql

# Load expanded data
mysql -u root mini_world_db < src/populate.sql
```

### 2. Start Application
```bash
python3 src/app.py
```

### 3. Access Application
- **URL**: http://127.0.0.1:5000
- **User Login**: MARINE_HQ / SEAGULL
- **Admin Login**: ROB_LUCCI / DARK_JUSTICE

---

## 🧪 Testing Checklist

### Feature 1: Faction Power Analysis ⚔️

**Navigation**: Dashboard → "FACTION POWER ANALYSIS"

**Expected Results**:
- ✓ 4 factions displayed:
  - World Government (Leader: Sakazuki Akainu)
  - Four Emperors (Leader: Monkey D. Luffy)
  - Revolutionary Army (Leader: Monkey D. Dragon)
  - Cross Guild (Leader: Buggy The Clown)

- ✓ Metrics for each faction:
  - Allied Crew Count
  - Controlled Territories
  - Total Members
  - Total Bounty (in billions)
  - Average Bounty
  - Highest Individual Bounty

- ✓ Revolutionary Army should show:
  - Total Bounty: ฿5,602,000,000 (Dragon ฿5B + Sabo ฿602M)
  - Highest Bounty: ฿5,000,000,000

- ✓ Four Emperors should show:
  - Multiple allied crews (Straw Hats, Heart Pirates, etc.)
  - Total bounty in tens of billions

**What This Demonstrates**:
- Complex 7-table JOIN query
- Aggregate functions (SUM, AVG, MAX, COUNT)
- LEFT JOINs for optional relationships
- GROUP BY with multiple columns
- Subquery for latest bounty version

---

### Feature 2: Historical Event Summary 📜

**Navigation**: Dashboard → "HISTORICAL EVENT SUMMARY"

**Expected Results**:
- ✓ 7 historical events displayed:
  1. God Valley Incident (1484)
  2. Rocky Port Incident (1520)
  3. Paramount War Preparation (1521)
  4. Summit War of Marineford (1522)
  5. Whole Cake Island Arc (1523)
  6. Raid on Onigashima (1524)
  7. Egghead Incident (1524) - **ONGOING** badge

- ✓ For each event:
  - Start/End dates
  - Duration in days (or ONGOING)
  - Number of involved crews
  - Number of involved marines
  - Location (Island + Region)
  - List of participating crews

- ✓ Statistics cards show:
  - Total Events: 7
  - Ongoing Events: 1
  - Completed Events: 6
  - Average Duration: calculated

**What This Demonstrates**:
- N-ary relationship queries (Encounter)
- Temporal data handling (NULL for ongoing)
- String aggregation (GROUP_CONCAT)
- Calculated fields (DATEDIFF)
- Complex JOINs with Event→Encounter→Crew/Marine/Island

---

### Feature 3: Territory Control (XOR Constraint) 🏝️

**Navigation**: Dashboard → "TERRITORY CONTROL" (in Database Modification Operations)

**Test Cases**:

#### Test Case 1: Valid - Faction Control Only
1. Select Island: "Marineford"
2. Control Level: "Absolute"
3. Select Faction: "World Government"
4. Leave Crew: "-- Select Crew (Option B) --"
5. Click "Assign Territory Control"
6. **Expected**: ✓ Success message, territory updated

#### Test Case 2: Valid - Crew Control Only
1. Select Island: "Wano Country"
2. Control Level: "Liberation"
3. Leave Faction: "-- Select Faction (Option A) --"
4. Select Crew: "Straw Hat Pirates"
5. Click "Assign Territory Control"
6. **Expected**: ✓ Success message, territory updated

#### Test Case 3: Invalid - Both Selected
1. Select Island: "Dawn Island"
2. Select Faction: "World Government"
3. Select Crew: "Straw Hat Pirates"
4. **Observe**: Crew dropdown should be disabled automatically (JavaScript)
5. **If you bypass JS**: Server returns "VIOLATION: Exclusive-OR Constraint"

#### Test Case 4: Invalid - Neither Selected
1. Select Island: "Egghead"
2. Leave both Faction and Crew unselected
3. Click "Assign Territory Control"
4. **Expected**: ❌ "ERROR: You must select either a Faction OR a Crew"

**What This Demonstrates**:
- Application-level constraint enforcement
- Python validation logic
- JavaScript mutual exclusion
- Flash message system
- Explicit NULL setting in SQL
- Form state management

---

## 🗂️ Database Verification Queries

### Check Faction Power Data
```sql
USE mini_world_db;

SELECT 
    f.Faction_Name,
    CONCAT(p.First_Name, ' ', COALESCE(p.Last_Name, '')) AS Leader,
    COUNT(DISTINCT a.Crew_ID) AS Allied_Crews,
    COUNT(DISTINCT t.Island_ID) AS Territories,
    SUM(br.Amount) AS Total_Bounty
FROM Faction f
LEFT JOIN Person p ON f.Leader_ID = p.Person_ID
LEFT JOIN Allegiance a ON f.Faction_ID = a.Faction_ID
LEFT JOIN Territory t ON f.Faction_ID = t.Faction_ID
LEFT JOIN Crew c ON a.Crew_ID = c.Crew_ID
LEFT JOIN Membership m ON c.Crew_ID = m.Crew_ID
LEFT JOIN Pirate pi ON m.Person_ID = pi.Person_ID
LEFT JOIN Bounty_Record br ON pi.Person_ID = br.Person_ID
GROUP BY f.Faction_ID
ORDER BY Total_Bounty DESC;
```

### Check Territory XOR Constraint
```sql
SELECT 
    i.Island_Name,
    t.Control_Level,
    CASE 
        WHEN t.Faction_ID IS NOT NULL THEN CONCAT('Faction: ', f.Faction_Name)
        WHEN t.Crew_ID IS NOT NULL THEN CONCAT('Crew: ', c.Crew_Name)
        ELSE 'ERROR: Neither set!'
    END AS Controller,
    CASE 
        WHEN t.Faction_ID IS NOT NULL AND t.Crew_ID IS NOT NULL THEN '❌ VIOLATION'
        WHEN t.Faction_ID IS NULL AND t.Crew_ID IS NULL THEN '❌ VIOLATION'
        ELSE '✓ Valid'
    END AS XOR_Status
FROM Territory t
JOIN Island i ON t.Island_ID = i.Island_ID
LEFT JOIN Faction f ON t.Faction_ID = f.Faction_ID
LEFT JOIN Crew c ON t.Crew_ID = c.Crew_ID;
```

### Check Bounty Totals by Faction
```sql
SELECT 
    f.Faction_Name,
    CONCAT(p.First_Name, ' ', COALESCE(p.Last_Name, '')) AS Person,
    br.Amount AS Bounty,
    pi.Infamy_Level
FROM Faction f
JOIN Allegiance a ON f.Faction_ID = a.Faction_ID
JOIN Crew c ON a.Crew_ID = c.Crew_ID
JOIN Membership m ON c.Crew_ID = m.Crew_ID
JOIN Pirate pi ON m.Person_ID = pi.Person_ID
JOIN Person p ON pi.Person_ID = p.Person_ID
LEFT JOIN Bounty_Record br ON pi.Person_ID = br.Person_ID
WHERE br.Record_Version = (
    SELECT MAX(Record_Version) FROM Bounty_Record WHERE Person_ID = pi.Person_ID
)
ORDER BY f.Faction_ID, br.Amount DESC;
```

### Check Event Participants
```sql
SELECT 
    e.Event_Name,
    e.Start_Date,
    e.End_Date,
    i.Island_Name AS Location,
    c.Crew_Name,
    CONCAT(p.First_Name, ' ', COALESCE(p.Last_Name, '')) AS Marine
FROM Event e
LEFT JOIN Encounter en ON e.Event_ID = en.Event_ID
LEFT JOIN Island i ON en.Island_ID = i.Island_ID
LEFT JOIN Crew c ON en.Crew_ID = c.Crew_ID
LEFT JOIN Marine_Officer mo ON en.Marine_ID = mo.Person_ID
LEFT JOIN Person p ON mo.Person_ID = p.Person_ID
ORDER BY e.Start_Date DESC;
```

---

## 📊 Expected Data Summary

### Persons: 25 total
- **Emperors**: Luffy, Shanks, Blackbeard, Kaido (deceased), Big Mom (deceased)
- **Marines**: Akainu (Fleet Admiral), Kizaru (Admiral), Fujitora (Admiral)
- **CP0**: Rob Lucci, Stussy
- **Revolutionaries**: Dragon, Sabo
- **Warlords**: Mihawk, Crocodile, Buggy

### Bounties: 20 records
- **Highest**: Dragon (฿5,000,000,000)
- **Emperor Tier**: Kaido ฿4.611B, Big Mom ฿4.388B, Shanks ฿4.048B, Blackbeard ฿3.996B
- **Luffy**: 3 versions (฿30M → ฿1.5B → ฿3B)

### Crews: 8 total
- **Active**: Straw Hats, Heart Pirates, Red Hair Pirates, Blackbeard Pirates, Kid Pirates, Buggy's Delivery
- **Disbanded**: Beasts Pirates, Big Mom Pirates

### Factions: 4 total
- World Government, Four Emperors, Revolutionary Army, Cross Guild

### Events: 7 total
- 6 completed, 1 ongoing (Egghead Incident)

### Devil Fruits: 12 total
- 6 awakened (Nika, Ope Ope, Leopard, Soru Soru, Mochi Mochi, plus one more)

### Ships: 8 total
- Includes Thousand Sunny, Polar Tang, Red Force, Victoria Punk, etc.

---

## 🔍 Troubleshooting

### Issue: Database connection error
**Solution**: Check MySQL service is running
```bash
sudo systemctl status mysql
sudo systemctl start mysql
```

### Issue: "Table doesn't exist" errors
**Solution**: Ensure schema.sql and populate.sql run successfully
```bash
mysql -u root mini_world_db < src/schema.sql
mysql -u root mini_world_db < src/populate.sql
```

### Issue: XOR constraint not working
**Solution**: Check Territory table structure
```sql
DESCRIBE Territory;
-- Should show Faction_ID and Crew_ID as nullable INT columns
```

### Issue: Bounty amounts showing as 0
**Solution**: Verify Bounty_Record has data
```sql
SELECT Person_ID, Record_Version, Amount FROM Bounty_Record;
-- Should show 20 records
```

### Issue: Factions showing NULL leaders
**Solution**: Ensure UPDATE statements in populate.sql executed
```sql
SELECT Faction_Name, Leader_ID FROM Faction;
-- All 4 factions should have Leader_ID values
```

---

## ✅ Success Criteria

Your Phase 4 implementation is successful if:

- [x] Faction Power Analysis displays 4 factions with bounty totals
- [x] Historical Event Summary shows 7 events with proper duration
- [x] Territory Control prevents selecting both faction and crew
- [x] Territory Control shows error when neither selected
- [x] Territory Control successfully updates when one option selected
- [x] Dashboard shows all 3 new operation buttons
- [x] All queries return results without errors
- [x] Database contains 25 persons, 20 bounties, 8 crews, 4 factions

---

## 🎓 Professor Demonstration Script

### 1. Login & Dashboard (30 seconds)
- Show login screen → Enter credentials
- Display dashboard with 10 operation buttons
- Highlight 3 new features added

### 2. Faction Power Analysis (2 minutes)
- Click Faction Power Analysis button
- Point out 7-table JOIN complexity
- Show bounty calculations (billions)
- Highlight metrics: crews, territories, members, bounties
- Explain aggregation functions used

### 3. Historical Event Summary (2 minutes)
- Click Historical Event Summary button
- Show timeline of 7 events
- Point to ONGOING badge on Egghead Incident
- Show statistics cards with calculations
- Explain temporal data handling

### 4. Territory XOR Constraint (3 minutes)
- Click Territory Control button
- **Demonstrate valid case**: Select faction only → Success
- **Demonstrate valid case**: Select crew only → Success
- **Demonstrate invalid case**: Try both → Show error
- **Demonstrate invalid case**: Try neither → Show error
- Explain Python constraint enforcement
- Show JavaScript mutual exclusion feature

### 5. Code Walkthrough (if time permits)
- Open app.py → Show faction_power_report() SQL
- Open populate.sql → Show data richness (25 persons, 20 bounties)
- Open territory_control.html → Show JavaScript validation

**Total Demo Time**: ~8 minutes

---

*Generated for Phase 4 Testing*
*Aegis Intelligence Database - One Piece World*

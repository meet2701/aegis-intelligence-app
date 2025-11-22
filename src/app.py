"""
Aegis Intelligence Database (AID) - Main Application
World Government Intelligence Terminal Interface

Phase 4 - Final Submission
Team: Big Three
"""

from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import pymysql
import sys
from datetime import datetime
from db_utils import DatabaseConnection, format_query_results, get_db_password

app = Flask(__name__)
app.secret_key = 'AEGIS_CLASSIFIED_KEY_DO_NOT_SHARE'  # Change in production

# Global database connection
db = None

# User roles and credentials
USERS = {
    'MARINE_HQ': {
        'password': 'SEAGULL',
        'role': 'marine',
        'full_name': 'Marine Headquarters Officer'
    },
    'ROB_LUCCI': {
        'password': 'DARK_JUSTICE',
        'role': 'admin',
        'full_name': 'CP0 Administrator'
    }
}


def init_database():
    """Initialize database connection at application startup."""
    global db
    
    print("\n" + "="*70)
    print(" █████╗ ███████╗ ██████╗ ██╗███████╗    ██╗███╗   ██╗████████╗")
    print("██╔══██╗██╔════╝██╔════╝ ██║██╔════╝    ██║████╗  ██║╚══██╔══╝")
    print("███████║█████╗  ██║  ███╗██║███████╗    ██║██╔██╗ ██║   ██║   ")
    print("██╔══██║██╔══╝  ██║   ██║██║╚════██║    ██║██║╚██╗██║   ██║   ")
    print("██║  ██║███████╗╚██████╔╝██║███████║    ██║██║ ╚████║   ██║   ")
    print("╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝╚══════╝    ╚═╝╚═╝  ╚═══╝   ╚═╝   ")
    print("="*70)
    print("WORLD GOVERNMENT INTELLIGENCE DATABASE SYSTEM")
    print("CLASSIFIED - AUTHORIZED PERSONNEL ONLY")
    print("="*70 + "\n")
    
    db_password = get_db_password()
    
    db = DatabaseConnection(
        host='localhost',
        user='root',  # Change if different
        password=db_password,
        database='mini_world_db'  # Match the database name in schema.sql
    )
    
    if db.connect():
        print("\n[STATUS] Aegis Intelligence Database is online.")
        print("[STATUS] All systems operational. Justice will prevail.\n")
        return True
    else:
        print("\n[CRITICAL ERROR] Failed to establish database connection.")
        print("[SYSTEM] Application terminating...\n")
        sys.exit(1)


# Authentication Routes

@app.route('/')
def index():
    """Redirect to login if not authenticated, otherwise to appropriate dashboard."""
    if 'username' in session:
        if session.get('role') == 'admin':
            return redirect(url_for('admin_console'))
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user authentication."""
    if request.method == 'POST':
        username = request.form.get('username', '').strip().upper()
        password = request.form.get('password', '').strip()
        
        if username in USERS and USERS[username]['password'] == password:
            session['username'] = username
            session['role'] = USERS[username]['role']
            session['full_name'] = USERS[username]['full_name']
            
            flash(f'Access Granted. Welcome, {session["full_name"]}.', 'success')
            
            if session['role'] == 'admin':
                return redirect(url_for('admin_console'))
            return redirect(url_for('dashboard'))
        else:
            flash('ACCESS DENIED. Invalid credentials.', 'danger')
    
    return render_template('login.html')


@app.route('/logout')
def logout():
    """Log out the current user."""
    username = session.get('username', 'Unknown')
    session.clear()
    flash(f'User {username} logged out. Session terminated.', 'info')
    return redirect(url_for('login'))


# Marine Officer Dashboard Routes

@app.route('/dashboard')
def dashboard():
    """Main dashboard for Marine Officers."""
    if 'username' not in session or session.get('role') != 'marine':
        flash('ACCESS DENIED. Marine credentials required.', 'danger')
        return redirect(url_for('login'))
    
    return render_template('dashboard.html')


# ============================================================================
# PHASE 4: HUB SYSTEM
# ============================================================================

# Hub Landing Pages

@app.route('/hub/intelligence')
def intelligence_hub():
    """Intelligence Hub landing page."""
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('hubs/intelligence.html')


@app.route('/hub/tactical')
def tactical_analysis():
    """Tactical Analysis Hub landing page."""
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('hubs/analysis.html')


@app.route('/hub/command')
def command_operations():
    """Command Operations Hub landing page."""
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('hubs/operations.html')


# ============================================================================
# INTELLIGENCE HUB - Retrieval & Search Operations
# ============================================================================

@app.route('/intel/devil-fruits', methods=['GET', 'POST'])
def devil_fruit_encyclopedia():
    """Devil Fruit Encyclopedia with sorting and filtering options."""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    # Get filter parameters
    fruit_type = request.args.get('fruit_type', 'all')  # all, Paramecia, Zoan, Logia
    sort_by = request.args.get('sort_by', 'type')  # type, fruit_id, name
    show_awakened = request.args.get('show_awakened', '')  # 'on' if checked
    show_active = request.args.get('show_active', '')  # 'on' if checked
    
    # Base query
    sql = """
        SELECT 
            df.Fruit_ID,
            df.Fruit_Name,
            df.Type AS Fruit_Type,
            df.Description,
            df.is_Awakened AS Is_Awakened,
            p.First_Name,
            p.Last_Name,
            p.Status
        FROM Devil_Fruit df
        LEFT JOIN Devil_Fruit_Possession dfp ON df.Fruit_ID = dfp.Fruit_ID
        LEFT JOIN Person p ON dfp.Person_ID = p.Person_ID
        WHERE 1=1
    """
    
    params = []
    
    # Apply fruit type filter
    if fruit_type != 'all':
        sql += " AND df.Type = %s"
        params.append(fruit_type)
    
    # Apply filters
    if show_awakened == 'on':
        sql += " AND df.is_Awakened = TRUE"
    
    if show_active == 'on':
        sql += " AND (p.Status = 'Active' OR p.Status IS NULL)"
    
    # Apply sorting
    if sort_by == 'fruit_id':
        sql += " ORDER BY df.Fruit_ID"
    elif sort_by == 'name':
        sql += " ORDER BY df.Fruit_Name"
    else:  # default: type
        sql += " ORDER BY df.Type, df.Fruit_Name"
    
    results = db.execute_query(sql, tuple(params)) if params else db.execute_query(sql)
    results = format_query_results(results)
    
    return render_template('intel/devil_fruits.html', 
                         results=results,
                         fruit_type=fruit_type,
                         sort_by=sort_by,
                         show_awakened=show_awakened,
                         show_active=show_active)


@app.route('/intel/marine-directory', methods=['GET', 'POST'])
def marine_directory():
    """Marine Officer Directory with Rank filter."""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    rank = request.form.get('rank', '') if request.method == 'POST' else ''
    
    sql = """
        SELECT 
            p.Person_ID,
            CONCAT(p.First_Name, ' ', COALESCE(p.Last_Name, '')) AS Officer_Name,
            mo.`Rank`,
            mo.Service_Number,
            p.Status,
            p.Date_of_Birth
        FROM Person p
        INNER JOIN Marine_Officer mo ON p.Person_ID = mo.Person_ID
    """
    
    if rank:
        sql += " WHERE mo.`Rank` = %s"
        sql += " ORDER BY CASE mo.`Rank`"
        sql += "   WHEN 'Fleet Admiral' THEN 1"
        sql += "   WHEN 'Admiral' THEN 2"
        sql += "   WHEN 'Vice Admiral' THEN 3"
        sql += "   WHEN 'Rear Admiral' THEN 4"
        sql += "   WHEN 'Commodore' THEN 5"
        sql += "   WHEN 'Captain' THEN 6"
        sql += "   ELSE 7 END, p.First_Name"
        results = db.execute_query(sql, (rank,))
    else:
        sql += " ORDER BY CASE mo.`Rank`"
        sql += "   WHEN 'Fleet Admiral' THEN 1"
        sql += "   WHEN 'Admiral' THEN 2"
        sql += "   WHEN 'Vice Admiral' THEN 3"
        sql += "   WHEN 'Rear Admiral' THEN 4"
        sql += "   WHEN 'Commodore' THEN 5"
        sql += "   WHEN 'Captain' THEN 6"
        sql += "   ELSE 7 END, p.First_Name"
        results = db.execute_query(sql)
    
    results = format_query_results(results)
    
    ranks = ['Fleet Admiral', 'Admiral', 'Vice Admiral', 'Rear Admiral', 
             'Commodore', 'Captain', 'Commander', 'Lieutenant']
    
    return render_template('intel/marine_directory.html', 
                         results=results, 
                         rank=rank,
                         ranks=ranks)


@app.route('/intel/bounty-index')
def bounty_index():
    """Simple Pirate Bounty Index."""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    sql = """
        SELECT 
            CONCAT(p.First_Name, ' ', COALESCE(p.Last_Name, '')) AS Pirate_Name,
            COALESCE(br.Amount, 0) AS Bounty
        FROM Person p
        INNER JOIN Pirate pi ON p.Person_ID = pi.Person_ID
        LEFT JOIN Bounty_Record br ON p.Person_ID = br.Person_ID
            AND br.Record_Version = (
                SELECT MAX(Record_Version)
                FROM Bounty_Record
                WHERE Person_ID = p.Person_ID
            )
        ORDER BY Bounty DESC, Pirate_Name
    """
    
    results = db.execute_query(sql)
    results = format_query_results(results)
    
    return render_template('intel/bounty_index.html', results=results)


@app.route('/intel/will-of-d')
def will_of_d_search():
    """Search for persons with 'D.' in their name."""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    sql = """
        SELECT 
            p.Person_ID,
            CONCAT(p.First_Name, ' ', COALESCE(p.Last_Name, '')) AS Full_Name,
            CASE 
                WHEN pi.Person_ID IS NOT NULL THEN 'Pirate'
                WHEN mo.Person_ID IS NOT NULL THEN 'Marine Officer'
                WHEN c.Person_ID IS NOT NULL THEN 'Civilian'
                ELSE 'Unknown'
            END AS Role,
            p.Status,
            COALESCE(br.Amount, 0) AS Bounty
        FROM Person p
        LEFT JOIN Pirate pi ON p.Person_ID = pi.Person_ID
        LEFT JOIN Marine_Officer mo ON p.Person_ID = mo.Person_ID
        LEFT JOIN Civilian c ON p.Person_ID = c.Person_ID
        LEFT JOIN Bounty_Record br ON p.Person_ID = br.Person_ID
            AND br.Record_Version = (
                SELECT MAX(Record_Version)
                FROM Bounty_Record
                WHERE Person_ID = p.Person_ID
            )
        WHERE CONCAT(p.First_Name, ' ', COALESCE(p.Last_Name, '')) LIKE '%%D.%%'
           OR CONCAT(p.First_Name, ' ', COALESCE(p.Last_Name, '')) LIKE '%%D %%'
        ORDER BY Full_Name
    """
    
    results = db.execute_query(sql)
    results = format_query_results(results)
    
    return render_template('intel/will_of_d.html', results=results)


@app.route('/intel/ability-search', methods=['GET', 'POST'])
def ability_search():
    """Search persons by ability with reference list."""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    # Get list of all distinct abilities for reference
    abilities_sql = """
        SELECT DISTINCT Ability 
        FROM Person_Abilities 
        WHERE Ability IS NOT NULL 
        ORDER BY Ability
    """
    abilities = db.execute_query(abilities_sql)
    
    results = None
    search_ability = ''
    
    if request.method == 'POST':
        search_ability = request.form.get('ability', '').strip()
        
        if search_ability:
            sql = """
                SELECT 
                    CONCAT(p.First_Name, ' ', COALESCE(p.Last_Name, '')) AS Person_Name,
                    pa.Ability,
                    CASE 
                        WHEN pi.Person_ID IS NOT NULL THEN 'Pirate'
                        WHEN mo.Person_ID IS NOT NULL THEN 'Marine Officer'
                        ELSE 'Other'
                    END AS Role,
                    p.Status
                FROM Person p
                INNER JOIN Person_Abilities pa ON p.Person_ID = pa.Person_ID
                LEFT JOIN Pirate pi ON p.Person_ID = pi.Person_ID
                LEFT JOIN Marine_Officer mo ON p.Person_ID = mo.Person_ID
                WHERE pa.Ability LIKE %s
                ORDER BY Person_Name
            """
            results = db.execute_query(sql, (f'%{search_ability}%',))
            results = format_query_results(results)
    
    return render_template('intel/ability_search.html', 
                         results=results,
                         abilities=abilities,
                         search_ability=search_ability)


@app.route('/intel/log-search', methods=['GET', 'POST'])
def log_decrypter():
    """Search ship log entries by keyword."""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    results = None
    keyword = ''
    
    if request.method == 'POST':
        keyword = request.form.get('keyword', '').strip()
        
        if keyword:
            sql = """
                SELECT 
                    le.Ship_ID,
                    s.Ship_Name,
                    le.Log_Timestamp,
                    le.Entry_Text,
                    le.Latitude,
                    le.Longitude,
                    c.Crew_Name
                FROM Log_Entry le
                INNER JOIN Ship s ON le.Ship_ID = s.Ship_ID
                LEFT JOIN Crew c ON s.Owning_Crew_ID = c.Crew_ID
                WHERE le.Entry_Text LIKE %s
                ORDER BY le.Log_Timestamp DESC
            """
            results = db.execute_query(sql, (f'%{keyword}%',))
            results = format_query_results(results)
    
    return render_template('intel/log_decrypter.html', 
                         results=results,
                         keyword=keyword)


@app.route('/intel/pirate-search', methods=['GET', 'POST'])
def pirate_search():
    """Search for pirates by name, bounty range, and/or sea region."""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    # Get list of sea regions for dropdown
    regions_sql = "SELECT Region_ID, Region_Name FROM Sea_Region ORDER BY Region_Name"
    regions = db.execute_query(regions_sql)
    
    results = None
    search_type = 'name'  # Default
    search_name = ''
    min_bounty = ''
    max_bounty = ''
    region_id = ''
    
    if request.method == 'POST':
        search_type = request.form.get('search_type', 'name')
        search_name = request.form.get('pirate_name', '').strip()
        min_bounty = request.form.get('min_bounty', '')
        max_bounty = request.form.get('max_bounty', '')
        region_id = request.form.get('region_id', '')
        
        # Base query with latest bounty using subquery
        sql = """
            SELECT 
                p.Person_ID,
                p.First_Name,
                p.Last_Name,
                p.Status,
                pi.Infamy_Level,
                c.Crew_Name,
                sr.Region_Name,
                COALESCE(br.Amount, 0) as Bounty,
                br.Issue_Date as Bounty_Date,
                br.Last_Seen_Location
            FROM Person p
            INNER JOIN Pirate pi ON p.Person_ID = pi.Person_ID
            LEFT JOIN Membership m ON p.Person_ID = m.Person_ID
            LEFT JOIN Crew c ON m.Crew_ID = c.Crew_ID
            LEFT JOIN Island i ON p.Home_Island_ID = i.Island_ID
            LEFT JOIN Sea_Region sr ON i.Region_ID = sr.Region_ID
            LEFT JOIN Bounty_Record br ON p.Person_ID = br.Person_ID 
                AND br.Record_Version = (
                    SELECT MAX(Record_Version) 
                    FROM Bounty_Record 
                    WHERE Person_ID = p.Person_ID
                )
            WHERE 1=1
        """
        
        params = []
        
        # Apply filters based on search type and inputs
        if search_type == 'name' and search_name:
            sql += """ AND (
                CONCAT(p.First_Name, ' ', COALESCE(p.Last_Name, '')) LIKE %s
                OR p.First_Name LIKE %s
                OR p.Last_Name LIKE %s
            )"""
            search_pattern = f"%{search_name}%"
            params.extend([search_pattern, search_pattern, search_pattern])
        
        elif search_type == 'bounty':
            if min_bounty:
                sql += " AND COALESCE(br.Amount, 0) >= %s"
                params.append(int(min_bounty))
            if max_bounty:
                sql += " AND COALESCE(br.Amount, 0) <= %s"
                params.append(int(max_bounty))
        
        elif search_type == 'region' and region_id:
            sql += " AND sr.Region_ID = %s"
            params.append(int(region_id))
        
        sql += " ORDER BY COALESCE(br.Amount, 0) DESC, p.First_Name"
        
        # Execute query
        if params:
            results = db.execute_query(sql, tuple(params))
        else:
            results = db.execute_query(sql)
        results = format_query_results(results)
    
    return render_template('intel/pirate_search.html', 
                         results=results, 
                         regions=regions,
                         search_type=search_type,
                         search_name=search_name,
                         min_bounty=min_bounty,
                         max_bounty=max_bounty,
                         region_id=region_id)


# ============================================================================
# TACTICAL ANALYSIS HUB - Aggregates & Reports
# ============================================================================

@app.route('/tactical/crew-valuation', methods=['GET', 'POST'])
def crew_valuation():
    """Calculate total bounty for a crew."""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    # Get all crews for dropdown
    crews_sql = "SELECT Crew_ID, Crew_Name FROM Crew ORDER BY Crew_Name"
    crews = db.execute_query(crews_sql)
    
    results = None
    crew_id = ''
    
    if request.method == 'POST':
        crew_id = request.form.get('crew_id', '')
        
        if crew_id:
            sql = """
                SELECT 
                    c.Crew_Name,
                    COUNT(DISTINCT m.Person_ID) AS Total_Members,
                    SUM(br.Amount) AS Total_Bounty,
                    AVG(br.Amount) AS Average_Bounty,
                    MAX(br.Amount) AS Highest_Bounty,
                    MIN(br.Amount) AS Lowest_Bounty
                FROM Crew c
                LEFT JOIN Membership m ON c.Crew_ID = m.Crew_ID
                LEFT JOIN Pirate pi ON m.Person_ID = pi.Person_ID
                LEFT JOIN Bounty_Record br ON pi.Person_ID = br.Person_ID
                    AND br.Record_Version = (
                        SELECT MAX(Record_Version)
                        FROM Bounty_Record
                        WHERE Person_ID = pi.Person_ID
                    )
                WHERE c.Crew_ID = %s
                GROUP BY c.Crew_ID, c.Crew_Name
            """
            results = db.execute_query(sql, (crew_id,))
            results = format_query_results(results)
    
    return render_template('tactical/crew_valuation.html', 
                         results=results,
                         crews=crews,
                         crew_id=crew_id)


@app.route('/tactical/regional-average', methods=['GET', 'POST'])
def regional_average():
    """Calculate average bounty by region."""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    # Get all regions for dropdown
    regions_sql = "SELECT Region_ID, Region_Name FROM Sea_Region ORDER BY Region_Name"
    regions = db.execute_query(regions_sql)
    
    results = None
    region_id = ''
    
    if request.method == 'POST':
        region_id = request.form.get('region_id', '')
        
        if region_id:
            sql = """
                SELECT 
                    sr.Region_Name,
                    COUNT(DISTINCT p.Person_ID) AS Total_Pirates,
                    AVG(br.Amount) AS Average_Bounty,
                    MIN(br.Amount) AS Minimum_Bounty,
                    MAX(br.Amount) AS Maximum_Bounty,
                    SUM(br.Amount) AS Total_Regional_Bounty
                FROM Sea_Region sr
                INNER JOIN Island i ON sr.Region_ID = i.Region_ID
                INNER JOIN Person p ON i.Island_ID = p.Home_Island_ID
                INNER JOIN Pirate pi ON p.Person_ID = pi.Person_ID
                LEFT JOIN Bounty_Record br ON p.Person_ID = br.Person_ID
                    AND br.Record_Version = (
                        SELECT MAX(Record_Version)
                        FROM Bounty_Record
                        WHERE Person_ID = p.Person_ID
                    )
                WHERE sr.Region_ID = %s AND p.Status = 'Active'
                GROUP BY sr.Region_ID, sr.Region_Name
            """
            results = db.execute_query(sql, (region_id,))
            results = format_query_results(results)
    
    return render_template('tactical/regional_average.html', 
                         results=results,
                         regions=regions,
                         region_id=region_id)


@app.route('/tactical/island-census')
def island_census():
    """Count islands per region."""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    sql = """
        SELECT 
            sr.Region_Name,
            COUNT(i.Island_ID) AS Island_Count,
            COALESCE(SUM(i.Population), 0) AS Total_Population,
            COALESCE(AVG(i.Population), 0) AS Average_Population,
            GROUP_CONCAT(DISTINCT i.Climate ORDER BY i.Climate SEPARATOR ', ') AS Climate_Types
        FROM Sea_Region sr
        LEFT JOIN Island i ON sr.Region_ID = i.Region_ID
        GROUP BY sr.Region_ID, sr.Region_Name
        ORDER BY Island_Count DESC, sr.Region_Name
    """
    
    results = db.execute_query(sql)
    results = format_query_results(results)
    
    return render_template('tactical/island_census.html', results=results)


@app.route('/tactical/most-wanted')
def most_wanted():
    """Display the highest bounty pirate."""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    sql = """
        SELECT 
            CONCAT(p.First_Name, ' ', COALESCE(p.Last_Name, '')) AS Pirate_Name,
            br.Amount,
            c.Crew_Name,
            i.Island_Name,
            sr.Region_Name,
            p.Status,
            pi.Infamy_Level,
            br.Issue_Date AS Date_Issued
        FROM Person p
        INNER JOIN Pirate pi ON p.Person_ID = pi.Person_ID
        INNER JOIN Bounty_Record br ON p.Person_ID = br.Person_ID
            AND br.Record_Version = (
                SELECT MAX(Record_Version)
                FROM Bounty_Record
                WHERE Person_ID = p.Person_ID
            )
        LEFT JOIN Membership m ON p.Person_ID = m.Person_ID
        LEFT JOIN Crew c ON m.Crew_ID = c.Crew_ID
        LEFT JOIN Island i ON p.Home_Island_ID = i.Island_ID
        LEFT JOIN Sea_Region sr ON i.Region_ID = sr.Region_ID
        WHERE br.Amount > 0
        ORDER BY br.Amount DESC
        LIMIT 1
    """
    
    results = db.execute_query(sql)
    
    # Extract single pirate if results exist
    pirate = None
    if results and isinstance(results, list) and len(results) > 0:
        pirate = results[0]
    
    return render_template('tactical/most_wanted.html', pirate=pirate)


# ============================================================================
# COMMAND OPERATIONS - INSERT/UPDATE/DELETE
# ============================================================================

@app.route('/command/register-criminal', methods=['GET', 'POST'])
def register_criminal():
    """Register a new criminal/pirate to the database."""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    message = None
    message_type = 'success'
    
    if request.method == 'POST':
        try:
            # Get form data
            first_name = request.form.get('first_name', '').strip()
            last_name = request.form.get('last_name', '').strip()
            date_of_birth = request.form.get('date_of_birth', '').strip()
            status = request.form.get('status', 'Unknown')
            home_island_id = request.form.get('home_island_id', '').strip()
            infamy_level = request.form.get('infamy_level', '').strip()
            crew_id = request.form.get('crew_id', '').strip()
            role = request.form.get('role', '').strip()
            
            # Validation
            if not first_name:
                raise ValueError("First name is required")
            
            # Insert into Person table first
            person_sql = """
                INSERT INTO Person (First_Name, Last_Name, Date_of_Birth, Status, Home_Island_ID) 
                VALUES (%s, %s, %s, %s, %s)
            """
            db.execute_update(person_sql, (
                first_name, 
                last_name if last_name else None,
                date_of_birth if date_of_birth else None,
                status,
                int(home_island_id) if home_island_id else None
            ))
            
            # Get the newly inserted Person_ID
            get_id_sql = "SELECT LAST_INSERT_ID() as Person_ID"
            result = db.execute_query(get_id_sql)
            person_id = result[0]['Person_ID']
            
            # Insert into Pirate table
            pirate_sql = """
                INSERT INTO Pirate (Person_ID, Infamy_Level) 
                VALUES (%s, %s)
            """
            db.execute_update(pirate_sql, (person_id, infamy_level if infamy_level else None))
            
            # Insert into Membership table if crew is selected
            if crew_id:
                membership_sql = """
                    INSERT INTO Membership (Person_ID, Crew_ID, Role)
                    VALUES (%s, %s, %s)
                """
                db.execute_update(membership_sql, (person_id, int(crew_id), role if role else None))
            
            full_name = f"{first_name} {last_name}" if last_name else first_name
            message = f"✅ Successfully registered {full_name} (ID: {person_id}) as Pirate"
            message_type = 'success'
            
        except Exception as e:
            message = f"❌ Error: {str(e)}"
            message_type = 'danger'
    
    # Get crews and islands for dropdowns
    crews_sql = "SELECT Crew_ID, Crew_Name FROM Crew ORDER BY Crew_Name"
    crews = db.execute_query(crews_sql)
    
    islands_sql = """
        SELECT i.Island_ID, i.Island_Name, sr.Region_Name 
        FROM Island i 
        JOIN Sea_Region sr ON i.Region_ID = sr.Region_ID 
        ORDER BY i.Island_Name
    """
    islands = db.execute_query(islands_sql)
    
    return render_template('operations/register_criminal.html', 
                         crews=crews, 
                         islands=islands,
                         message=message,
                         message_type=message_type)


@app.route('/command/issue-bounty', methods=['GET', 'POST'])
def issue_bounty():
    """Issue a new bounty for an existing pirate."""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    message = None
    message_type = 'success'
    
    if request.method == 'POST':
        try:
            # Get form data
            person_id = request.form.get('person_id', '').strip()
            amount = request.form.get('amount', '').strip()
            date_issued = request.form.get('date_issued', '').strip()
            
            # Validation
            if not person_id or not amount:
                raise ValueError("Person and bounty amount are required")
            
            person_id = int(person_id)
            amount = int(amount)
            
            if amount < 0:
                raise ValueError("Bounty amount must be positive")
            
            # Check if pirate already has a bounty
            check_sql = """
                SELECT Person_ID FROM Bounty_Record 
                WHERE Person_ID = %s
            """
            existing = db.execute_query(check_sql, (person_id,))
            
            if existing:
                raise ValueError("This pirate already has a bounty. Use 'Update Bounty' to modify it.")
            
            # Insert first bounty record (Record_Version = 1)
            record_sql = """
                INSERT INTO Bounty_Record (Person_ID, Record_Version, Amount, Issue_Date, Last_Seen_Location)
                VALUES (%s, 1, %s, %s, NULL)
            """
            db.execute_update(record_sql, (person_id, amount, date_issued if date_issued else None))
            
            message = f"✅ Successfully issued bounty of ฿{amount:,}"
            message_type = 'success'
            
        except Exception as e:
            message = f"❌ Error: {str(e)}"
            message_type = 'danger'
    
    # Get pirates without bounties
    pirates_sql = """
        SELECT p.Person_ID, 
               CONCAT(p.First_Name, ' ', COALESCE(p.Last_Name, '')) AS Person_Name,
               p.Status
        FROM Pirate pi
        JOIN Person p ON pi.Person_ID = p.Person_ID
        WHERE pi.Person_ID NOT IN (SELECT Person_ID FROM Bounty_Record)
        ORDER BY p.First_Name, p.Last_Name
    """
    pirates = db.execute_query(pirates_sql)
    
    return render_template('operations/issue_bounty.html',
                         pirates=pirates,
                         message=message,
                         message_type=message_type)


@app.route('/command/log-fruit', methods=['GET', 'POST'])
def log_devil_fruit():
    """Log a newly discovered Devil Fruit."""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    message = None
    message_type = 'success'
    
    if request.method == 'POST':
        try:
            # Get form data
            fruit_name = request.form.get('fruit_name', '').strip()
            fruit_type = request.form.get('fruit_type', '').strip()
            description = request.form.get('description', '').strip()
            is_awakened = request.form.get('is_awakened', '') == 'on'
            
            # Validation
            if not fruit_name or not fruit_type:
                raise ValueError("Fruit name and type are required")
            
            if fruit_type not in ['Paramecia', 'Zoan', 'Logia']:
                raise ValueError("Invalid fruit type")
            
            # Check if fruit already exists
            check_sql = "SELECT Fruit_ID FROM Devil_Fruit WHERE Fruit_Name = %s"
            existing = db.execute_query(check_sql, (fruit_name,))
            
            if existing:
                raise ValueError(f"Devil Fruit '{fruit_name}' is already logged in the database")
            
            # Insert Devil Fruit
            fruit_sql = """
                INSERT INTO Devil_Fruit (Fruit_Name, Type, Description, is_Awakened) 
                VALUES (%s, %s, %s, %s)
            """
            db.execute_update(fruit_sql, (fruit_name, fruit_type, description if description else None, is_awakened))
            
            # Get fruit ID
            get_id_sql = "SELECT LAST_INSERT_ID() as Fruit_ID"
            result = db.execute_query(get_id_sql)
            fruit_id = result[0]['Fruit_ID']
            
            awakened_status = " (Awakened)" if is_awakened else ""
            message = f"✅ Successfully logged {fruit_name} ({fruit_type}){awakened_status} - ID: {fruit_id}"
            message_type = 'success'
            
        except Exception as e:
            message = f"❌ Error: {str(e)}"
            message_type = 'danger'
    
    return render_template('operations/log_fruit.html',
                         message=message,
                         message_type=message_type)


@app.route('/command/consume-fruit', methods=['GET', 'POST'])
def consume_devil_fruit():
    """Update Devil Fruit possession - transfer fruit from current user to new user."""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    message = None
    message_type = 'success'
    
    if request.method == 'POST':
        try:
            # Get form data
            fruit_id = request.form.get('fruit_id', '').strip()
            new_person_id = request.form.get('new_person_id', '').strip()
            
            # Validation
            if not fruit_id or not new_person_id:
                raise ValueError("Devil Fruit and New Person are required")
            
            fruit_id = int(fruit_id)
            new_person_id = int(new_person_id)
            
            # Check if new person already has a fruit
            check_person_sql = "SELECT Fruit_ID FROM Devil_Fruit_Possession WHERE Person_ID = %s"
            existing_person = db.execute_query(check_person_sql, (new_person_id,))
            
            if existing_person:
                raise ValueError("The new person already possesses a Devil Fruit. One person can only have one fruit.")
            
            # Get current owner info for message
            current_owner_sql = """
                SELECT dfp.Person_ID, 
                       CONCAT(p.First_Name, ' ', COALESCE(p.Last_Name, '')) AS Person_Name,
                       df.Fruit_Name
                FROM Devil_Fruit_Possession dfp
                JOIN Person p ON dfp.Person_ID = p.Person_ID
                JOIN Devil_Fruit df ON dfp.Fruit_ID = df.Fruit_ID
                WHERE dfp.Fruit_ID = %s
            """
            current_owner = db.execute_query(current_owner_sql, (fruit_id,))
            
            # Get new owner info
            new_owner_sql = """
                SELECT CONCAT(First_Name, ' ', COALESCE(Last_Name, '')) AS Person_Name
                FROM Person WHERE Person_ID = %s
            """
            new_owner = db.execute_query(new_owner_sql, (new_person_id,))
            
            if not new_owner:
                raise ValueError("New person not found")
            
            # Update possession record - transfer fruit to new person
            update_sql = """
                UPDATE Devil_Fruit_Possession 
                SET Person_ID = %s 
                WHERE Fruit_ID = %s
            """
            db.execute_update(update_sql, (new_person_id, fruit_id))
            
            if current_owner:
                message = f"✅ Successfully transferred {current_owner[0]['Fruit_Name']} from {current_owner[0]['Person_Name']} to {new_owner[0]['Person_Name']}"
            else:
                message = f"✅ Successfully assigned Devil Fruit to {new_owner[0]['Person_Name']}"
            message_type = 'success'
            
        except Exception as e:
            message = f"❌ Error: {str(e)}"
            message_type = 'danger'
    
    # Get only devil fruits that are already in the possession table (have been possessed at least once)
    fruits_sql = """
        SELECT df.Fruit_ID, 
               df.Fruit_Name, 
               df.Type, 
               df.Description,
               dfp.Person_ID AS Current_Owner_ID,
               CONCAT(p.First_Name, ' ', COALESCE(p.Last_Name, '')) AS Current_Owner_Name
        FROM Devil_Fruit df
        INNER JOIN Devil_Fruit_Possession dfp ON df.Fruit_ID = dfp.Fruit_ID
        LEFT JOIN Person p ON dfp.Person_ID = p.Person_ID
        ORDER BY df.Fruit_Name
    """
    fruits = db.execute_query(fruits_sql)
    
    # Get people without fruits (potential new owners)
    people_sql = """
        SELECT p.Person_ID, 
               CONCAT(p.First_Name, ' ', COALESCE(p.Last_Name, '')) AS Person_Name,
               p.Status
        FROM Person p
        WHERE p.Person_ID NOT IN (SELECT Person_ID FROM Devil_Fruit_Possession WHERE Person_ID IS NOT NULL)
        ORDER BY p.First_Name, p.Last_Name
    """
    people = db.execute_query(people_sql)
    
    return render_template('operations/consume_fruit.html',
                         fruits=fruits,
                         people=people,
                         message=message,
                         message_type=message_type)


@app.route('/command/update-bounty', methods=['GET', 'POST'])
def update_bounty():
    """Update bounty amount and create historical record."""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    message = None
    message_type = 'success'
    
    if request.method == 'POST':
        try:
            # Get form data
            person_id = request.form.get('person_id', '').strip()
            new_amount = request.form.get('new_amount', '').strip()
            date_issued = request.form.get('date_issued', '').strip()
            last_seen_location = request.form.get('last_seen_location', '').strip()
            
            # Validation
            if not person_id or not new_amount:
                raise ValueError("Person and new amount are required")
            
            person_id = int(person_id)
            new_amount = int(new_amount)
            
            if new_amount < 0:
                raise ValueError("Bounty amount must be positive")
            
            # Get current max version for this person
            version_sql = """
                SELECT COALESCE(MAX(Record_Version), 0) as max_version 
                FROM Bounty_Record 
                WHERE Person_ID = %s
            """
            version_result = db.execute_query(version_sql, (person_id,))
            next_version = version_result[0]['max_version'] + 1
            
            # Insert new record into Bounty_Record with incremented version
            record_sql = """
                INSERT INTO Bounty_Record (Person_ID, Record_Version, Amount, Issue_Date, Last_Seen_Location)
                VALUES (%s, %s, %s, %s, %s)
            """
            db.execute_update(record_sql, (person_id, next_version, new_amount, 
                                         date_issued if date_issued else None,
                                         last_seen_location if last_seen_location else None))
            
            message = f"✅ Successfully updated bounty to ฿{new_amount:,} (Version {next_version})"
            message_type = 'success'
            
        except Exception as e:
            message = f"❌ Error: {str(e)}"
            message_type = 'danger'
    
    # Get all active bounties
    bounties_sql = """
        SELECT 
            br.Person_ID,
            br.Record_Version,
            CONCAT(p.First_Name, ' ', COALESCE(p.Last_Name, '')) AS Person_Name,
            br.Amount,
            br.Issue_Date AS Date_Issued,
            p.Status,
            br.Record_Version as version_count
        FROM Bounty_Record br
        INNER JOIN Person p ON br.Person_ID = p.Person_ID
        INNER JOIN Pirate pi ON p.Person_ID = pi.Person_ID
        WHERE br.Record_Version = (
            SELECT MAX(Record_Version)
            FROM Bounty_Record
            WHERE Person_ID = br.Person_ID
        )
        ORDER BY br.Amount DESC
    """
    bounties = db.execute_query(bounties_sql)
    
    return render_template('operations/update_bounty.html',
                         bounties=bounties,
                         message=message,
                         message_type=message_type)


@app.route('/command/revoke-bounty', methods=['GET', 'POST'])
def revoke_bounty():
    """Remove a bounty from the database."""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    message = None
    message_type = 'success'
    
    if request.method == 'POST':
        try:
            # Get form data
            person_id = request.form.get('person_id', '').strip()
            
            # Validation
            if not person_id:
                raise ValueError("Person ID is required")
            
            person_id = int(person_id)
            
            # Get bounty info before deletion
            info_sql = """
                SELECT CONCAT(p.First_Name, ' ', COALESCE(p.Last_Name, '')) AS Person_Name,
                       br.Amount
                FROM Bounty_Record br
                JOIN Person p ON br.Person_ID = p.Person_ID
                WHERE br.Person_ID = %s
                  AND br.Record_Version = (
                      SELECT MAX(Record_Version)
                      FROM Bounty_Record
                      WHERE Person_ID = br.Person_ID
                  )
            """
            info = db.execute_query(info_sql, (person_id,))
            
            if not info:
                raise ValueError("Bounty not found")
            
            person_name = info[0]['Person_Name']
            amount = info[0]['Amount']
            
            # Delete all bounty records for this person
            delete_bounty_sql = "DELETE FROM Bounty_Record WHERE Person_ID = %s"
            db.execute_update(delete_bounty_sql, (person_id,))
            
            message = f"✅ Successfully revoked bounty for {person_name} (฿{amount:,})"
            message_type = 'success'
            
        except Exception as e:
            message = f"❌ Error: {str(e)}"
            message_type = 'danger'
    
    # Get all bounties (latest version for each pirate)
    bounties_sql = """
        SELECT br.Person_ID,
               CONCAT(p.First_Name, ' ', COALESCE(p.Last_Name, '')) AS Person_Name,
               br.Amount,
               br.Issue_Date AS Date_Issued,
               p.Status
        FROM Bounty_Record br
        JOIN Person p ON br.Person_ID = p.Person_ID
        JOIN Pirate pi ON p.Person_ID = pi.Person_ID
        WHERE br.Record_Version = (
            SELECT MAX(Record_Version)
            FROM Bounty_Record
            WHERE Person_ID = br.Person_ID
        )
        ORDER BY br.Amount DESC
    """
    bounties = db.execute_query(bounties_sql)
    
    return render_template('operations/revoke_bounty.html',
                         bounties=bounties,
                         message=message,
                         message_type=message_type)


@app.route('/command/remove-log-entry', methods=['GET', 'POST'])
def remove_log_entry():
    """Remove/Delete ship log entry from the database."""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    message = None
    message_type = 'success'
    
    if request.method == 'POST':
        try:
            # Get form data
            ship_id = request.form.get('ship_id', '').strip()
            log_timestamp = request.form.get('log_timestamp', '').strip()
            
            # Validation
            if not ship_id or not log_timestamp:
                raise ValueError("Ship ID and Log Timestamp are required")
            
            ship_id = int(ship_id)
            
            # Get info before deletion
            info_sql = """
                SELECT s.Ship_Name, 
                       le.Log_Timestamp,
                       le.Entry_Text,
                       c.Crew_Name
                FROM Log_Entry le
                JOIN Ship s ON le.Ship_ID = s.Ship_ID
                LEFT JOIN Crew c ON s.Owning_Crew_ID = c.Crew_ID
                WHERE le.Ship_ID = %s AND le.Log_Timestamp = %s
            """
            info = db.execute_query(info_sql, (ship_id, log_timestamp))
            
            if not info:
                raise ValueError("Log entry not found")
            
            ship_name = info[0]['Ship_Name']
            timestamp = info[0]['Log_Timestamp']
            entry_preview = info[0]['Entry_Text'][:50] + "..." if len(info[0]['Entry_Text']) > 50 else info[0]['Entry_Text']
            
            # Delete log entry record (composite primary key)
            delete_sql = "DELETE FROM Log_Entry WHERE Ship_ID = %s AND Log_Timestamp = %s"
            db.execute_update(delete_sql, (ship_id, log_timestamp))
            
            message = f"✅ Successfully removed log entry from {ship_name} at {timestamp}"
            message_type = 'success'
            
        except Exception as e:
            message = f"❌ Error: {str(e)}"
            message_type = 'danger'
    
    # Get all log entries with ship information
    logs_sql = """
        SELECT le.Ship_ID,
               le.Log_Timestamp,
               s.Ship_Name,
               c.Crew_Name,
               le.Entry_Text,
               le.Latitude,
               le.Longitude
        FROM Log_Entry le
        JOIN Ship s ON le.Ship_ID = s.Ship_ID
        LEFT JOIN Crew c ON s.Owning_Crew_ID = c.Crew_ID
        ORDER BY le.Log_Timestamp DESC, s.Ship_Name
    """
    logs = db.execute_query(logs_sql)
    
    return render_template('operations/remove_log_entry.html',
                         logs=logs,
                         message=message,
                         message_type=message_type)


@app.route('/command/remove-fruit-possession', methods=['GET', 'POST'])
def remove_fruit_possession():
    """Remove/Delete Devil Fruit possession record."""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    message = None
    message_type = 'success'
    
    if request.method == 'POST':
        try:
            # Get form data
            fruit_id = request.form.get('fruit_id', '').strip()
            
            # Validation
            if not fruit_id:
                raise ValueError("Devil Fruit is required")
            
            fruit_id = int(fruit_id)
            
            # Get info before deletion
            info_sql = """
                SELECT df.Fruit_Name, 
                       df.Type,
                       p.Person_ID,
                       CONCAT(p.First_Name, ' ', COALESCE(p.Last_Name, '')) AS Person_Name
                FROM Devil_Fruit_Possession dfp
                JOIN Devil_Fruit df ON dfp.Fruit_ID = df.Fruit_ID
                LEFT JOIN Person p ON dfp.Person_ID = p.Person_ID
                WHERE dfp.Fruit_ID = %s
            """
            info = db.execute_query(info_sql, (fruit_id,))
            
            if not info:
                raise ValueError("Devil Fruit possession record not found")
            
            fruit_name = info[0]['Fruit_Name']
            person_name = info[0]['Person_Name'] if info[0]['Person_Name'] else "Unknown"
            
            # Delete possession record
            delete_sql = "DELETE FROM Devil_Fruit_Possession WHERE Fruit_ID = %s"
            db.execute_update(delete_sql, (fruit_id,))
            
            message = f"✅ Successfully removed {fruit_name} possession from {person_name}"
            message_type = 'success'
            
        except Exception as e:
            message = f"❌ Error: {str(e)}"
            message_type = 'danger'
    
    # Get all devil fruit possessions
    possessions_sql = """
        SELECT dfp.Fruit_ID,
               df.Fruit_Name,
               df.Type,
               df.Description,
               dfp.Person_ID,
               CONCAT(p.First_Name, ' ', COALESCE(p.Last_Name, '')) AS Person_Name,
               p.Status
        FROM Devil_Fruit_Possession dfp
        JOIN Devil_Fruit df ON dfp.Fruit_ID = df.Fruit_ID
        LEFT JOIN Person p ON dfp.Person_ID = p.Person_ID
        ORDER BY df.Fruit_Name
    """
    possessions = db.execute_query(possessions_sql)
    
    return render_template('operations/remove_fruit_possession.html',
                         possessions=possessions,
                         message=message,
                         message_type=message_type)


@app.route('/update/change_status', methods=['GET', 'POST'])
def update_status():
    """Update a person's status."""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    message = None
    message_type = 'success'
    
    if request.method == 'POST':
        person_id = request.form.get('person_id')
        new_status = request.form.get('new_status')
        
        # Get current status first
        get_status_sql = """
            SELECT First_Name, Last_Name, Status 
            FROM Person 
            WHERE Person_ID = %s
        """
        person_info = db.execute_query(get_status_sql, (person_id,))
        
        if person_info:
            old_status = person_info[0]['Status']
            person_name = f"{person_info[0]['First_Name']} {person_info[0]['Last_Name']}" if person_info[0]['Last_Name'] else person_info[0]['First_Name']
            
            # Update status
            sql = """
                UPDATE Person
                SET Status = %s
                WHERE Person_ID = %s
            """
            
            affected = db.execute_update(sql, (new_status, person_id))
            
            if affected > 0:
                message = f"✅ Status updated for {person_name} (ID: {person_id}): {old_status} → {new_status}"
                message_type = 'success'
            else:
                message = f"❌ Failed to update status"
                message_type = 'danger'
        else:
            message = f"❌ Person ID {person_id} not found"
            message_type = 'warning'
    
    # Get list of people for dropdown
    people_sql = """
        SELECT Person_ID, First_Name, Last_Name, Status
        FROM Person
        ORDER BY Last_Name, First_Name
    """
    people = db.execute_query(people_sql)
    
    return render_template('updates/change_status.html', people=people, message=message, message_type=message_type)


# ============================================================================
# CP0 ADMIN CONSOLE ROUTES
# ============================================================================

@app.route('/admin_console')
def admin_console():
    """Admin console for CP0 administrators (DDL operations)."""
    if 'username' not in session or session.get('role') != 'admin':
        flash('ACCESS DENIED. CP0 clearance required.', 'danger')
        return redirect(url_for('login'))
    
    return render_template('admin_console.html')


@app.route('/admin/buster_call', methods=['POST'])
def buster_call():
    """ADMIN: Drop all tables (Buster Call Protocol)."""
    if 'username' not in session or session.get('role') != 'admin':
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    confirmation = request.form.get('confirmation', '')
    
    if confirmation != 'EXECUTE_BUSTER_CALL':
        flash('OPERATION ABORTED. Incorrect confirmation code.', 'warning')
        return redirect(url_for('admin_console'))
    
    # Get all tables
    tables_sql = "SHOW TABLES"
    tables = db.execute_query(tables_sql)
    
    if tables:
        # Disable foreign key checks
        db.execute_ddl("SET FOREIGN_KEY_CHECKS = 0")
        
        dropped_count = 0
        for table_dict in tables:
            table_name = list(table_dict.values())[0]
            if db.execute_ddl(f"DROP TABLE IF EXISTS {table_name}"):
                dropped_count += 1
        
        # Re-enable foreign key checks
        db.execute_ddl("SET FOREIGN_KEY_CHECKS = 1")
        
        flash(f'BUSTER CALL EXECUTED. {dropped_count} tables eliminated.', 'success')
    else:
        flash('No tables found in database.', 'info')
    
    return redirect(url_for('admin_console'))


@app.route('/admin/truncate_table', methods=['POST'])
def truncate_table():
    """ADMIN: Truncate a specific table."""
    if 'username' not in session or session.get('role') != 'admin':
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    table_name = request.form.get('table_name', '').strip()
    
    if not table_name:
        flash('ERROR: No table name provided.', 'danger')
        return redirect(url_for('admin_console'))
    
    # Disable foreign key checks temporarily
    db.execute_ddl("SET FOREIGN_KEY_CHECKS = 0")
    success = db.execute_ddl(f"TRUNCATE TABLE {table_name}")
    db.execute_ddl("SET FOREIGN_KEY_CHECKS = 1")
    
    if success:
        flash(f'TABLE PURGED: {table_name} has been truncated.', 'success')
    else:
        flash(f'OPERATION FAILED: Unable to truncate {table_name}.', 'danger')
    
    return redirect(url_for('admin_console'))


@app.route('/admin/alter_schema', methods=['POST'])
def alter_schema():
    """ADMIN: Execute custom DDL command."""
    if 'username' not in session or session.get('role') != 'admin':
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    ddl_command = request.form.get('ddl_command', '').strip()
    
    if not ddl_command:
        flash('ERROR: No DDL command provided.', 'danger')
        return redirect(url_for('admin_console'))
    
    # Security check: Only allow ALTER, CREATE INDEX, DROP INDEX
    allowed_commands = ['ALTER', 'CREATE INDEX', 'DROP INDEX']
    if not any(ddl_command.upper().startswith(cmd) for cmd in allowed_commands):
        flash('SECURITY VIOLATION: Only ALTER, CREATE INDEX, and DROP INDEX commands allowed.', 'danger')
        return redirect(url_for('admin_console'))
    
    success = db.execute_ddl(ddl_command)
    
    if success:
        flash(f'SCHEMA ALTERED SUCCESSFULLY: {ddl_command[:100]}...', 'success')
    else:
        flash('OPERATION FAILED: DDL execution error.', 'danger')
    
    return redirect(url_for('admin_console'))


@app.route('/admin/view_tables')
def view_tables():
    """ADMIN: View all tables in the database."""
    if 'username' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))
    
    tables_sql = "SHOW TABLES"
    tables = db.execute_query(tables_sql)
    
    table_info = []
    if tables:
        for table_dict in tables:
            table_name = list(table_dict.values())[0]
            
            # Get row count
            count_sql = f"SELECT COUNT(*) AS row_count FROM {table_name}"
            count_result = db.execute_query(count_sql)
            row_count = count_result[0]['row_count'] if count_result else 0
            
            table_info.append({
                'name': table_name,
                'row_count': row_count
            })
    
    return render_template('admin/view_tables.html', tables=table_info)


# Error handlers

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return render_template('error.html', 
                         error_code=404, 
                         error_message='INTELLIGENCE NOT FOUND',
                         error_detail='The requested resource does not exist in the database.'), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return render_template('error.html', 
                         error_code=500, 
                         error_message='SYSTEM MALFUNCTION',
                         error_detail='An internal error occurred. Contact Cipher Pol support.'), 500


# Application startup

if __name__ == '__main__':
    if init_database():
        print("\n[SYSTEM] Starting Flask application...")
        print("[SYSTEM] Access the terminal at: http://127.0.0.1:5000")
        print("[SYSTEM] Press CTRL+C to terminate.\n")
        
        try:
            app.run(debug=True, host='0.0.0.0', port=5000)
        finally:
            if db:
                db.disconnect()
    else:
        print("[CRITICAL] Database initialization failed. Exiting.")
        sys.exit(1)

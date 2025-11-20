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
# MODULE HUBS (Phase 4 - Modular Architecture)
# ============================================================================

@app.route('/hub/intelligence')
def intelligence_hub():
    """Intelligence Hub - Data Retrieval & Search Operations."""
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('hubs/intelligence.html')


@app.route('/hub/tactical')
def tactical_analysis():
    """Tactical Analysis Hub - Aggregate Queries & Reports."""
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('hubs/tactical.html')


@app.route('/hub/command')
def command_ops():
    """Command Operations Hub - Database Modifications."""
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('hubs/command.html')


# ============================================================================
# INTELLIGENCE HUB - SELECTION QUERIES
# ============================================================================

@app.route('/intel/query/high-bounty-pirates')
def query_high_bounty_pirates():
    """Selection Query 1: Pirates with bounty > 500,000,000."""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    sql = """
        SELECT 
            p.Person_ID,
            CONCAT(p.First_Name, ' ', COALESCE(p.Last_Name, '')) AS Full_Name,
            p.Status,
            pi.Infamy_Level,
            br.Amount AS Bounty,
            br.Issue_Date
        FROM Person p
        INNER JOIN Pirate pi ON p.Person_ID = pi.Person_ID
        LEFT JOIN Bounty_Record br ON p.Person_ID = br.Person_ID
            AND br.Record_Version = (
                SELECT MAX(Record_Version)
                FROM Bounty_Record
                WHERE Person_ID = p.Person_ID
            )
        WHERE br.Amount > 500000000
        ORDER BY br.Amount DESC
    """
    
    results = db.execute_query(sql)
    results = format_query_results(results)
    
    return render_template('universal_table.html',
                         query_title='High Bounty Pirates',
                         description='Pirates with bounty exceeding ฿500,000,000',
                         icon='💰',
                         results=results,
                         back_url=url_for('intelligence_hub'),
                         back_name='Intelligence Hub',
                         now=datetime.now(),
                         show_form=False)


@app.route('/intel/query/logia-fruits')
def query_logia_fruits():
    """Selection Query 2: All Logia-type Devil Fruits."""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    sql = """
        SELECT 
            df.Fruit_ID,
            df.Fruit_Name,
            df.Type,
            df.Description,
            df.is_Awakened,
            CONCAT(p.First_Name, ' ', COALESCE(p.Last_Name, '')) AS `Current_User`
        FROM Devil_Fruit df
        LEFT JOIN Devil_Fruit_Possession dfp ON df.Fruit_ID = dfp.Fruit_ID
        LEFT JOIN Person p ON dfp.Person_ID = p.Person_ID
        WHERE df.Type = 'Logia'
        ORDER BY df.Fruit_Name
    """
    
    results = db.execute_query(sql)
    results = format_query_results(results)
    
    return render_template('universal_table.html',
                         query_title='Logia Devil Fruits',
                         description='All Logia-type fruits in the database',
                         icon='🔥',
                         results=results,
                         back_url=url_for('intelligence_hub'),
                         back_name='Intelligence Hub',
                         now=datetime.now(),
                         show_form=False)


@app.route('/intel/query/admirals')
def query_admirals():
    """Selection Query 3: All Marine Admirals."""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    sql = """
        SELECT 
            p.Person_ID,
            CONCAT(p.First_Name, ' ', COALESCE(p.Last_Name, '')) AS Full_Name,
            mo.`Rank`,
            mo.Service_Number,
            p.Status,
            p.Date_of_Birth
        FROM Person p
        INNER JOIN Marine_Officer mo ON p.Person_ID = mo.Person_ID
        WHERE mo.`Rank` LIKE '%%Admiral%%'
        ORDER BY 
            CASE mo.`Rank`
                WHEN 'Fleet Admiral' THEN 1
                WHEN 'Admiral' THEN 2
                WHEN 'Vice Admiral' THEN 3
                ELSE 4
            END,
            p.First_Name
    """
    
    results = db.execute_query(sql)
    results = format_query_results(results)
    
    return render_template('universal_table.html',
                         query_title='Admiral Roster',
                         description='All Marine Officers with Admiral rank',
                         icon='⭐',
                         results=results,
                         back_url=url_for('intelligence_hub'),
                         back_name='Intelligence Hub',
                         now=datetime.now(),
                         show_form=False)


@app.route('/intel/query/grandline-islands')
def query_grandline_islands():
    """Selection Query 4: Islands in Grand Line."""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    sql = """
        SELECT 
            i.Island_ID,
            i.Island_Name,
            i.Climate,
            i.Population,
            sr.Region_Name,
            sr.Threat_Level
        FROM Island i
        INNER JOIN Sea_Region sr ON i.Region_ID = sr.Region_ID
        WHERE sr.Region_Name LIKE '%%Grand Line%%'
        ORDER BY i.Island_Name
    """
    
    results = db.execute_query(sql)
    results = format_query_results(results)
    
    return render_template('universal_table.html',
                         query_title='Grand Line Islands',
                         description='Islands located in Grand Line regions',
                         icon='🏝️',
                         results=results,
                         back_url=url_for('intelligence_hub'),
                         back_name='Intelligence Hub',
                         now=datetime.now(),
                         show_form=False)


@app.route('/intel/query/old-crews', methods=['GET', 'POST'])
def query_old_crews():
    """Selection Query 5: Crews formed before specified year."""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    results = None
    if request.method == 'POST':
        year = request.form.get('year', '1520')
        
        sql = """
            SELECT 
                c.Crew_ID,
                c.Crew_Name,
                c.Date_Formed,
                c.Status,
                YEAR(CURDATE()) - YEAR(c.Date_Formed) AS Years_Active,
                COUNT(m.Person_ID) AS Member_Count
            FROM Crew c
            LEFT JOIN Membership m ON c.Crew_ID = m.Crew_ID
            WHERE YEAR(c.Date_Formed) < %s
            GROUP BY c.Crew_ID, c.Crew_Name, c.Date_Formed, c.Status
            ORDER BY c.Date_Formed
        """
        
        results = db.execute_query(sql, (year,))
        results = format_query_results(results)
    
    form_fields = [
        {'name': 'year', 'label': 'Formation Year (Before)', 'type': 'number', 'placeholder': '1520', 'required': True, 'col_width': 12}
    ]
    
    return render_template('universal_table.html',
                         query_title='Veteran Crews',
                         description='Crews formed before the specified year',
                         icon='⏰',
                         results=results,
                         back_url=url_for('intelligence_hub'),
                         back_name='Intelligence Hub',
                         now=datetime.now(),
                         show_form=True,
                         form_action=url_for('query_old_crews'),
                         form_fields=form_fields,
                         form_instruction='Enter a year to find all crews formed before that date')


@app.route('/intel/query/captured')
def query_captured():
    """Selection Query 6: All captured individuals."""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    sql = """
        SELECT 
            p.Person_ID,
            CONCAT(p.First_Name, ' ', COALESCE(p.Last_Name, '')) AS Full_Name,
            p.Status,
            p.Date_of_Birth,
            CASE 
                WHEN pi.Person_ID IS NOT NULL THEN 'Pirate'
                WHEN mo.Person_ID IS NOT NULL THEN 'Marine'
                WHEN c.Person_ID IS NOT NULL THEN 'Civilian'
                ELSE 'Unknown'
            END AS Type,
            br.Amount AS Last_Bounty
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
        WHERE p.Status = 'Captured'
        ORDER BY p.First_Name
    """
    
    results = db.execute_query(sql)
    results = format_query_results(results)
    
    return render_template('universal_table.html',
                         query_title='Captured Targets',
                         description='All individuals with Captured status',
                         icon='⛓️',
                         results=results,
                         back_url=url_for('intelligence_hub'),
                         back_name='Intelligence Hub',
                         now=datetime.now(),
                         show_form=False)


@app.route('/intel/query/awakened-users')
def query_awakened_users():
    """Selection Query 7: Pirates with awakened Devil Fruits."""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    sql = """
        SELECT 
            p.Person_ID,
            CONCAT(p.First_Name, ' ', COALESCE(p.Last_Name, '')) AS Full_Name,
            p.Status,
            pi.Infamy_Level,
            df.Fruit_Name,
            df.Type AS Fruit_Type,
            df.is_Awakened,
            br.Amount AS Bounty
        FROM Person p
        INNER JOIN Pirate pi ON p.Person_ID = pi.Person_ID
        INNER JOIN Devil_Fruit_Possession dfp ON p.Person_ID = dfp.Person_ID
        INNER JOIN Devil_Fruit df ON dfp.Fruit_ID = df.Fruit_ID
        LEFT JOIN Bounty_Record br ON p.Person_ID = br.Person_ID
            AND br.Record_Version = (
                SELECT MAX(Record_Version)
                FROM Bounty_Record
                WHERE Person_ID = p.Person_ID
            )
        WHERE df.is_Awakened = TRUE
        ORDER BY br.Amount DESC
    """
    
    results = db.execute_query(sql)
    results = format_query_results(results)
    
    return render_template('universal_table.html',
                         query_title='Awakened Fruit Users',
                         description='Pirates who have awakened their Devil Fruits',
                         icon='⚡',
                         results=results,
                         back_url=url_for('intelligence_hub'),
                         back_name='Intelligence Hub',
                         now=datetime.now(),
                         show_form=False)


# ============================================================================
# INTELLIGENCE HUB - PROJECTION QUERIES
# ============================================================================

@app.route('/intel/query/marine-ranks')
def query_marine_ranks():
    """Projection Query 1: Marine Names and Ranks."""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    sql = """
        SELECT 
            p.Person_ID,
            CONCAT(p.First_Name, ' ', COALESCE(p.Last_Name, '')) AS Full_Name,
            mo.`Rank`,
            mo.Service_Number
        FROM Person p
        INNER JOIN Marine_Officer mo ON p.Person_ID = mo.Person_ID
        ORDER BY 
            CASE mo.`Rank`
                WHEN 'Fleet Admiral' THEN 1
                WHEN 'Admiral' THEN 2
                WHEN 'Vice Admiral' THEN 3
                ELSE 4
            END,
            p.First_Name
    """
    
    results = db.execute_query(sql)
    results = format_query_results(results)
    
    return render_template('universal_table.html',
                         query_title='Marine Ranks',
                         description='Names and ranks of all Marine Officers',
                         icon='🎖️',
                         results=results,
                         back_url=url_for('intelligence_hub'),
                         back_name='Intelligence Hub',
                         now=datetime.now(),
                         show_form=False)


@app.route('/intel/query/pirate-bounties')
def query_pirate_bounties():
    """Projection Query 2: Pirate Names and Bounties."""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    sql = """
        SELECT 
            p.Person_ID,
            CONCAT(p.First_Name, ' ', COALESCE(p.Last_Name, '')) AS Full_Name,
            br.Amount AS Bounty,
            br.Issue_Date
        FROM Person p
        INNER JOIN Pirate pi ON p.Person_ID = pi.Person_ID
        LEFT JOIN Bounty_Record br ON p.Person_ID = br.Person_ID
            AND br.Record_Version = (
                SELECT MAX(Record_Version)
                FROM Bounty_Record
                WHERE Person_ID = p.Person_ID
            )
        ORDER BY br.Amount DESC
    """
    
    results = db.execute_query(sql)
    results = format_query_results(results)
    
    return render_template('universal_table.html',
                         query_title='Pirate Bounties',
                         description='Names and current bounty amounts',
                         icon='💵',
                         results=results,
                         back_url=url_for('intelligence_hub'),
                         back_name='Intelligence Hub',
                         now=datetime.now(),
                         show_form=False)


@app.route('/intel/query/fruit-types')
def query_fruit_types():
    """Projection Query 3: Devil Fruit Names and Types."""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    sql = """
        SELECT 
            df.Fruit_ID,
            df.Fruit_Name,
            df.Type,
            df.is_Awakened
        FROM Devil_Fruit df
        ORDER BY df.Type, df.Fruit_Name
    """
    
    results = db.execute_query(sql)
    results = format_query_results(results)
    
    return render_template('universal_table.html',
                         query_title='Devil Fruit Catalog',
                         description='Names and types of all Devil Fruits',
                         icon='🍇',
                         results=results,
                         back_url=url_for('intelligence_hub'),
                         back_name='Intelligence Hub',
                         now=datetime.now(),
                         show_form=False)


@app.route('/intel/query/crew-dates')
def query_crew_dates():
    """Projection Query 4: Crew Names and Formation Dates."""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    sql = """
        SELECT 
            c.Crew_ID,
            c.Crew_Name,
            c.Date_Formed,
            c.Status,
            YEAR(CURDATE()) - YEAR(c.Date_Formed) AS Years_Active
        FROM Crew c
        ORDER BY c.Date_Formed
    """
    
    results = db.execute_query(sql)
    results = format_query_results(results)
    
    return render_template('universal_table.html',
                         query_title='Crew Timeline',
                         description='Crew names and formation dates',
                         icon='📅',
                         results=results,
                         back_url=url_for('intelligence_hub'),
                         back_name='Intelligence Hub',
                         now=datetime.now(),
                         show_form=False)


@app.route('/intel/query/island-climates')
def query_island_climates():
    """Projection Query 5: Island Names and Climates."""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    sql = """
        SELECT 
            i.Island_ID,
            i.Island_Name,
            i.Climate,
            sr.Region_Name
        FROM Island i
        INNER JOIN Sea_Region sr ON i.Region_ID = sr.Region_ID
        ORDER BY sr.Region_Name, i.Island_Name
    """
    
    results = db.execute_query(sql)
    results = format_query_results(results)
    
    return render_template('universal_table.html',
                         query_title='Island Climates',
                         description='Island names and climate types',
                         icon='🌤️',
                         results=results,
                         back_url=url_for('intelligence_hub'),
                         back_name='Intelligence Hub',
                         now=datetime.now(),
                         show_form=False)


@app.route('/intel/query/ship-registry')
def query_ship_registry():
    """Projection Query 6: Ship Names and Owning Crews."""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    sql = """
        SELECT 
            s.Ship_ID,
            s.Ship_Name,
            s.Class,
            c.Crew_Name AS Owner,
            s.Commission_Date
        FROM Ship s
        LEFT JOIN Crew c ON s.Owning_Crew_ID = c.Crew_ID
        ORDER BY s.Ship_Name
    """
    
    results = db.execute_query(sql)
    results = format_query_results(results)
    
    return render_template('universal_table.html',
                         query_title='Ship Registry',
                         description='Ship names and their owning crews',
                         icon='🚢',
                         results=results,
                         back_url=url_for('intelligence_hub'),
                         back_name='Intelligence Hub',
                         now=datetime.now(),
                         show_form=False)


@app.route('/intel/query/faction-leaders')
def query_faction_leaders():
    """Projection Query 7: Faction Names and Leaders."""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    sql = """
        SELECT 
            f.Faction_ID,
            f.Faction_Name,
            f.Ideology,
            CONCAT(p.First_Name, ' ', COALESCE(p.Last_Name, '')) AS Leader_Name
        FROM Faction f
        LEFT JOIN Person p ON f.Leader_ID = p.Person_ID
        ORDER BY f.Faction_Name
    """
    
    results = db.execute_query(sql)
    results = format_query_results(results)
    
    return render_template('universal_table.html',
                         query_title='Faction Leadership',
                         description='Faction names and their leaders',
                         icon='👑',
                         results=results,
                         back_url=url_for('intelligence_hub'),
                         back_name='Intelligence Hub',
                         now=datetime.now(),
                         show_form=False)


# ============================================================================
# INTELLIGENCE HUB - SEARCH QUERIES
# ============================================================================

@app.route('/intel/search/person-name', methods=['GET', 'POST'])
def search_person_name():
    """Search Query 1: Search person by name pattern."""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    results = None
    if request.method == 'POST':
        name_pattern = request.form.get('name_pattern', '').strip()
        
        sql = """
            SELECT 
                p.Person_ID,
                CONCAT(p.First_Name, ' ', COALESCE(p.Last_Name, '')) AS Full_Name,
                p.Date_of_Birth,
                p.Status,
                CASE 
                    WHEN pi.Person_ID IS NOT NULL THEN 'Pirate'
                    WHEN mo.Person_ID IS NOT NULL THEN 'Marine Officer'
                    WHEN c.Person_ID IS NOT NULL THEN 'Civilian'
                    ELSE 'Unknown'
                END AS Type
            FROM Person p
            LEFT JOIN Pirate pi ON p.Person_ID = pi.Person_ID
            LEFT JOIN Marine_Officer mo ON p.Person_ID = mo.Person_ID
            LEFT JOIN Civilian c ON p.Person_ID = c.Person_ID
            WHERE CONCAT(p.First_Name, ' ', COALESCE(p.Last_Name, '')) LIKE %s
            ORDER BY p.First_Name
        """
        
        results = db.execute_query(sql, (f'%{name_pattern}%',))
        results = format_query_results(results)
    
    form_fields = [
        {'name': 'name_pattern', 'label': 'Name Pattern (e.g., "D.")', 'type': 'text', 'placeholder': 'Enter name or pattern', 'required': True, 'col_width': 12}
    ]
    
    return render_template('universal_table.html',
                         query_title='Search Person by Name',
                         description='Find persons matching name pattern',
                         icon='👤',
                         results=results,
                         back_url=url_for('intelligence_hub'),
                         back_name='Intelligence Hub',
                         now=datetime.now(),
                         show_form=True,
                         form_action=url_for('search_person_name'),
                         form_fields=form_fields)


@app.route('/intel/search/crew-name', methods=['GET', 'POST'])
def search_crew_name():
    """Search Query 2: Search crew by name pattern."""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    results = None
    if request.method == 'POST':
        crew_pattern = request.form.get('crew_pattern', '').strip()
        
        sql = """
            SELECT 
                c.Crew_ID,
                c.Crew_Name,
                c.Date_Formed,
                c.Status,
                COUNT(m.Person_ID) AS Member_Count
            FROM Crew c
            LEFT JOIN Membership m ON c.Crew_ID = m.Crew_ID
            WHERE c.Crew_Name LIKE %s
            GROUP BY c.Crew_ID, c.Crew_Name, c.Date_Formed, c.Status
            ORDER BY c.Crew_Name
        """
        
        results = db.execute_query(sql, (f'%{crew_pattern}%',))
        results = format_query_results(results)
    
    form_fields = [
        {'name': 'crew_pattern', 'label': 'Crew Name Pattern (e.g., "Heart")', 'type': 'text', 'placeholder': 'Enter crew name', 'required': True, 'col_width': 12}
    ]
    
    return render_template('universal_table.html',
                         query_title='Search Crew by Name',
                         description='Find crews matching name pattern',
                         icon='🏴‍☠️',
                         results=results,
                         back_url=url_for('intelligence_hub'),
                         back_name='Intelligence Hub',
                         now=datetime.now(),
                         show_form=True,
                         form_action=url_for('search_crew_name'),
                         form_fields=form_fields)


@app.route('/intel/search/marine-service', methods=['GET', 'POST'])
def search_marine_service():
    """Search Query 3: Search Marine by service number."""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    results = None
    if request.method == 'POST':
        service_number = request.form.get('service_number', '').strip()
        
        sql = """
            SELECT 
                p.Person_ID,
                CONCAT(p.First_Name, ' ', COALESCE(p.Last_Name, '')) AS Full_Name,
                mo.`Rank`,
                mo.Service_Number,
                p.Status,
                p.Date_of_Birth
            FROM Person p
            INNER JOIN Marine_Officer mo ON p.Person_ID = mo.Person_ID
            WHERE mo.Service_Number LIKE %s
            ORDER BY mo.`Rank`, p.First_Name
        """
        
        results = db.execute_query(sql, (f'%{service_number}%',))
        results = format_query_results(results)
    
    form_fields = [
        {'name': 'service_number', 'label': 'Service Number', 'type': 'text', 'placeholder': 'MA-001', 'required': True, 'col_width': 12}
    ]
    
    return render_template('universal_table.html',
                         query_title='Marine Service Lookup',
                         description='Find Marine Officer by service number',
                         icon='🔢',
                         results=results,
                         back_url=url_for('intelligence_hub'),
                         back_name='Intelligence Hub',
                         now=datetime.now(),
                         show_form=True,
                         form_action=url_for('search_marine_service'),
                         form_fields=form_fields)


@app.route('/intel/search/by-ability', methods=['GET', 'POST'])
def search_by_ability():
    """Search Query 4: Search persons by ability."""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    results = None
    if request.method == 'POST':
        ability = request.form.get('ability', '').strip()
        
        sql = """
            SELECT 
                p.Person_ID,
                CONCAT(p.First_Name, ' ', COALESCE(p.Last_Name, '')) AS Full_Name,
                pa.Ability,
                p.Status,
                CASE 
                    WHEN pi.Person_ID IS NOT NULL THEN 'Pirate'
                    WHEN mo.Person_ID IS NOT NULL THEN 'Marine Officer'
                    ELSE 'Other'
                END AS Type
            FROM Person p
            INNER JOIN Person_Abilities pa ON p.Person_ID = pa.Person_ID
            LEFT JOIN Pirate pi ON p.Person_ID = pi.Person_ID
            LEFT JOIN Marine_Officer mo ON p.Person_ID = mo.Person_ID
            WHERE pa.Ability LIKE %s
            ORDER BY p.First_Name
        """
        
        results = db.execute_query(sql, (f'%{ability}%',))
        results = format_query_results(results)
    
    form_fields = [
        {'name': 'ability', 'label': 'Ability Name (e.g., "Haki")', 'type': 'text', 'placeholder': 'Enter ability', 'required': True, 'col_width': 12}
    ]
    
    return render_template('universal_table.html',
                         query_title='Search by Ability',
                         description='Find persons with specific abilities',
                         icon='💪',
                         results=results,
                         back_url=url_for('intelligence_hub'),
                         back_name='Intelligence Hub',
                         now=datetime.now(),
                         show_form=True,
                         form_action=url_for('search_by_ability'),
                         form_fields=form_fields)


@app.route('/intel/search/faction-ideology', methods=['GET', 'POST'])
def search_faction_ideology():
    """Search Query 5: Search faction by ideology."""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    results = None
    if request.method == 'POST':
        ideology = request.form.get('ideology', '').strip()
        
        sql = """
            SELECT 
                f.Faction_ID,
                f.Faction_Name,
                f.Ideology,
                CONCAT(p.First_Name, ' ', COALESCE(p.Last_Name, '')) AS Leader_Name,
                COUNT(DISTINCT a.Crew_ID) AS Allied_Crews
            FROM Faction f
            LEFT JOIN Person p ON f.Leader_ID = p.Person_ID
            LEFT JOIN Allegiance a ON f.Faction_ID = a.Faction_ID
            WHERE f.Ideology LIKE %s
            GROUP BY f.Faction_ID, f.Faction_Name, f.Ideology, Leader_Name
            ORDER BY f.Faction_Name
        """
        
        results = db.execute_query(sql, (f'%{ideology}%',))
        results = format_query_results(results)
    
    form_fields = [
        {'name': 'ideology', 'label': 'Ideology Pattern', 'type': 'text', 'placeholder': 'e.g., "Justice"', 'required': True, 'col_width': 12}
    ]
    
    return render_template('universal_table.html',
                         query_title='Search Faction by Ideology',
                         description='Find factions matching ideology pattern',
                         icon='🎯',
                         results=results,
                         back_url=url_for('intelligence_hub'),
                         back_name='Intelligence Hub',
                         now=datetime.now(),
                         show_form=True,
                         form_action=url_for('search_faction_ideology'),
                         form_fields=form_fields)


@app.route('/intel/search/log-entries', methods=['GET', 'POST'])
def search_log_entries():
    """Search Query 6: Search ship log entries by keyword."""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    results = None
    if request.method == 'POST':
        keyword = request.form.get('keyword', '').strip()
        
        sql = """
            SELECT 
                le.Log_Timestamp,
                s.Ship_Name,
                c.Crew_Name,
                le.Entry_Text,
                le.Latitude,
                le.Longitude
            FROM Log_Entry le
            INNER JOIN Ship s ON le.Ship_ID = s.Ship_ID
            LEFT JOIN Crew c ON s.Owning_Crew_ID = c.Crew_ID
            WHERE le.Entry_Text LIKE %s
            ORDER BY le.Log_Timestamp DESC
        """
        
        results = db.execute_query(sql, (f'%{keyword}%',))
        results = format_query_results(results)
    
    form_fields = [
        {'name': 'keyword', 'label': 'Search Keyword', 'type': 'text', 'placeholder': 'Enter keyword from log', 'required': True, 'col_width': 12}
    ]
    
    return render_template('universal_table.html',
                         query_title='Search Ship Logs',
                         description='Find log entries containing keyword',
                         icon='📝',
                         results=results,
                         back_url=url_for('intelligence_hub'),
                         back_name='Intelligence Hub',
                         now=datetime.now(),
                         show_form=True,
                         form_action=url_for('search_log_entries'),
                         form_fields=form_fields)


# ============================================================================
# TACTICAL ANALYSIS HUB - AGGREGATE QUERIES
# ============================================================================

@app.route('/tactical/aggregate/crew-bounty', methods=['GET', 'POST'])
def aggregate_crew_bounty():
    """Aggregate Query 1: Total bounty for specific crew."""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    results = None
    if request.method == 'POST':
        crew_id = request.form.get('crew_id')
        
        sql = """
            SELECT 
                c.Crew_Name,
                COUNT(DISTINCT m.Person_ID) AS Total_Members,
                SUM(br.Amount) AS Total_Bounty,
                AVG(br.Amount) AS Average_Bounty,
                MAX(br.Amount) AS Highest_Bounty
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
    
    # Get crew list for dropdown
    crews_sql = "SELECT Crew_ID, Crew_Name FROM Crew ORDER BY Crew_Name"
    crews = db.execute_query(crews_sql)
    crew_options = [(c['Crew_ID'], c['Crew_Name']) for c in crews]
    
    form_fields = [
        {'name': 'crew_id', 'label': 'Select Crew', 'type': 'select', 'options': crew_options, 'required': True, 'col_width': 12}
    ]
    
    return render_template('universal_table.html',
                         query_title='Crew Total Bounty',
                         description='Aggregate bounty statistics for crew members',
                         icon='💰',
                         results=results,
                         back_url=url_for('tactical_analysis'),
                         back_name='Tactical Analysis',
                         now=datetime.now(),
                         show_form=True,
                         form_action=url_for('aggregate_crew_bounty'),
                         form_fields=form_fields)


@app.route('/tactical/aggregate/eastblue-avg')
def aggregate_eastblue_avg():
    """Aggregate Query 2: Average bounty of East Blue pirates."""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    sql = """
        SELECT 
            sr.Region_Name,
            COUNT(DISTINCT p.Person_ID) AS Total_Pirates,
            AVG(br.Amount) AS Average_Bounty,
            MIN(br.Amount) AS Minimum_Bounty,
            MAX(br.Amount) AS Maximum_Bounty
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
        WHERE sr.Region_Name LIKE '%%East Blue%%'
        GROUP BY sr.Region_ID, sr.Region_Name
    """
    
    results = db.execute_query(sql)
    results = format_query_results(results)
    
    return render_template('universal_table.html',
                         query_title='East Blue Average Bounty',
                         description='Statistical analysis of East Blue pirates',
                         icon='🌊',
                         results=results,
                         back_url=url_for('tactical_analysis'),
                         back_name='Tactical Analysis',
                         now=datetime.now(),
                         show_form=False)


@app.route('/tactical/aggregate/islands-per-region')
def aggregate_islands_per_region():
    """Aggregate Query 3: Count islands grouped by region."""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    sql = """
        SELECT 
            sr.Region_Name,
            COUNT(i.Island_ID) AS Island_Count,
            GROUP_CONCAT(DISTINCT i.Climate ORDER BY i.Climate SEPARATOR ', ') AS Climate_Types,
            COUNT(DISTINCT t.Faction_ID) AS Controlling_Factions
        FROM Sea_Region sr
        LEFT JOIN Island i ON sr.Region_ID = i.Region_ID
        LEFT JOIN Territory t ON i.Island_ID = t.Island_ID
        GROUP BY sr.Region_ID, sr.Region_Name
        ORDER BY Island_Count DESC
    """
    
    results = db.execute_query(sql)
    results = format_query_results(results)
    
    return render_template('universal_table.html',
                         query_title='Islands by Region',
                         description='Island distribution across sea regions',
                         icon='🗺️',
                         results=results,
                         back_url=url_for('tactical_analysis'),
                         back_name='Tactical Analysis',
                         now=datetime.now(),
                         show_form=False)


@app.route('/tactical/aggregate/highest-bounty')
def aggregate_highest_bounty():
    """Aggregate Query 4: Highest bounty in the database."""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    sql = """
        SELECT 
            CONCAT(p.First_Name, ' ', COALESCE(p.Last_Name, '')) AS Full_Name,
            br.Amount AS Bounty,
            br.Issue_Date,
            c.Crew_Name,
            sr.Region_Name AS Home_Region
        FROM Bounty_Record br
        INNER JOIN Person p ON br.Person_ID = p.Person_ID
        LEFT JOIN Membership m ON p.Person_ID = m.Person_ID
        LEFT JOIN Crew c ON m.Crew_ID = c.Crew_ID
        LEFT JOIN Island i ON p.Home_Island_ID = i.Island_ID
        LEFT JOIN Sea_Region sr ON i.Region_ID = sr.Region_ID
        WHERE br.Amount = (SELECT MAX(Amount) FROM Bounty_Record)
            AND br.Record_Version = (
                SELECT MAX(Record_Version)
                FROM Bounty_Record
                WHERE Person_ID = br.Person_ID
            )
    """
    
    results = db.execute_query(sql)
    results = format_query_results(results)
    
    return render_template('universal_table.html',
                         query_title='Highest Bounty',
                         description='Maximum active bounty in the database',
                         icon='👑',
                         results=results,
                         back_url=url_for('tactical_analysis'),
                         back_name='Tactical Analysis',
                         now=datetime.now(),
                         show_form=False)


@app.route('/tactical/aggregate/faction-ships', methods=['GET', 'POST'])
def aggregate_faction_ships():
    """Aggregate Query 5: Ship count for specific faction."""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    results = None
    if request.method == 'POST':
        faction_id = request.form.get('faction_id')
        
        sql = """
            SELECT 
                f.Faction_Name,
                COUNT(DISTINCT s.Ship_ID) AS Total_Ships,
                COUNT(DISTINCT c.Crew_ID) AS Allied_Crews,
                GROUP_CONCAT(DISTINCT s.Class ORDER BY s.Class SEPARATOR ', ') AS Ship_Classes
            FROM Faction f
            LEFT JOIN Allegiance a ON f.Faction_ID = a.Faction_ID
            LEFT JOIN Crew c ON a.Crew_ID = c.Crew_ID
            LEFT JOIN Ship s ON c.Crew_ID = s.Owning_Crew_ID
            WHERE f.Faction_ID = %s
            GROUP BY f.Faction_ID, f.Faction_Name
        """
        
        results = db.execute_query(sql, (faction_id,))
        results = format_query_results(results)
    
    # Get faction list for dropdown
    factions_sql = "SELECT Faction_ID, Faction_Name FROM Faction ORDER BY Faction_Name"
    factions = db.execute_query(factions_sql)
    faction_options = [(f['Faction_ID'], f['Faction_Name']) for f in factions]
    
    form_fields = [
        {'name': 'faction_id', 'label': 'Select Faction', 'type': 'select', 'options': faction_options, 'required': True, 'col_width': 12}
    ]
    
    return render_template('universal_table.html',
                         query_title='Faction Ship Count',
                         description='Naval assets controlled by faction',
                         icon='⚓',
                         results=results,
                         back_url=url_for('tactical_analysis'),
                         back_name='Tactical Analysis',
                         now=datetime.now(),
                         show_form=True,
                         form_action=url_for('aggregate_faction_ships'),
                         form_fields=form_fields)


# ============================================================================
# TACTICAL ANALYSIS HUB - COMPLEX REPORTS
# ============================================================================

@app.route('/tactical/report/regional-threat')
def regional_threat_assessment():
    """Complex Report 3: Top 10 pirates by region."""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    sql = """
        SELECT * FROM (
            SELECT 
                sr.Region_Name,
                CONCAT(p.First_Name, ' ', COALESCE(p.Last_Name, '')) AS Pirate_Name,
                br.Amount AS Bounty,
                c.Crew_Name,
                p.Status,
                RANK() OVER (PARTITION BY sr.Region_ID ORDER BY br.Amount DESC) AS Regional_Rank
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
            LEFT JOIN Membership m ON p.Person_ID = m.Person_ID
            LEFT JOIN Crew c ON m.Crew_ID = c.Crew_ID
        ) AS ranked_pirates
        WHERE Regional_Rank <= 10
        ORDER BY Region_Name, Regional_Rank
    """
    
    results = db.execute_query(sql)
    results = format_query_results(results)
    
    return render_template('reports/regional_threat_assessment.html',
                         results=results,
                         now=datetime.now())


@app.route('/tactical/report/devil-fruit-dossier')
def devil_fruit_dossier():
    """Complex Report 4: Devil Fruit registry with users."""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    sql = """
        SELECT 
            df.Fruit_Name,
            df.Type,
            df.is_Awakened,
            CONCAT(p.First_Name, ' ', COALESCE(p.Last_Name, '')) AS `Current_User`,
            p.Status AS User_Status,
            f.Faction_Name,
            c.Crew_Name
        FROM Devil_Fruit df
        LEFT JOIN Devil_Fruit_Possession dfp ON df.Fruit_ID = dfp.Fruit_ID
        LEFT JOIN Person p ON dfp.Person_ID = p.Person_ID
        LEFT JOIN Membership m ON p.Person_ID = m.Person_ID
        LEFT JOIN Crew c ON m.Crew_ID = c.Crew_ID
        LEFT JOIN Allegiance a ON c.Crew_ID = a.Crew_ID
        LEFT JOIN Faction f ON a.Faction_ID = f.Faction_ID
        ORDER BY df.Type, df.Fruit_Name
    """
    
    results = db.execute_query(sql)
    results = format_query_results(results)
    
    return render_template('reports/devil_fruit_dossier.html',
                         results=results,
                         now=datetime.now())


@app.route('/tactical/report/territories')
def territories_overview():
    """Complex Report 6: Territory control overview."""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    sql = """
        SELECT 
            i.Island_Name,
            sr.Region_Name,
            i.Climate,
            i.Population,
            f.Faction_Name AS Controlling_Faction,
            c.Crew_Name AS Controlling_Crew,
            CONCAT(leader.First_Name, ' ', COALESCE(leader.Last_Name, '')) AS Faction_Leader
        FROM Island i
        INNER JOIN Sea_Region sr ON i.Region_ID = sr.Region_ID
        LEFT JOIN Territory t ON i.Island_ID = t.Island_ID
        LEFT JOIN Faction f ON t.Faction_ID = f.Faction_ID
        LEFT JOIN Crew c ON t.Crew_ID = c.Crew_ID
        LEFT JOIN Person leader ON f.Leader_ID = leader.Person_ID
        ORDER BY sr.Region_Name, i.Population DESC
    """
    
    results = db.execute_query(sql)
    results = format_query_results(results)
    
    return render_template('reports/territories_overview.html',
                         results=results,
                         now=datetime.now())


# ============================================================================
# COMMAND OPERATIONS HUB - INSERT OPERATIONS
# ============================================================================

@app.route('/command/insert/register-person', methods=['GET', 'POST'])
def register_person():
    """Insert Operation 1: Register new person with home island validation."""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    message = None
    message_type = None
    
    if request.method == 'POST':
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        dob = request.form.get('dob')
        home_island_id = request.form.get('home_island_id')
        status = request.form.get('status', 'Active')
        
        # Validate home island exists
        check_sql = "SELECT Island_ID FROM Island WHERE Island_ID = %s"
        island_check = db.execute_query(check_sql, (home_island_id,))
        
        if not island_check:
            message = f"❌ Home Island ID {home_island_id} does not exist!"
            message_type = "error"
        else:
            insert_sql = """
                INSERT INTO Person (First_Name, Last_Name, Date_of_Birth, Home_Island_ID, Status)
                VALUES (%s, %s, %s, %s, %s)
            """
            try:
                db.execute_query(insert_sql, (first_name, last_name, dob, home_island_id, status))
                message = f"✅ Successfully registered {first_name} {last_name}!"
                message_type = "success"
            except Exception as e:
                message = f"❌ Error: {str(e)}"
                message_type = "error"
    
    # Get islands for dropdown
    islands_sql = "SELECT Island_ID, Island_Name FROM Island ORDER BY Island_Name"
    islands = db.execute_query(islands_sql)
    
    return render_template('operations/register_person.html',
                         islands=islands,
                         message=message,
                         message_type=message_type,
                         now=datetime.now())


@app.route('/command/insert/issue-bounty', methods=['GET', 'POST'])
def issue_bounty():
    """Insert Operation 2: Issue bounty for pirate with validation."""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    message = None
    message_type = None
    
    if request.method == 'POST':
        person_id = request.form.get('person_id')
        amount = request.form.get('amount')
        issue_date = request.form.get('issue_date')
        
        # Verify person exists and is a pirate
        check_sql = """
            SELECT p.Person_ID, CONCAT(p.First_Name, ' ', COALESCE(p.Last_Name, '')) AS Name
            FROM Person p
            INNER JOIN Pirate pi ON p.Person_ID = pi.Person_ID
            WHERE p.Person_ID = %s
        """
        pirate_check = db.execute_query(check_sql, (person_id,))
        
        if not pirate_check:
            message = f"❌ Person ID {person_id} does not exist or is not a pirate!"
            message_type = "error"
        else:
            # Get latest record version
            version_sql = """
                SELECT COALESCE(MAX(Record_Version), 0) + 1 AS Next_Version
                FROM Bounty_Record
                WHERE Person_ID = %s
            """
            version_result = db.execute_query(version_sql, (person_id,))
            next_version = version_result[0]['Next_Version']
            
            insert_sql = """
                INSERT INTO Bounty_Record (Person_ID, Amount, Issue_Date, Record_Version)
                VALUES (%s, %s, %s, %s)
            """
            try:
                db.execute_query(insert_sql, (person_id, amount, issue_date, next_version))
                message = f"✅ Successfully issued bounty of ฿{amount:,} for {pirate_check[0]['Name']}!"
                message_type = "success"
            except Exception as e:
                message = f"❌ Error: {str(e)}"
                message_type = "error"
    
    # Get pirates for dropdown
    pirates_sql = """
        SELECT p.Person_ID, CONCAT(p.First_Name, ' ', COALESCE(p.Last_Name, '')) AS Name
        FROM Person p
        INNER JOIN Pirate pi ON p.Person_ID = pi.Person_ID
        ORDER BY p.First_Name
    """
    pirates = db.execute_query(pirates_sql)
    
    return render_template('operations/issue_bounty.html',
                         pirates=pirates,
                         message=message,
                         message_type=message_type,
                         now=datetime.now())


@app.route('/command/insert/commission-ship', methods=['GET', 'POST'])
def commission_ship():
    """Insert Operation 3: Commission new ship with crew validation."""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    message = None
    message_type = None
    
    if request.method == 'POST':
        ship_name = request.form.get('ship_name', '').strip()
        ship_class = request.form.get('ship_class', '').strip()
        owning_crew_id = request.form.get('owning_crew_id')
        commission_date = request.form.get('commission_date')
        
        # Validate crew exists
        check_sql = "SELECT Crew_ID, Crew_Name FROM Crew WHERE Crew_ID = %s"
        crew_check = db.execute_query(check_sql, (owning_crew_id,))
        
        if owning_crew_id and not crew_check:
            message = f"❌ Crew ID {owning_crew_id} does not exist!"
            message_type = "error"
        else:
            insert_sql = """
                INSERT INTO Ship (Ship_Name, Class, Owning_Crew_ID, Commission_Date)
                VALUES (%s, %s, %s, %s)
            """
            try:
                db.execute_query(insert_sql, (ship_name, ship_class, owning_crew_id if owning_crew_id else None, commission_date))
                message = f"✅ Successfully commissioned {ship_name}!"
                message_type = "success"
            except Exception as e:
                message = f"❌ Error: {str(e)}"
                message_type = "error"
    
    # Get crews for dropdown
    crews_sql = "SELECT Crew_ID, Crew_Name FROM Crew ORDER BY Crew_Name"
    crews = db.execute_query(crews_sql)
    
    return render_template('operations/commission_ship.html',
                         crews=crews,
                         message=message,
                         message_type=message_type,
                         now=datetime.now())


@app.route('/command/insert/log-devil-fruit', methods=['GET', 'POST'])
def log_devil_fruit():
    """Insert Operation 4: Register Devil Fruit with type validation."""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    message = None
    message_type = None
    
    if request.method == 'POST':
        fruit_name = request.form.get('fruit_name', '').strip()
        fruit_type = request.form.get('fruit_type')
        is_awakened = request.form.get('is_awakened') == 'on'
        
        # Validate ENUM type
        if fruit_type not in ['Paramecia', 'Zoan', 'Logia']:
            message = f"❌ Invalid fruit type! Must be Paramecia, Zoan, or Logia."
            message_type = "error"
        else:
            insert_sql = """
                INSERT INTO Devil_Fruit (Fruit_Name, Type, is_Awakened)
                VALUES (%s, %s, %s)
            """
            try:
                db.execute_query(insert_sql, (fruit_name, fruit_type, is_awakened))
                message = f"✅ Successfully registered {fruit_name} ({fruit_type})!"
                message_type = "success"
            except Exception as e:
                message = f"❌ Error: {str(e)}"
                message_type = "error"
    
    return render_template('operations/log_devil_fruit.html',
                         message=message,
                         message_type=message_type,
                         now=datetime.now())


@app.route('/command/insert/form-crew', methods=['GET', 'POST'])
def form_crew():
    """Insert Operation 5: Create new crew with date validation."""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    message = None
    message_type = None
    
    if request.method == 'POST':
        crew_name = request.form.get('crew_name', '').strip()
        date_formed = request.form.get('date_formed')
        status = request.form.get('status', 'Active')
        
        # Validate date not in future
        from datetime import datetime as dt
        today = dt.now().date()
        formed_date = dt.strptime(date_formed, '%Y-%m-%d').date()
        
        if formed_date > today:
            message = f"❌ Formation date cannot be in the future!"
            message_type = "error"
        else:
            insert_sql = """
                INSERT INTO Crew (Crew_Name, Date_Formed, Status)
                VALUES (%s, %s, %s)
            """
            try:
                db.execute_query(insert_sql, (crew_name, date_formed, status))
                message = f"✅ Successfully formed crew '{crew_name}'!"
                message_type = "success"
            except Exception as e:
                message = f"❌ Error: {str(e)}"
                message_type = "error"
    
    return render_template('operations/form_crew.html',
                         message=message,
                         message_type=message_type,
                         now=datetime.now())


# ============================================================================
# COMMAND OPERATIONS HUB - UPDATE OPERATIONS
# ============================================================================

@app.route('/command/update/update-bounty', methods=['GET', 'POST'])
def update_bounty():
    """Update Operation 1: Update pirate bounty with versioned record."""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    message = None
    message_type = None
    
    if request.method == 'POST':
        person_id = request.form.get('person_id')
        new_amount = request.form.get('new_amount')
        issue_date = request.form.get('issue_date')
        
        # Get latest record version
        version_sql = """
            SELECT COALESCE(MAX(Record_Version), 0) + 1 AS Next_Version
            FROM Bounty_Record
            WHERE Person_ID = %s
        """
        version_result = db.execute_query(version_sql, (person_id,))
        next_version = version_result[0]['Next_Version']
        
        # Insert new bounty record
        insert_sql = """
            INSERT INTO Bounty_Record (Person_ID, Amount, Issue_Date, Record_Version)
            VALUES (%s, %s, %s, %s)
        """
        try:
            db.execute_query(insert_sql, (person_id, new_amount, issue_date, next_version))
            message = f"✅ Successfully updated bounty to ฿{int(new_amount):,}!"
            message_type = "success"
        except Exception as e:
            message = f"❌ Error: {str(e)}"
            message_type = "error"
    
    # Get pirates with current bounties
    pirates_sql = """
        SELECT 
            p.Person_ID,
            CONCAT(p.First_Name, ' ', COALESCE(p.Last_Name, '')) AS Name,
            br.Amount AS Current_Bounty
        FROM Person p
        INNER JOIN Pirate pi ON p.Person_ID = pi.Person_ID
        LEFT JOIN Bounty_Record br ON p.Person_ID = br.Person_ID
            AND br.Record_Version = (
                SELECT MAX(Record_Version)
                FROM Bounty_Record
                WHERE Person_ID = p.Person_ID
            )
        ORDER BY p.First_Name
    """
    pirates = db.execute_query(pirates_sql)
    
    return render_template('operations/update_bounty.html',
                         pirates=pirates,
                         message=message,
                         message_type=message_type,
                         now=datetime.now())


@app.route('/command/update/update-marine-rank', methods=['GET', 'POST'])
def update_marine_rank():
    """Update Operation 4: Update Marine Officer rank."""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    message = None
    message_type = None
    
    if request.method == 'POST':
        person_id = request.form.get('person_id')
        new_rank = request.form.get('new_rank')
        
        update_sql = "UPDATE Marine_Officer SET `Rank` = %s WHERE Person_ID = %s"
        try:
            db.execute_query(update_sql, (new_rank, person_id))
            message = f"✅ Successfully updated Marine rank to {new_rank}!"
            message_type = "success"
        except Exception as e:
            message = f"❌ Error: {str(e)}"
            message_type = "error"
    
    # Get marines for dropdown
    marines_sql = """
        SELECT p.Person_ID, CONCAT(p.First_Name, ' ', COALESCE(p.Last_Name, '')) AS Name, mo.`Rank`
        FROM Person p
        INNER JOIN Marine_Officer mo ON p.Person_ID = mo.Person_ID
        ORDER BY p.First_Name
    """
    marines = db.execute_query(marines_sql)
    
    ranks = ['Fleet Admiral', 'Admiral', 'Vice Admiral', 'Rear Admiral', 'Commodore', 'Captain', 'Commander', 'Lieutenant Commander', 'Lieutenant', 'Lieutenant Junior Grade', 'Ensign']
    
    return render_template('operations/update_marine_rank.html',
                         marines=marines,
                         ranks=ranks,
                         message=message,
                         message_type=message_type,
                         now=datetime.now())


@app.route('/command/update/change-status', methods=['GET', 'POST'])
def change_status():
    """Update Operation 2: Change person status."""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    message = None
    message_type = None
    
    if request.method == 'POST':
        person_id = request.form.get('person_id')
        new_status = request.form.get('new_status')
        
        update_sql = "UPDATE Person SET Status = %s WHERE Person_ID = %s"
        try:
            db.execute_query(update_sql, (new_status, person_id))
            message = f"✅ Successfully changed status to {new_status}!"
            message_type = "success"
        except Exception as e:
            message = f"❌ Error: {str(e)}"
            message_type = "error"
    
    # Get persons for dropdown
    persons_sql = """
        SELECT Person_ID, CONCAT(First_Name, ' ', COALESCE(Last_Name, '')) AS Name, Status
        FROM Person
        ORDER BY First_Name
    """
    persons = db.execute_query(persons_sql)
    
    return render_template('operations/change_status.html',
                         persons=persons,
                         message=message,
                         message_type=message_type,
                         now=datetime.now())


@app.route('/command/update/record-fruit-consumption', methods=['GET', 'POST'])
def record_fruit_consumption():
    """Update Operation 3: Record Devil Fruit consumption with transaction."""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    message = None
    message_type = None
    
    if request.method == 'POST':
        person_id = request.form.get('person_id')
        fruit_id = request.form.get('fruit_id')
        date_consumed = request.form.get('date_consumed')
        
        # Check if fruit is already possessed
        check_sql = """
            SELECT Person_ID FROM Devil_Fruit_Possession
            WHERE Fruit_ID = %s AND Date_Lost IS NULL
        """
        existing = db.execute_query(check_sql, (fruit_id,))
        
        if existing:
            message = f"❌ This fruit is already possessed by Person ID {existing[0]['Person_ID']}!"
            message_type = "error"
        else:
            insert_sql = """
                INSERT INTO Devil_Fruit_Possession (Person_ID, Fruit_ID, Date_Consumed)
                VALUES (%s, %s, %s)
            """
            try:
                db.execute_query(insert_sql, (person_id, fruit_id, date_consumed))
                message = f"✅ Successfully recorded fruit consumption!"
                message_type = "success"
            except Exception as e:
                message = f"❌ Error: {str(e)}"
                message_type = "error"
    
    # Get persons and fruits
    persons_sql = "SELECT Person_ID, CONCAT(First_Name, ' ', COALESCE(Last_Name, '')) AS Name FROM Person ORDER BY First_Name"
    persons = db.execute_query(persons_sql)
    
    fruits_sql = "SELECT Fruit_ID, Fruit_Name, Type FROM Devil_Fruit ORDER BY Fruit_Name"
    fruits = db.execute_query(fruits_sql)
    
    return render_template('operations/record_fruit_consumption.html',
                         persons=persons,
                         fruits=fruits,
                         message=message,
                         message_type=message_type,
                         now=datetime.now())


@app.route('/command/update/remove-territory-control', methods=['GET', 'POST'])
def remove_territory_control():
    """Update Operation 5: Clear territory control."""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    message = None
    message_type = None
    
    if request.method == 'POST':
        island_id = request.form.get('island_id')
        
        update_sql = """
            UPDATE Territory
            SET Faction_ID = NULL, Crew_ID = NULL
            WHERE Island_ID = %s
        """
        try:
            db.execute_query(update_sql, (island_id,))
            message = f"✅ Successfully removed territory control!"
            message_type = "success"
        except Exception as e:
            message = f"❌ Error: {str(e)}"
            message_type = "error"
    
    # Get territories with current control
    territories_sql = """
        SELECT i.Island_ID, i.Island_Name, f.Faction_Name, c.Crew_Name
        FROM Island i
        LEFT JOIN Territory t ON i.Island_ID = t.Island_ID
        LEFT JOIN Faction f ON t.Faction_ID = f.Faction_ID
        LEFT JOIN Crew c ON t.Crew_ID = c.Crew_ID
        WHERE t.Faction_ID IS NOT NULL OR t.Crew_ID IS NOT NULL
        ORDER BY i.Island_Name
    """
    territories = db.execute_query(territories_sql)
    
    return render_template('operations/remove_territory_control.html',
                         territories=territories,
                         message=message,
                         message_type=message_type,
                         now=datetime.now())


# ============================================================================
# COMMAND OPERATIONS HUB - DELETE OPERATIONS
# ============================================================================

@app.route('/command/delete/decommission-ship', methods=['GET', 'POST'])
def decommission_ship():
    """Delete Operation 1: Decommission ship with cascade handling."""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    message = None
    message_type = None
    
    if request.method == 'POST':
        ship_id = request.form.get('ship_id')
        
        delete_sql = "DELETE FROM Ship WHERE Ship_ID = %s"
        try:
            db.execute_query(delete_sql, (ship_id,))
            message = f"✅ Successfully decommissioned ship!"
            message_type = "success"
        except Exception as e:
            message = f"❌ Error: {str(e)}"
            message_type = "error"
    
    # Get ships
    ships_sql = """
        SELECT s.Ship_ID, s.Ship_Name, c.Crew_Name
        FROM Ship s
        LEFT JOIN Crew c ON s.Owning_Crew_ID = c.Crew_ID
        ORDER BY s.Ship_Name
    """
    ships = db.execute_query(ships_sql)
    
    return render_template('operations/decommission_ship.html',
                         ships=ships,
                         message=message,
                         message_type=message_type,
                         now=datetime.now())


@app.route('/command/delete/disband-crew', methods=['GET', 'POST'])
def disband_crew():
    """Delete Operation 2: Disband crew and clear memberships."""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    message = None
    message_type = None
    
    if request.method == 'POST':
        crew_id = request.form.get('crew_id')
        
        # First clear memberships
        clear_sql = "UPDATE Membership SET Crew_ID = NULL WHERE Crew_ID = %s"
        try:
            db.execute_query(clear_sql, (crew_id,))
            message = f"✅ Successfully disbanded crew and cleared memberships!"
            message_type = "success"
        except Exception as e:
            message = f"❌ Error: {str(e)}"
            message_type = "error"
    
    # Get crews
    crews_sql = """
        SELECT c.Crew_ID, c.Crew_Name, COUNT(m.Person_ID) AS Member_Count
        FROM Crew c
        LEFT JOIN Membership m ON c.Crew_ID = m.Crew_ID
        GROUP BY c.Crew_ID, c.Crew_Name
        ORDER BY c.Crew_Name
    """
    crews = db.execute_query(crews_sql)
    
    return render_template('operations/disband_crew.html',
                         crews=crews,
                         message=message,
                         message_type=message_type,
                         now=datetime.now())


# READ OPERATIONS (Queries)

@app.route('/query/wanted_poster', methods=['GET', 'POST'])
def wanted_poster_search():
    """Query 1: Search for pirates by name, bounty range, and/or sea region."""
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
        
        print(f"[DEBUG] search_type: {search_type}, name: {search_name}, min: {min_bounty}, max: {max_bounty}, region: {region_id}")
        
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
            # If no bounty filters, show all (no additional WHERE needed)
        
        elif search_type == 'region' and region_id:
            sql += " AND sr.Region_ID = %s"
            params.append(int(region_id))
        
        sql += " ORDER BY COALESCE(br.Amount, 0) DESC, p.First_Name"
        
        # Execute query with or without params
        if params:
            results = db.execute_query(sql, tuple(params))
        else:
            results = db.execute_query(sql)
        results = format_query_results(results)
    
    return render_template('queries/wanted_poster.html', 
                         results=results, 
                         regions=regions,
                         search_type=search_type,
                         search_name=search_name,
                         min_bounty=min_bounty,
                         max_bounty=max_bounty,
                         region_id=region_id)


@app.route('/query/devil_fruits', methods=['GET', 'POST'])
def devil_fruit_encyclopedia():
    """Query 2: List all Devil Fruits with sorting and filtering options."""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    # Default values
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
    
    print(f"[DEBUG] Devil Fruits - sort_by: {sort_by}, awakened: {show_awakened}, active: {show_active}")
    
    results = db.execute_query(sql, tuple(params)) if params else db.execute_query(sql)
    results = format_query_results(results)
    
    return render_template('queries/devil_fruits.html', 
                         results=results,
                         sort_by=sort_by,
                         show_awakened=show_awakened,
                         show_active=show_active)


@app.route('/query/territory_map', methods=['GET'])
def territory_map():
    """Query 3: Show territory control (XOR: Faction or Crew)."""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    sql = """
        SELECT 
            i.Island_ID,
            i.Island_Name,
            i.Climate,
            i.Population,
            sr.Region_Name,
            CASE 
                WHEN t.Faction_ID IS NOT NULL THEN f.Faction_Name
                WHEN t.Crew_ID IS NOT NULL THEN c.Crew_Name
                ELSE 'Unclaimed Territory'
            END AS Controller,
            CASE 
                WHEN t.Faction_ID IS NOT NULL THEN 'Faction'
                WHEN t.Crew_ID IS NOT NULL THEN 'Crew'
                ELSE 'None'
            END AS Controller_Type,
            t.Date_Acquired,
            t.Control_Level
        FROM Island i
        INNER JOIN Sea_Region sr ON i.Region_ID = sr.Region_ID
        LEFT JOIN Territory t ON i.Island_ID = t.Island_ID
        LEFT JOIN Faction f ON t.Faction_ID = f.Faction_ID
        LEFT JOIN Crew c ON t.Crew_ID = c.Crew_ID
        ORDER BY sr.Region_Name, i.Island_Name
    """
    
    results = db.execute_query(sql)
    results = format_query_results(results)
    
    return render_template('queries/territory_map.html', results=results)


@app.route('/query/crew_manifest', methods=['GET', 'POST'])
def crew_manifest():
    """Query 4: Show crew members, ship, and total bounty."""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    crew_list = None
    manifest_data = None
    
    # Get list of all crews for dropdown
    crew_sql = "SELECT Crew_ID, Crew_Name FROM Crew ORDER BY Crew_Name"
    crew_list = db.execute_query(crew_sql)
    
    if request.method == 'POST':
        crew_id = request.form.get('crew_id')
        
        # Get crew info and ship
        crew_info_sql = """
            SELECT 
                c.Crew_ID,
                c.Crew_Name,
                c.Date_Formed,
                c.Status,
                s.Ship_Name,
                s.Class AS Ship_Class
            FROM Crew c
            LEFT JOIN Ship s ON c.Crew_ID = s.Owning_Crew_ID
            WHERE c.Crew_ID = %s
        """
        
        # Get crew members with details
        members_sql = """
            SELECT 
                p.Person_ID,
                p.First_Name,
                p.Last_Name,
                p.Status,
                COALESCE(br.Amount, 0) AS Bounty,
                df.Fruit_Name,
                m.Role
            FROM Membership m
            INNER JOIN Person p ON m.Person_ID = p.Person_ID
            LEFT JOIN Pirate pi ON p.Person_ID = pi.Person_ID
            LEFT JOIN Bounty_Record br ON p.Person_ID = br.Person_ID 
                AND br.Record_Version = (
                    SELECT MAX(Record_Version) 
                    FROM Bounty_Record 
                    WHERE Person_ID = p.Person_ID
                )
            LEFT JOIN Devil_Fruit_Possession dfp ON p.Person_ID = dfp.Person_ID
            LEFT JOIN Devil_Fruit df ON dfp.Fruit_ID = df.Fruit_ID
            WHERE m.Crew_ID = %s
            ORDER BY p.First_Name
        """
        
        # Get total bounty
        total_bounty_sql = """
            SELECT SUM(br.Amount) AS Total_Bounty
            FROM Membership m
            INNER JOIN Pirate pi ON m.Person_ID = pi.Person_ID
            LEFT JOIN Bounty_Record br ON pi.Person_ID = br.Person_ID
                AND br.Record_Version = (
                    SELECT MAX(Record_Version)
                    FROM Bounty_Record
                    WHERE Person_ID = pi.Person_ID
                )
            WHERE m.Crew_ID = %s
        """
        
        crew_info = db.execute_query(crew_info_sql, (crew_id,))
        members = db.execute_query(members_sql, (crew_id,))
        total_bounty = db.execute_query(total_bounty_sql, (crew_id,))
        
        manifest_data = {
            'crew_info': crew_info[0] if crew_info else None,
            'members': members if members else [],
            'total_bounty': total_bounty[0]['Total_Bounty'] if total_bounty and total_bounty[0]['Total_Bounty'] else 0
        }
    
    return render_template('queries/crew_manifest.html', crew_list=crew_list, manifest_data=manifest_data)


@app.route('/query/threat_report', methods=['GET', 'POST'])
def regional_threat_report():
    """Query 5: Count pirates in each sea region."""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    results = None
    
    if request.method == 'POST':
        region_id = request.form.get('region_id', '')
        
        if region_id:
            # Specific region threat analysis
            sql = """
                SELECT 
                    sr.Region_Name,
                    sr.Threat_Level,
                    COUNT(DISTINCT pi.Person_ID) AS Pirate_Count,
                    SUM(br.Amount) AS Total_Bounties,
                    AVG(br.Amount) AS Avg_Bounty,
                    MAX(br.Amount) AS Highest_Bounty
                FROM Sea_Region sr
                LEFT JOIN Island i ON sr.Region_ID = i.Region_ID
                LEFT JOIN Person p ON i.Island_ID = p.Home_Island_ID
                LEFT JOIN Pirate pi ON p.Person_ID = pi.Person_ID
                LEFT JOIN Bounty_Record br ON pi.Person_ID = br.Person_ID
                    AND br.Record_Version = (
                        SELECT MAX(Record_Version)
                        FROM Bounty_Record
                        WHERE Person_ID = pi.Person_ID
                    )
                WHERE sr.Region_ID = %s AND p.Status = 'Active'
                GROUP BY sr.Region_ID, sr.Region_Name, sr.Threat_Level
            """
            results = db.execute_query(sql, (region_id,))
        else:
            # All regions summary
            sql = """
                SELECT 
                    sr.Region_Name,
                    sr.Threat_Level,
                    COUNT(DISTINCT pi.Person_ID) AS Pirate_Count,
                    SUM(br.Amount) AS Total_Bounties
                FROM Sea_Region sr
                LEFT JOIN Island i ON sr.Region_ID = i.Region_ID
                LEFT JOIN Person p ON i.Island_ID = p.Home_Island_ID
                LEFT JOIN Pirate pi ON p.Person_ID = pi.Person_ID
                LEFT JOIN Bounty_Record br ON pi.Person_ID = br.Person_ID
                    AND br.Record_Version = (
                        SELECT MAX(Record_Version)
                        FROM Bounty_Record
                        WHERE Person_ID = pi.Person_ID
                    )
                WHERE p.Status = 'Active' OR p.Status IS NULL
                GROUP BY sr.Region_ID, sr.Region_Name, sr.Threat_Level
                ORDER BY Total_Bounties DESC
            """
            results = db.execute_query(sql)
        
        results = format_query_results(results)
    
    # Get region list for dropdown
    region_sql = "SELECT Region_ID, Region_Name FROM Sea_Region ORDER BY Region_Name"
    regions = db.execute_query(region_sql)
    
    return render_template('queries/threat_report.html', results=results, regions=regions)


@app.route('/query/faction_power', methods=['GET'])
def faction_power_report():
    """Query 6: Faction Power Analysis - Complex Multi-Table JOIN with Aggregation (Phase 1 Requirement)."""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    # Complex query: Faction → Allegiance → Crew → Membership → Pirate → Bounty_Record + Territory count
    sql = """
        SELECT 
            f.Faction_ID,
            f.Faction_Name,
            f.Ideology,
            CONCAT(leader.First_Name, ' ', COALESCE(leader.Last_Name, '')) AS Leader_Name,
            COUNT(DISTINCT a.Crew_ID) AS Allied_Crew_Count,
            COUNT(DISTINCT t.Island_ID) AS Controlled_Territories,
            COUNT(DISTINCT m.Person_ID) AS Total_Members,
            COALESCE(SUM(br.Amount), 0) AS Total_Bounty_Sum,
            COALESCE(AVG(br.Amount), 0) AS Avg_Bounty,
            COALESCE(MAX(br.Amount), 0) AS Highest_Bounty
        FROM Faction f
        LEFT JOIN Person leader ON f.Leader_ID = leader.Person_ID
        LEFT JOIN Allegiance a ON f.Faction_ID = a.Faction_ID
        LEFT JOIN Crew c ON a.Crew_ID = c.Crew_ID
        LEFT JOIN Membership m ON c.Crew_ID = m.Crew_ID
        LEFT JOIN Pirate pi ON m.Person_ID = pi.Person_ID
        LEFT JOIN Bounty_Record br ON pi.Person_ID = br.Person_ID
            AND br.Record_Version = (
                SELECT MAX(Record_Version)
                FROM Bounty_Record
                WHERE Person_ID = pi.Person_ID
            )
        LEFT JOIN Territory t ON f.Faction_ID = t.Faction_ID
        GROUP BY f.Faction_ID, f.Faction_Name, f.Ideology, Leader_Name
        ORDER BY Total_Bounty_Sum DESC, Allied_Crew_Count DESC
    """
    
    results = db.execute_query(sql)
    results = format_query_results(results)
    
    return render_template('queries/faction_power.html', results=results, now=datetime.now())


@app.route('/query/event_summary', methods=['GET'])
def event_summary():
    """Query 7: Historical Event Summary - Complex Event-Encounter JOIN (Phase 1 Requirement)."""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    # Complex query: Event → Encounter → Crew/Marine/Island
    sql = """
        SELECT 
            e.Event_ID,
            e.Event_Name,
            e.Start_Date,
            e.End_Date,
            DATEDIFF(COALESCE(e.End_Date, CURDATE()), e.Start_Date) AS Duration_Days,
            COUNT(DISTINCT en.Crew_ID) AS Involved_Crews,
            COUNT(DISTINCT en.Marine_ID) AS Involved_Marines,
            i.Island_Name AS Location,
            sr.Region_Name AS Region,
            GROUP_CONCAT(DISTINCT c.Crew_Name SEPARATOR ', ') AS Crew_Names
        FROM Event e
        LEFT JOIN Encounter en ON e.Event_ID = en.Event_ID
        LEFT JOIN Island i ON en.Island_ID = i.Island_ID
        LEFT JOIN Sea_Region sr ON i.Region_ID = sr.Region_ID
        LEFT JOIN Crew c ON en.Crew_ID = c.Crew_ID
        GROUP BY e.Event_ID, e.Event_Name, e.Start_Date, e.End_Date, i.Island_Name, sr.Region_Name
        ORDER BY e.Start_Date DESC
    """
    
    results = db.execute_query(sql)
    results = format_query_results(results)
    
    return render_template('queries/event_summary.html', results=results, now=datetime.now())


# WRITE OPERATIONS (Updates)

@app.route('/update/register_criminal', methods=['GET', 'POST'])
def register_criminal():
    """Update 1: INSERT - Register a new pirate."""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        # Get form data
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        date_of_birth = request.form.get('date_of_birth')
        bounty = request.form.get('bounty', 0)
        infamy_level = request.form.get('infamy_level', 'Unknown')
        
        try:
            # Insert into Person table
            person_sql = """
                INSERT INTO Person (First_Name, Last_Name, Date_Of_Birth, Status)
                VALUES (%s, %s, %s, 'Active')
            """
            affected = db.execute_update(person_sql, (first_name, last_name, date_of_birth))
            
            if affected > 0:
                # Get the last inserted Person_ID
                person_id_sql = "SELECT LAST_INSERT_ID() AS Person_ID"
                result = db.execute_query(person_id_sql)
                person_id = result[0]['Person_ID']
                
                # Insert into Pirate table (no Bounty column in Pirate table)
                pirate_sql = """
                    INSERT INTO Pirate (Person_ID, Infamy_Level)
                    VALUES (%s, %s)
                """
                db.execute_update(pirate_sql, (person_id, infamy_level))
                
                # Insert bounty record if bounty > 0
                if bounty and int(bounty) > 0:
                    bounty_sql = """
                        INSERT INTO Bounty_Record (Person_ID, Record_Version, Issue_Date, Amount)
                        VALUES (%s, 1, CURDATE(), %s)
                    """
                    db.execute_update(bounty_sql, (person_id, bounty))
                
                flash(f'DATABASE SYNCHRONIZED. New criminal registered: {first_name} {last_name} (ID: {person_id})', 'success')
            else:
                flash('DATABASE ERROR: Failed to register criminal.', 'danger')
                
        except Exception as e:
            flash(f'OPERATION FAILED: {str(e)}', 'danger')
        
        return redirect(url_for('dashboard'))
    
    return render_template('updates/register_criminal.html')


@app.route('/update/change_status', methods=['GET', 'POST'])
def update_status():
    """Update 2: UPDATE - Change a person's status."""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        person_id = request.form.get('person_id')
        new_status = request.form.get('new_status')
        
        sql = """
            UPDATE Person
            SET Status = %s
            WHERE Person_ID = %s
        """
        
        affected = db.execute_update(sql, (new_status, person_id))
        
        if affected > 0:
            flash(f'DATABASE SYNCHRONIZED. Person ID {person_id} status updated to: {new_status}', 'success')
        elif affected == 0:
            flash(f'INTELLIGENCE NOT FOUND. No person with ID: {person_id}', 'warning')
        else:
            flash('DATABASE ERROR: Update failed.', 'danger')
        
        return redirect(url_for('dashboard'))
    
    # Get list of people for dropdown
    people_sql = """
        SELECT Person_ID, First_Name, Last_Name, Status
        FROM Person
        ORDER BY Last_Name, First_Name
    """
    people = db.execute_query(people_sql)
    
    return render_template('updates/change_status.html', people=people)


@app.route('/update/revoke_bounty', methods=['GET', 'POST'])
def revoke_bounty():
    """Update 3: DELETE - Remove a bounty record."""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        person_id = request.form.get('person_id')
        record_version = request.form.get('record_version')
        
        sql = """
            DELETE FROM Bounty_Record
            WHERE Person_ID = %s AND Record_Version = %s
        """
        
        affected = db.execute_update(sql, (person_id, record_version))
        
        if affected > 0:
            flash(f'DATABASE SYNCHRONIZED. Bounty record deleted for Person ID: {person_id}, Version: {record_version}', 'success')
        elif affected == 0:
            flash('INTELLIGENCE NOT FOUND. No matching bounty record.', 'warning')
        else:
            flash('DATABASE ERROR: Deletion failed.', 'danger')
        
        return redirect(url_for('dashboard'))
    
    # Get list of bounty records
    bounty_sql = """
        SELECT 
            br.Person_ID,
            br.Record_Version,
            p.First_Name,
            p.Last_Name,
            br.Issue_Date,
            br.Last_Seen_Location
        FROM Bounty_Record br
        INNER JOIN Person p ON br.Person_ID = p.Person_ID
        ORDER BY br.Issue_Date DESC
    """
    bounty_records = db.execute_query(bounty_sql)
    
    return render_template('updates/revoke_bounty.html', bounty_records=bounty_records)


@app.route('/update/territory_control', methods=['GET', 'POST'])
def update_territory_control():
    """Update 4: Territory Control - Enforce XOR Constraint (Faction OR Crew)."""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        island_id = request.form.get('island_id')
        faction_id = request.form.get('faction_id', '').strip()
        crew_id = request.form.get('crew_id', '').strip()
        control_level = request.form.get('control_level', 'Full Control')
        
        # PHASE 3 XOR CONSTRAINT ENFORCEMENT (Python Logic)
        if faction_id and crew_id:
            flash('❌ VIOLATION: Exclusive-OR Constraint (Faction vs Crew). A territory cannot be controlled by BOTH a Faction AND a Crew.', 'danger')
            # Reload form data
            islands = db.execute_query("SELECT Island_ID, Island_Name FROM Island ORDER BY Island_Name")
            factions = db.execute_query("SELECT Faction_ID, Faction_Name FROM Faction ORDER BY Faction_Name")
            crews = db.execute_query("SELECT Crew_ID, Crew_Name FROM Crew ORDER BY Crew_Name")
            return render_template('updates/territory_control.html', islands=islands, factions=factions, crews=crews)
        
        if not faction_id and not crew_id:
            flash('❌ ERROR: You must select either a Faction OR a Crew to control this territory.', 'warning')
            islands = db.execute_query("SELECT Island_ID, Island_Name FROM Island ORDER BY Island_Name")
            factions = db.execute_query("SELECT Faction_ID, Faction_Name FROM Faction ORDER BY Faction_Name")
            crews = db.execute_query("SELECT Crew_ID, Crew_Name FROM Crew ORDER BY Crew_Name")
            return render_template('updates/territory_control.html', islands=islands, factions=factions, crews=crews)
        
        try:
            # Check if territory already exists
            check_sql = "SELECT Island_ID FROM Territory WHERE Island_ID = %s"
            existing = db.execute_query(check_sql, (island_id,))
            
            if existing:
                # UPDATE existing territory (enforce XOR)
                if faction_id:
                    sql = """
                        UPDATE Territory 
                        SET Faction_ID = %s, Crew_ID = NULL, Control_Level = %s, Date_Acquired = CURDATE()
                        WHERE Island_ID = %s
                    """
                    affected = db.execute_update(sql, (faction_id, control_level, island_id))
                else:
                    sql = """
                        UPDATE Territory 
                        SET Crew_ID = %s, Faction_ID = NULL, Control_Level = %s, Date_Acquired = CURDATE()
                        WHERE Island_ID = %s
                    """
                    affected = db.execute_update(sql, (crew_id, control_level, island_id))
                
                if affected > 0:
                    controller = f"Faction ID {faction_id}" if faction_id else f"Crew ID {crew_id}"
                    flash(f'✅ TERRITORY UPDATED. Island ID {island_id} now controlled by {controller}.', 'success')
                else:
                    flash('ERROR: Update failed.', 'danger')
            else:
                # INSERT new territory (enforce XOR)
                if faction_id:
                    sql = """
                        INSERT INTO Territory (Island_ID, Faction_ID, Crew_ID, Control_Level, Date_Acquired)
                        VALUES (%s, %s, NULL, %s, CURDATE())
                    """
                    affected = db.execute_update(sql, (island_id, faction_id, control_level))
                else:
                    sql = """
                        INSERT INTO Territory (Island_ID, Faction_ID, Crew_ID, Control_Level, Date_Acquired)
                        VALUES (%s, NULL, %s, %s, CURDATE())
                    """
                    affected = db.execute_update(sql, (island_id, crew_id, control_level))
                
                if affected > 0:
                    controller = f"Faction ID {faction_id}" if faction_id else f"Crew ID {crew_id}"
                    flash(f'✅ TERRITORY CLAIMED. Island ID {island_id} now controlled by {controller}.', 'success')
                else:
                    flash('ERROR: Insert failed.', 'danger')
                    
        except Exception as e:
            flash(f'OPERATION FAILED: {str(e)}', 'danger')
        
        return redirect(url_for('dashboard'))
    
    # GET request - load form data
    islands = db.execute_query("SELECT Island_ID, Island_Name FROM Island ORDER BY Island_Name")
    factions = db.execute_query("SELECT Faction_ID, Faction_Name FROM Faction ORDER BY Faction_Name")
    crews = db.execute_query("SELECT Crew_ID, Crew_Name FROM Crew ORDER BY Crew_Name")
    
    return render_template('updates/territory_control.html', islands=islands, factions=factions, crews=crews)


# CP0 ADMIN CONSOLE ROUTES

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

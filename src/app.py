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
            br.Last_Seen_Island_ID
        FROM Bounty_Record br
        INNER JOIN Person p ON br.Person_ID = p.Person_ID
        ORDER BY br.Issue_Date DESC
    """
    bounty_records = db.execute_query(bounty_sql)
    
    return render_template('updates/revoke_bounty.html', bounty_records=bounty_records)


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

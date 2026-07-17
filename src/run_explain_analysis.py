"""
Aegis Intelligence DB — EXPLAIN ANALYZE Benchmark Script
Runs before/after timing comparisons for key queries and indexes.
Usage: python3 run_explain_analysis.py
"""

import pymysql
import getpass
import sys
import time

# ──────────────────────────────────────────
#  ANSI colors for terminal readability
# ──────────────────────────────────────────
G  = "\033[92m"   # green
Y  = "\033[93m"   # yellow
R  = "\033[91m"   # red
B  = "\033[94m"   # blue
W  = "\033[97m"   # white bold
RS = "\033[0m"    # reset

def hr(char="─", n=68):
    print(char * n)

def section(title):
    print()
    hr("═")
    print(f"{W}  {title}{RS}")
    hr("═")

def subsection(title):
    print(f"\n{B}▶ {title}{RS}")
    hr("─", 50)

# ──────────────────────────────────────────
#  DB connect
# ──────────────────────────────────────────
def connect():
    print("\n" + "═"*68)
    print(f"{W}  AEGIS INTELLIGENCE — EXPLAIN ANALYZE BENCHMARK{RS}")
    print("═"*68)
    password = getpass.getpass("\nEnter MySQL root password: ")
    try:
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password=password,
            database='mini_world_db',
            cursorclass=pymysql.cursors.DictCursor,
        )
        print(f"{G}✓ Connected to mini_world_db{RS}")
        return conn
    except pymysql.Error as e:
        print(f"{R}✗ Connection failed: {e}{RS}")
        sys.exit(1)

# ──────────────────────────────────────────
#  Run EXPLAIN ANALYZE and return actual time
# ──────────────────────────────────────────
def run_explain(conn, label, sql):
    with conn.cursor() as cur:
        t0 = time.perf_counter()
        cur.execute("EXPLAIN ANALYZE " + sql)
        rows = cur.fetchall()
        t1 = time.perf_counter()

    wall_ms = (t1 - t0) * 1000.0
    raw = "\n".join(r[list(r.keys())[0]] for r in rows)

    # Extract "actual time=X..Y" — last occurrence is the root node
    import re
    matches = re.findall(r"actual time=([\d.]+)\.\.([\d.]+)", raw)
    if matches:
        start_ms = float(matches[-1][0])
        end_ms   = float(matches[-1][1])
    else:
        start_ms = end_ms = wall_ms

    print(f"  {Y}Wall clock  :{RS} {wall_ms:.3f} ms")
    print(f"  {Y}EXPLAIN end :{RS} {end_ms:.3f} ms  (root node actual time)")
    print(f"\n  {W}Raw EXPLAIN output:{RS}")
    for line in raw.split("\n")[:30]:   # cap output at 30 lines
        print("    " + line)

    return end_ms

# ──────────────────────────────────────────
#  Create / drop index helpers
# ──────────────────────────────────────────
def create_index(conn, name, ddl):
    try:
        with conn.cursor() as cur:
            cur.execute(ddl)
        conn.commit()
        print(f"  {G}✓ Index '{name}' created{RS}")
    except pymysql.err.OperationalError as e:
        if "Duplicate key name" in str(e) or "1061" in str(e):
            print(f"  {Y}⚠ Index '{name}' already exists — dropping and recreating{RS}")
            with conn.cursor() as cur:
                table = ddl.split("ON")[1].split("(")[0].strip()
                cur.execute(f"DROP INDEX `{name}` ON {table}")
                cur.execute(ddl)
            conn.commit()
            print(f"  {G}✓ Index '{name}' recreated{RS}")
        else:
            print(f"  {R}✗ Could not create index: {e}{RS}")

def drop_index_if_exists(conn, name, table):
    try:
        with conn.cursor() as cur:
            cur.execute(f"DROP INDEX `{name}` ON {table}")
        conn.commit()
        print(f"  {Y}(Pre-cleanup: dropped existing '{name}'){RS}")
    except Exception:
        pass   # didn't exist, fine

# ──────────────────────────────────────────
#  THE QUERIES
# ──────────────────────────────────────────

Q_CREW_VALUATION = """
SELECT
    c.Crew_Name,
    COUNT(DISTINCT m.Person_ID)  AS Total_Members,
    SUM(br.Amount)               AS Total_Bounty,
    AVG(br.Amount)               AS Average_Bounty,
    MAX(br.Amount)               AS Highest_Bounty,
    MIN(br.Amount)               AS Lowest_Bounty
FROM Crew c
LEFT JOIN Membership m      ON c.Crew_ID    = m.Crew_ID
LEFT JOIN Pirate pi         ON m.Person_ID  = pi.Person_ID
LEFT JOIN Bounty_Record br  ON pi.Person_ID = br.Person_ID
    AND br.Record_Version = (
        SELECT MAX(Record_Version)
        FROM Bounty_Record
        WHERE Person_ID = pi.Person_ID
    )
GROUP BY c.Crew_ID, c.Crew_Name
"""

Q_BOUNTY_INDEX = """
SELECT
    CONCAT(p.First_Name, ' ', COALESCE(p.Last_Name, '')) AS Pirate_Name,
    COALESCE(br.Amount, 0) AS Bounty
FROM Person p
INNER JOIN Pirate pi        ON p.Person_ID  = pi.Person_ID
LEFT JOIN  Bounty_Record br ON p.Person_ID  = br.Person_ID
    AND br.Record_Version = (
        SELECT MAX(Record_Version)
        FROM Bounty_Record
        WHERE Person_ID = p.Person_ID
    )
ORDER BY Bounty DESC, Pirate_Name
"""

Q_ISLAND_CENSUS = """
SELECT
    sr.Region_Name,
    COUNT(i.Island_ID)              AS Island_Count,
    COALESCE(SUM(i.Population), 0)  AS Total_Population,
    COALESCE(AVG(i.Population), 0)  AS Average_Population,
    GROUP_CONCAT(DISTINCT i.Climate ORDER BY i.Climate SEPARATOR ', ') AS Climate_Types
FROM Sea_Region sr
LEFT JOIN Island i ON sr.Region_ID = i.Region_ID
GROUP BY sr.Region_ID, sr.Region_Name
ORDER BY Island_Count DESC, sr.Region_Name
"""

Q_PIRATE_SEARCH_ALL = """
SELECT
    p.Person_ID,
    p.First_Name, p.Last_Name, p.Status,
    pi.Infamy_Level,
    c.Crew_Name,
    sr.Region_Name,
    COALESCE(br.Amount, 0) as Bounty,
    br.Last_Seen_Location
FROM Person p
INNER JOIN Pirate pi        ON p.Person_ID  = pi.Person_ID
LEFT JOIN  Membership m     ON p.Person_ID  = m.Person_ID
LEFT JOIN  Crew c           ON m.Crew_ID    = c.Crew_ID
LEFT JOIN  Island i         ON p.Home_Island_ID = i.Island_ID
LEFT JOIN  Sea_Region sr    ON i.Region_ID  = sr.Region_ID
LEFT JOIN  Bounty_Record br ON p.Person_ID  = br.Person_ID
    AND br.Record_Version = (
        SELECT MAX(Record_Version)
        FROM Bounty_Record
        WHERE Person_ID = p.Person_ID
    )
ORDER BY COALESCE(br.Amount, 0) DESC, p.First_Name
"""

# ──────────────────────────────────────────
#  MAIN
# ──────────────────────────────────────────
def main():
    conn = connect()
    results = {}

    # ── QUERY 1: Crew Valuation ───────────────────────────────────────────
    section("QUERY 1 — Crew Valuation (multi-join + correlated subquery)")

    subsection("BEFORE — no index on Bounty_Record(Person_ID, Record_Version)")
    drop_index_if_exists(conn, "idx_bounty_person_ver", "Bounty_Record")
    before1 = run_explain(conn, "crew_valuation_before", Q_CREW_VALUATION)
    results["crew_val_before"] = before1

    subsection("Adding index: idx_bounty_person_ver")
    create_index(conn, "idx_bounty_person_ver",
                 "CREATE INDEX idx_bounty_person_ver ON Bounty_Record(Person_ID, Record_Version)")

    subsection("AFTER — with idx_bounty_person_ver")
    after1 = run_explain(conn, "crew_valuation_after", Q_CREW_VALUATION)
    results["crew_val_after"] = after1

    pct1 = ((before1 - after1) / before1 * 100) if before1 > 0 else 0
    print(f"\n  {G}📊 Crew Valuation improvement: {before1:.3f}ms → {after1:.3f}ms  ({pct1:.1f}% faster){RS}")

    # ── QUERY 2: Bounty Index (pirate ranking) ────────────────────────────
    section("QUERY 2 — Bounty Index / Pirate Ranking (correlated subquery on all pirates)")

    subsection("BEFORE — drop Person_ID index temporarily")
    drop_index_if_exists(conn, "idx_pirate_person", "Pirate")
    before2 = run_explain(conn, "bounty_index_before", Q_BOUNTY_INDEX)
    results["bounty_before"] = before2

    subsection("Adding index: idx_pirate_person on Pirate(Person_ID)")
    create_index(conn, "idx_pirate_person",
                 "CREATE INDEX idx_pirate_person ON Pirate(Person_ID)")

    subsection("AFTER — with idx_pirate_person")
    after2 = run_explain(conn, "bounty_index_after", Q_BOUNTY_INDEX)
    results["bounty_after"] = after2

    pct2 = ((before2 - after2) / before2 * 100) if before2 > 0 else 0
    print(f"\n  {G}📊 Bounty Index improvement: {before2:.3f}ms → {after2:.3f}ms  ({pct2:.1f}% faster){RS}")

    # ── QUERY 3: Island Census (GROUP BY aggregate) ───────────────────────
    section("QUERY 3 — Island Census (GROUP BY + SUM/AVG/COUNT aggregate)")

    subsection("BEFORE — drop index on Island(Region_ID)")
    drop_index_if_exists(conn, "idx_island_region", "Island")
    before3 = run_explain(conn, "island_census_before", Q_ISLAND_CENSUS)
    results["census_before"] = before3

    subsection("Adding index: idx_island_region on Island(Region_ID)")
    create_index(conn, "idx_island_region",
                 "CREATE INDEX idx_island_region ON Island(Region_ID)")

    subsection("AFTER — with idx_island_region")
    after3 = run_explain(conn, "island_census_after", Q_ISLAND_CENSUS)
    results["census_after"] = after3

    pct3 = ((before3 - after3) / before3 * 100) if before3 > 0 else 0
    print(f"\n  {G}📊 Island Census improvement: {before3:.3f}ms → {after3:.3f}ms  ({pct3:.1f}% faster){RS}")

    # ── QUERY 4: Full Pirate Search (6-way join) ──────────────────────────
    section("QUERY 4 — Full Pirate Search (6-table join + correlated subquery)")

    subsection("BEFORE (indexes from Q1–Q3 already in place — testing join benefit)")
    drop_index_if_exists(conn, "idx_membership_person", "Membership")
    before4 = run_explain(conn, "pirate_search_before", Q_PIRATE_SEARCH_ALL)
    results["pirate_before"] = before4

    subsection("Adding index: idx_membership_person on Membership(Person_ID)")
    create_index(conn, "idx_membership_person",
                 "CREATE INDEX idx_membership_person ON Membership(Person_ID)")

    subsection("AFTER — with idx_membership_person")
    after4 = run_explain(conn, "pirate_search_after", Q_PIRATE_SEARCH_ALL)
    results["pirate_after"] = after4

    pct4 = ((before4 - after4) / before4 * 100) if before4 > 0 else 0
    print(f"\n  {G}📊 Pirate Search improvement: {before4:.3f}ms → {after4:.3f}ms  ({pct4:.1f}% faster){RS}")

    # ── FINAL SUMMARY ─────────────────────────────────────────────────────
    section("FINAL SUMMARY")
    print(f"""
  {'Query':<35} {'Before':>10} {'After':>10} {'Speedup':>10}
  {'─'*35} {'─'*10} {'─'*10} {'─'*10}
  {'Crew Valuation (corr. subquery)':<35} {before1:>9.3f}ms {after1:>9.3f}ms {pct1:>9.1f}%
  {'Bounty Ranking (corr. subquery)':<35} {before2:>9.3f}ms {after2:>9.3f}ms {pct2:>9.1f}%
  {'Island Census (GROUP BY aggr.)':<35} {before3:>9.3f}ms {after3:>9.3f}ms {pct3:>9.1f}%
  {'Pirate Search (6-table join)':<35} {before4:>9.3f}ms {after4:>9.3f}ms {pct4:>9.1f}%
""")

    avg_improvement = (pct1 + pct2 + pct3 + pct4) / 4
    max_improvement = max(pct1, pct2, pct3, pct4)
    print(f"  {W}Average improvement across 4 queries: {avg_improvement:.1f}%{RS}")
    print(f"  {W}Peak improvement:                     {max_improvement:.1f}%{RS}")
    print()

    hr("═")
    print(f"{W}  INDEXES ADDED (keep these for production performance):{RS}")
    hr("═")
    print("""
  1. Bounty_Record(Person_ID, Record_Version) — speeds correlated subqueries
  2. Pirate(Person_ID)                        — speeds pirate JOIN lookups
  3. Island(Region_ID)                        — speeds region GROUP BY joins
  4. Membership(Person_ID)                    — speeds 6-way pirate searches
""")

    conn.close()
    print(f"{G}Done. Use the numbers above for your resume bullets.{RS}\n")

if __name__ == "__main__":
    main()

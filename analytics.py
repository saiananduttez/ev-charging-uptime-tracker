import sqlite3
import pandas as pd

def run_ev_analytics(db_name="ev_network.db"):
    conn = sqlite3.connect(db_name)
    
    # 1. Station Uptime & Reliability Score (% of time Operational: available or charging)
    uptime_query = """
    SELECT 
        station_name,
        location_zone,
        charger_type,
        COUNT(*) AS total_pings,
        SUM(CASE WHEN status IN ('available', 'charging') THEN 1 ELSE 0 END) AS active_pings,
        ROUND((SUM(CASE WHEN status IN ('available', 'charging') THEN 1.0 ELSE 0.0 END) / COUNT(*)) * 100, 2) AS uptime_pct
    FROM station_heartbeats
    GROUP BY station_id
    ORDER BY uptime_pct ASC;
    """

    # 2. Network Hardware Failure & Outage Breakdown
    fault_query = """
    SELECT 
        error_code,
        COUNT(*) AS occurrence_count
    FROM station_heartbeats
    WHERE error_code != 'OK'
    GROUP BY error_code
    ORDER BY occurrence_count DESC;
    """

    # 3. Zone-Level Operational Performance Summary
    zone_query = """
    SELECT 
        location_zone,
        COUNT(DISTINCT station_id) AS active_chargers,
        ROUND(AVG(CASE WHEN status IN ('available', 'charging') THEN 100.0 ELSE 0.0 END), 2) AS avg_zone_uptime_pct
    FROM station_heartbeats
    GROUP BY location_zone
    ORDER BY avg_zone_uptime_pct DESC;
    """

    df_uptime = pd.read_sql_query(uptime_query, conn)
    df_fault = pd.read_sql_query(fault_query, conn)
    df_zone = pd.read_sql_query(zone_query, conn)
    conn.close()

    print("\n========================================================")
    print("      EV CHARGER UPTIME & RELIABILITY BENCHMARK         ")
    print("========================================================")
    print(df_uptime.to_string(index=False))

    print("\n========================================================")
    print("           NETWORK FAULT & DOWNTIME ROOT CAUSES         ")
    print("========================================================")
    print(df_fault.to_string(index=False))

    print("\n========================================================")
    print("              ZONE OPERATIONAL PERFORMANCE              ")
    print("========================================================")
    print(df_zone.to_string(index=False))

if __name__ == "__main__":
    run_ev_analytics()
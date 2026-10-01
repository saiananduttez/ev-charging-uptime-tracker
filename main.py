import random
import uuid
from datetime import datetime, timedelta
from database import init_db, insert_heartbeats

# Network of public EV stations across municipal zones
STATIONS = [
    ("ST_001", "Downtown Civic Hub", "Zone 1 - Central", "DC Fast (CCS)", 150.0),
    ("ST_002", "Tech Corridor Supercharger", "Zone 2 - North", "DC Fast (CCS)", 250.0),
    ("ST_003", "Metro Station West P&R", "Zone 3 - West", "Level 2 (J1772)", 22.0),
    ("ST_004", "Airport Express Hub", "Zone 4 - South", "DC Fast (CCS)", 350.0),
    ("ST_005", "Shopping Mall East Deck", "Zone 5 - East", "Level 2 (J1772)", 22.0),
    ("ST_006", "Harbor Terminal Gateway", "Zone 1 - Central", "DC Fast (CCS)", 150.0),
    ("ST_007", "Suburban Commuter Depot", "Zone 3 - West", "Level 2 (J1772)", 11.0),
    ("ST_008", "University Campus North", "Zone 2 - North", "DC Fast (CCS)", 120.0),
]

def generate_telemetry(pings_per_station=30):
    """Simulates 24-hour telemetry heartbeats across the charging network."""
    events = []
    base_time = datetime.now() - timedelta(days=1)
    
    statuses = ["available", "charging", "faulted", "offline"]
    fault_codes = ["COMM_TIMEOUT", "CONNECTOR_FAULT", "GROUND_FAULT", "OVERTEMP"]

    for station in STATIONS:
        st_id, name, zone, c_type, power = station
        for h in range(pings_per_station):
            ping_time = base_time + timedelta(hours=h)
            
            # Stations have occasional real-world hardware or connectivity failures
            status = random.choices(statuses, weights=[0.50, 0.38, 0.08, 0.04])[0]
            err = random.choice(fault_codes) if status in ("faulted", "offline") else "OK"

            events.append((
                str(uuid.uuid4())[:8],
                st_id,
                name,
                zone,
                c_type,
                power,
                status,
                err,
                ping_time.strftime("%Y-%m-%d %H:%M:%S")
            ))
            
    return events

if __name__ == "__main__":
    init_db()
    telemetry_data = generate_telemetry(pings_per_station=30)
    insert_heartbeats(telemetry_data)
    print(f"Success: Ingested {len(telemetry_data)} telemetry pings across {len(STATIONS)} EV stations.")
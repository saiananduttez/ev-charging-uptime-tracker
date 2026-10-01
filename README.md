# Public EV Charging Station Availability & Uptime Tracker

An automated IoT telemetry ingestion pipeline and SQL analytics engine tracking municipal electric vehicle (EV) charging station availability, hardware failure modes, and zonal reliability benchmarks.

## Overview
Municipal EV charging networks require high-availability monitoring to satisfy regulatory SLA standards and avoid stranded motorist events. This pipeline simulates high-frequency heartbeat telemetry from public charging infrastructure, loads time-series status pings into a normalized SQLite database, and executes SQL analytical queries to monitor operational reliability, hardware fault trends, and geographic coverage.

## Tech Stack
- Python 3
- pandas, sqlite3, uuid, datetime
- SQLite Relational Database

## Key Features
- IoT Telemetry Ingestion: Ingests 240+ multi-zone station pings tracking charger state (available, charging, faulted, offline) across DC Fast (CCS) and Level 2 (J1772) chargers.
- Root Cause Fault Analysis: Classifies hardware degradation modes (connector wear, ground faults, temperature throttling, network dropouts).
- Municipal SLA Auditing: Computes operational uptime percentages grouped by individual station assets and municipal geographic zones.

## How to Run Locally

Clone or download the repository:
```bash
git clone [https://github.com/saiananduttez/ev-charging-uptime-tracker.git](https://github.com/saiananduttez/ev-charging-uptime-tracker.git)
cd ev-charging-uptime-tracker

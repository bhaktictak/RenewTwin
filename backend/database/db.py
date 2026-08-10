import aiosqlite
import random
import os
from datetime import datetime, timezone

DB_PATH = os.path.join(os.path.dirname(__file__), "renewtwin.db")

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS assets (
                asset_id TEXT PRIMARY KEY,
                asset_type TEXT,
                location TEXT,
                rated_capacity_kw REAL,
                installation_date TEXT,
                current_power_kw REAL,
                expected_power_kw REAL,
                temperature_c REAL,
                defect_class TEXT,
                defect_probability REAL,
                anomaly_score REAL,
                health_score REAL,
                risk_level TEXT,
                maintenance_priority INTEGER,
                last_inspection TEXT,
                recommended_action TEXT,
                status TEXT DEFAULT 'active',
                created_at TEXT,
                updated_at TEXT
            )
        ''')
        await db.execute('CREATE TABLE IF NOT EXISTS predictions (id INTEGER PRIMARY KEY)')
        await db.execute('CREATE TABLE IF NOT EXISTS anomalies (id INTEGER PRIMARY KEY)')
        await db.execute('CREATE TABLE IF NOT EXISTS maintenance_records (id INTEGER PRIMARY KEY)')
        await db.commit()
        
        async with db.execute('SELECT COUNT(*) FROM assets') as cursor:
            count = await cursor.fetchone()
            if count[0] == 0:
                await seed_assets()

async def seed_assets():
    random.seed(42)
    assets = []
    arrays = ['Array A', 'Array B', 'Array C']
    now = datetime.now(timezone.utc).isoformat()
    
    for i in range(1, 25):
        asset_id = f"PV-A-{i:03d}"
        location = random.choice(arrays)
        health_rand = random.random()
        
        if health_rand < 0.60:
            health_score = random.uniform(90, 100)
            risk_level = "HEALTHY"
            defect_class = "none"
            defect_prob = random.uniform(0, 0.1)
        elif health_rand < 0.80:
            health_score = random.uniform(75, 89.9)
            risk_level = "MONITOR"
            defect_class = random.choice(['none', 'soiling', 'shading'])
            defect_prob = random.uniform(0.1, 0.3)
        elif health_rand < 0.95:
            health_score = random.uniform(50, 74.9)
            risk_level = "AT RISK"
            defect_class = random.choice(['hotspot', 'crack', 'soiling'])
            defect_prob = random.uniform(0.3, 0.7)
        else:
            health_score = random.uniform(0, 49.9)
            risk_level = "CRITICAL"
            defect_class = random.choice(['cell_damage', 'hotspot', 'crack'])
            defect_prob = random.uniform(0.7, 1.0)
            
        expected_power = 400.0
        power_ratio = (health_score / 100.0)
        current_power = expected_power * random.uniform(power_ratio - 0.05, power_ratio + 0.05)
        
        temp = random.uniform(40, 85)
        
        assets.append((
            asset_id, 'solar_panel', location, 400.0, "2023-01-01T00:00:00Z",
            current_power, expected_power, temp, defect_class, defect_prob,
            random.uniform(0, 1), health_score, risk_level, 
            int(100 - health_score), "2023-10-01T00:00:00Z",
            f"Inspect {defect_class}" if defect_class != 'none' else 'None',
            'active', now, now
        ))
        
    async with aiosqlite.connect(DB_PATH) as db:
        await db.executemany('''
            INSERT INTO assets VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        ''', assets)
        await db.commit()

async def get_db():
    db = await aiosqlite.connect(DB_PATH)
    db.row_factory = aiosqlite.Row
    return db

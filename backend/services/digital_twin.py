from ..database.db import get_db

class DigitalTwinEngine:
    async def get_assets(self, risk_level: str = None, limit: int = 100):
        db = await get_db()
        query = "SELECT * FROM assets"
        params = []
        if risk_level:
            query += " WHERE risk_level = ?"
            params.append(risk_level)
        query += " LIMIT ?"
        params.append(limit)
        
        async with db.execute(query, params) as cursor:
            rows = await cursor.fetchall()
        await db.close()
        return [dict(row) for row in rows]

    async def get_twin(self, asset_id: str):
        db = await get_db()
        async with db.execute("SELECT * FROM assets WHERE asset_id = ?", (asset_id,)) as cursor:
            row = await cursor.fetchone()
        await db.close()
        if row:
            return dict(row)
        return None

    async def update_twin(self, asset_id: str, prediction_data: dict):
        pass # Optional update logic based on ML prediction
        
    async def get_fleet_summary(self):
        db = await get_db()
        async with db.execute("SELECT * FROM assets") as cursor:
            rows = await cursor.fetchall()
        await db.close()
        
        total = len(rows)
        healthy = sum(1 for r in rows if r['risk_level'] == 'HEALTHY')
        monitor = sum(1 for r in rows if r['risk_level'] == 'MONITOR')
        at_risk = sum(1 for r in rows if r['risk_level'] == 'AT RISK')
        critical = sum(1 for r in rows if r['risk_level'] == 'CRITICAL')
        
        avg_health = sum(r['health_score'] for r in rows) / total if total > 0 else 0
        
        return {
            "total_assets": total,
            "healthy_count": healthy,
            "monitor_count": monitor,
            "at_risk_count": at_risk,
            "critical_count": critical,
            "avg_health_score": avg_health,
            "maintenance_pending": at_risk + critical
        }
        
    async def get_maintenance_priorities(self):
        db = await get_db()
        async with db.execute("SELECT * FROM assets ORDER BY maintenance_priority DESC, health_score ASC") as cursor:
            rows = await cursor.fetchall()
        await db.close()
        
        return [
            {
                "asset_id": r['asset_id'],
                "priority": r['maintenance_priority'],
                "risk_level": r['risk_level'],
                "health_score": r['health_score'],
                "recommended_action": r['recommended_action'],
                "estimated_loss_pct": max(0.0, (r['expected_power_kw'] - r['current_power_kw']) / r['expected_power_kw'] * 100) if r['expected_power_kw'] > 0 else 0.0
            }
            for r in rows
        ]

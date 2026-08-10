def calculate_health(defect_probability: float, anomaly_score: float, current_power: float, expected_power: float, temperature_c: float, defect_class: str) -> dict:
    perf_deviation_ratio = 0.0
    if expected_power > 0:
        perf_deviation_ratio = max(0.0, (expected_power - current_power) / expected_power)
    perf_deviation_ratio = min(1.0, perf_deviation_ratio)
    
    temp_penalty = 0.0
    if temperature_c > 55:
        temp_penalty = min(1.0, (temperature_c - 55) / 30.0)
        
    health_score = 100 - (defect_probability * 40) - (anomaly_score * 30) - (perf_deviation_ratio * 20) - (temp_penalty * 10)
    health_score = max(0.0, min(100.0, health_score))
    
    if health_score >= 90:
        risk_level = "HEALTHY"
    elif health_score >= 75:
        risk_level = "MONITOR"
    elif health_score >= 50:
        risk_level = "AT RISK"
    else:
        risk_level = "CRITICAL"
        
    priority = int(100 - health_score)
    
    recommended_action = "None"
    if risk_level != "HEALTHY":
        if defect_class != 'none':
            recommended_action = f"Inspect and repair {defect_class}"
        else:
            recommended_action = "Routine inspection"
            
    return {
        "health_score": health_score,
        "risk_level": risk_level,
        "maintenance_priority": priority,
        "recommended_action": recommended_action,
        "label": "Prototype Asset Health Index"
    }

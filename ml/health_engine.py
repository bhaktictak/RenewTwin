def compute_health_score(defect_prob, anomaly_score, current_power, expected_power, temperature):
    """
    Computes a Prototype Asset Health Index.
    """
    perf_dev = max(0, (expected_power - current_power) / expected_power) if expected_power > 0 else 0
    temp_penalty = max(0, (temperature - 45) / 45) if temperature > 45 else 0
    
    score = 100 - (defect_prob * 40) - (anomaly_score * 30) - (perf_dev * 20) - (temp_penalty * 10)
    score = max(0, min(100, score))
    
    risk_level = classify_risk(score)
    
    return {
        'health_score': score,
        'risk_level': risk_level,
        'penalties': {
            'defect_penalty': defect_prob * 40,
            'anomaly_penalty': anomaly_score * 30,
            'performance_penalty': perf_dev * 20,
            'temperature_penalty': temp_penalty * 10
        },
        'label': 'Prototype Asset Health Index'
    }

def classify_risk(score):
    if score >= 80:
        return 'HEALTHY'
    elif score >= 60:
        return 'MONITOR'
    elif score >= 40:
        return 'AT_RISK'
    else:
        return 'CRITICAL'

def prioritize_maintenance(assets_list):
    """
    Sort assets based on health score (lowest first).
    """
    return sorted(assets_list, key=lambda x: x.get('health_score', 100))

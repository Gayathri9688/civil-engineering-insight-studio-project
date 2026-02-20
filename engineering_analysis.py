def engineering_analysis(description):
    observations = []
    recommendations = []
    risk = "Low"

    text = description.lower()

    if "collapsed" in text or "destroyed" in text or "demolished" in text:
        observations.append(
            "Severe structural collapse observed indicating failure of primary load-bearing elements."
        )
        recommendations.append(
            "Immediate evacuation and barricading of the affected structure is required."
        )
        recommendations.append(
            "Detailed structural audit must be conducted before any repair or demolition decision."
        )
        risk = "High"

    if "crack" in text or "broken" in text or "fracture" in text:
        observations.append(
            "Visible cracking and fracture of reinforced concrete members detected."
        )
        recommendations.append(
            "Non-destructive testing such as Ultrasonic Pulse Velocity and Rebound Hammer tests are recommended."
        )
        risk = "Medium"

    if "exposed" in text or "steel" in text or "reinforcement" in text:
        observations.append(
            "Exposed reinforcement suggests advanced concrete spalling and durability loss."
        )
        recommendations.append(
            "Corrosion assessment and durability evaluation should be performed."
        )
        risk = "High"

    if not observations:
        observations.append(
            "No major visible structural distress detected from the provided image."
        )
        recommendations.append(
            "Routine inspection and periodic monitoring are advised."
        )

    return observations, recommendations, risk

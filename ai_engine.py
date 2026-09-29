import re

KEYWORDS = {
    "critical": ["death","fatal","fire","collapse","accident","emergency","ambulance","outbreak"],
    "high": ["danger","unsafe","deep","severe","urgent","three days","week","shortage","flood"],
    "medium": ["broken","problem","delay","poor","interruption","garbage","pothole"],
}

DEPARTMENTS = {
    "Roads":"Public Works Department",
    "Water":"Water Supply Department",
    "Sanitation":"Municipal Sanitation Department",
    "Healthcare":"Health Department",
    "Education":"Education Department",
    "Electricity":"Electricity Department",
    "Public Safety":"Public Safety / Municipal Department",
    "Environment":"Environment Department",
    "Other":"Municipal Administration"
}

def _signals(text):
    t = text.lower()
    found = []
    for group, words in KEYWORDS.items():
        for w in words:
            if w in t:
                found.append(w)
    return list(dict.fromkeys(found))

def analyze_request(title, description, category, population):
    text = f"{title} {description}"
    signals = _signals(text)

    score = 25
    if any(s in signals for s in KEYWORDS["critical"]):
        score += 35
    if any(s in signals for s in KEYWORDS["high"]):
        score += 20
    if any(s in signals for s in KEYWORDS["medium"]):
        score += 10

    if population >= 10000:
        score += 20
    elif population >= 5000:
        score += 15
    elif population >= 1000:
        score += 10
    elif population >= 500:
        score += 5

    category_bonus = {
        "Healthcare": 8, "Water": 7, "Public Safety": 7,
        "Roads": 5, "Electricity": 5, "Sanitation": 4,
        "Education": 3, "Environment": 3, "Other": 0
    }
    score += category_bonus.get(category, 0)
    score = min(100, score)

    if score >= 75:
        priority, urgency = "High", "Immediate"
    elif score >= 50:
        priority, urgency = "Medium", "Within 7 days"
    else:
        priority, urgency = "Low", "Routine"

    if priority == "High":
        recommendation = f"Escalate to {DEPARTMENTS.get(category)} for field verification and action planning."
    elif priority == "Medium":
        recommendation = f"Create a service ticket with {DEPARTMENTS.get(category)} and schedule inspection."
    else:
        recommendation = f"Register the issue with {DEPARTMENTS.get(category)} for routine monitoring."

    reason_parts = []
    if signals:
        reason_parts.append("Risk signals detected: " + ", ".join(signals))
    reason_parts.append(f"Estimated affected population: {population:,}.")
    reason_parts.append(f"Category: {category}.")
    reason = " ".join(reason_parts)

    return {
        "priority": priority,
        "priority_score": score,
        "urgency": urgency,
        "signals": signals,
        "reason": reason,
        "recommendation": recommendation,
        "department": DEPARTMENTS.get(category, "Municipal Administration"),
        "latitude": 18.5204,
        "longitude": 73.8567,
    }

def summarize_request(description):
    words = re.findall(r"\w+", description)
    if len(words) <= 30:
        return description
    return " ".join(words[:30]) + "..."

def calculate_trust_score(place_data, osint_data, audit_report):
    """
    Calculates a 0-100 Trust Score based on heuristics and Agent feedback.
    100 = Perfect Trust
    0 = Fraud
    """
    score = 100
    breakdown = []

    # Heuristic 1: Missing Data Penalties
    if not place_data.get('website'):
        score -= 10
        breakdown.append("-10: No Website listed")
    
    if not place_data.get('phone'):
        score -= 20
        breakdown.append("-20: No Phone Number")

    # Heuristic 2: OSINT Signals
    # If we found very few results for a business that should be public
    if len(osint_data) < 2:
        score -= 15
        breakdown.append("-15: Weak Digital Footprint (< 2 external sources)")

    # Heuristic 3: Review Velocity (The "Bot Farm" Detector)
    reviews = place_data.get('reviews', [])
    if reviews:
        # Sort by time
        try:
             timestamps = sorted([r.get('time', 0) for r in reviews], reverse=True)
             if len(timestamps) >= 3:
                 # Check for "Burst" (3 reviews in < 24 hours)
                 latest_three_diff = timestamps[0] - timestamps[2]
                 if latest_three_diff < 86400: # 86400 seconds = 24 hours
                     score -= 30
                     breakdown.append("-30: Review Velocity Spike (Potential Bot Farm)")
        except:
             pass

    # Heuristic 4: Auditor Sentiment
    normalized_report = audit_report.lower()
    
    if "high confidence" in normalized_report or "high risk" in normalized_report or "fraud" in normalized_report:
        score -= 50
        breakdown.append("-50: Policy Auditor detected High Risk/Violation")
    elif "medium risk" in normalized_report:
        score -= 25
        breakdown.append("-25: Policy Auditor detected Medium Risk")
    elif "low risk" in normalized_report or "passed" in normalized_report:
        score += 0 # No penalty
    
    # Cap score
    score = max(0, min(100, score))
    
    return score, breakdown

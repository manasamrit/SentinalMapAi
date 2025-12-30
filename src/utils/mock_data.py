
SCENARIOS = {
    "suspicious_locksmith": {
        "name": "Ace 24/7 Locksmith",
        "address": "123 Residential Ave, Anytown, CA",
        "phone": "+1 555-019-9999",
        "website": "http://ace-lock-fast.com",
        "rating": 4.8,
        "reviews": [
            {"text": "Fastest service ever! arrived in 5 mins.", "rating": 5, "author_name": "John Doe", "time": 1709251200}, # March 1
            {"text": "Best locksmith in town.", "rating": 5, "author_name": "Jane Smith", "time": 1709254800}, # March 1 (1 hour later)
            {"text": "Amazing work 100% recommend", "rating": 5, "author_name": "Bob Lee", "time": 1709258400}, # March 1 (2 hours later)
            {"text": "Super fast", "rating": 5, "author_name": "Alice K", "time": 1709262000}, # March 1 (3 hours later)
            {"text": "They charged me double what they quoted.", "rating": 1, "author_name": "Angry Customer", "time": 1704067200} # Jan 1 (Older)
        ],
        "types": ["locksmith"],
        "osint_findings": {
            "search_results": [
                {"title": "Is 555-019-9999 a scam?", "snippet": "Reports of scam activity associated with this number."},
                {"title": "Residential Zoning Record", "snippet": "123 Residential Ave is a single family home."}
            ],
            "phone_risk": "High",
            "address_type": "Residential"
        }
    },
    "legit_coffee": {
        "name": "Daily Grind Coffee",
        "address": "456 Market St, Downtown, CA",
        "phone": "+1 555-020-0000",
        "website": "https://dailygrind.com",
        "rating": 4.5,
        "reviews": [
            {"text": "Great latte, slow wi-fi.", "rating": 4, "author_name": "Coffee Lover", "time": 1709000000},
            {"text": "Nice atmosphere.", "rating": 5, "author_name": "Remote Worker", "time": 1708000000},
            {"text": "Coffee was cold.", "rating": 2, "author_name": "Critic", "time": 1707000000}
        ],
        "types": ["cafe"],
        "osint_findings": {
            "search_results": [
                {"title": "Daily Grind Coffee - Yelp", "snippet": "4 stars. Good coffee."},
                {"title": "Downtown Business Assoc", "snippet": "Member: Daily Grind Coffee"}
            ],
            "phone_risk": "Low",
            "address_type": "Commercial"
        }
    }
}

POLICIES = """
Google Maps Trust & Safety Policy Guidelines (Threat Vectors):

1. **Lead-Gen Schemes / Ghost Businesses**:
   - Entities at residential addresses or virtual offices (Regus/WeWork) claiming to be 24/7 service centers are flagged.
   - Businesses with little to no external digital footprint (Yellow Pages, BBB, LinkedIn) are considered "High Risk".
   
2. **Review Manipulation (Fake Engagement)**:
   - "Review Bombing" or "Bot Farm" patterns (cluster of 5-star reviews in short timeframe).
   - "Review Boosting" via incentivized behavior.

3. **Misrepresentation**:
   - Keyword Stuffing in business name (e.g., "Best Locksmith Free Quote").
   - Phone numbers identified as VOIP/Burners without a verifiable human operator.
"""

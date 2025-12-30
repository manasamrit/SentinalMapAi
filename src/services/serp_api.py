from serpapi import GoogleSearch
from src.utils.mock_data import SCENARIOS

class SerpApiService:
    def __init__(self, api_key=None):
        self.api_key = api_key
        self.is_demo = not api_key

    def search_business_footprint(self, business_name, phone, address):
        """
        Searches for the business footprint.
        """
        if self.is_demo:
            # Simple heuristic to pick the right mock
            if "locksmith" in business_name.lower():
                return SCENARIOS["suspicious_locksmith"]["osint_findings"]["search_results"]
            else:
                return SCENARIOS["legit_coffee"]["osint_findings"]["search_results"]

        results = []
        try:
            # query 1: Name + Address
            params1 = {
                "q": f"{business_name} {address}",
                "api_key": self.api_key,
                "num": 3
            }
            search1 = GoogleSearch(params1)
            res1 = search1.get_dict()
            if 'organic_results' in res1:
                results.extend(res1['organic_results'])

            # query 2: Phone Number (Reverse Lookup style)
            params2 = {
                "q": f"\"{phone}\"", # exact match
                "api_key": self.api_key,
                "num": 3
            }
            search2 = GoogleSearch(params2)
            res2 = search2.get_dict()
            if 'organic_results' in res2:
                results.extend(res2['organic_results'])

            # Normalize output
            cleaned_results = []
            seen_links = set()
            for r in results:
                if r.get('link') not in seen_links:
                    cleaned_results.append({
                        "title": r.get('title'),
                        "link": r.get('link'),
                        "snippet": r.get('snippet', '')
                    })
                    seen_links.add(r.get('link'))
            
            return cleaned_results[:5] # Limit to 5 top relevant signals

        except Exception as e:
            print(f"SerpApi Error: {e}")
            return [{"title": "Error fetching real-time data", "snippet": "Using fallback data due to API error."}]

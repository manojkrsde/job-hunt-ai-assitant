import requests
from utils.config import USAJOBS_API_KEY

def fetch_usajobs(keyword, location="remote", results_per_page=5):
    """
    Fetches job results from the USAJobs API based on keyword and location.
    
    Args:
        keyword (str): Job search term.
        location (str): Job location (default "remote").
        results_per_page (int): Number of results to return (default 5).
        
    Returns:
        list: A list of job items from the API response.
    """
    url = "https://data.usajobs.gov/api/search"
    
    headers = {
        "Host": "data.usajobs.gov",
        "User-Agent": "sapnag255@gmail.com",
        "Authorization-Key": USAJOBS_API_KEY
    }
    
    params = {
        "Keyword": keyword,
        "LocationName": location,
        "ResultsPerPage": results_per_page
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            json_data = response.json()
            # The API returns a 'SearchResult' object which contains 'SearchResultItems'
            return json_data.get("SearchResult", {}).get("SearchResultItems", [])
        else:
            # Return empty list on failure or log error if needed
            print(f"Error: {response.status_code} - {response.text}")
            return []
            
    except Exception as e:
        print(f"Exception occurred: {e}")
        return []

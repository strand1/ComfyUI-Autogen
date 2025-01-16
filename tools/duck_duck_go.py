from duckduckgo_search import DDGS

# Define the tool name
tool_name = "duck_duck_go"

# Define the execute function
def execute(query: str, region: str = 'en-us', safesearch: str = 'off', max_results: int = 5):
    """
    Performs a DuckDuckGo search using the duckduckgo-search library.
    Args:
        query (str): The search query.
        result_limit (int): Maximum number of results to return (default is 5).
    Returns:
        dict: A dictionary containing search results (title, URL, and snippet).
    """
    try:
        ddg = DDGS()
        # Perform the search using duckduckgo-search
        results = ddg.text(keywords=query, region=region, safesearch=safesearch, max_results=max_results)

        if not results:
            return {"results": [], "message": "No results found."}

        # Format the results
        formatted_results = [
            {"title": result.get("title"), "url": result.get("href"), "snippet": result.get("body")}
            for result in results
        ]

        return {"results": formatted_results}

    except Exception as e:
        return {"error": f"Error occurred while searching: {e}"}

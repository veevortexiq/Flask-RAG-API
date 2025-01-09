import json


def initalquery(user_query, retrieval_chain):
    print("Initial querying started",user_query)
    all_tools = [
    "Image Optimiser", "Category Data Optimiser", "Product Data Optimiser",
    "Brand Guide Optimiser", "SEO Performace Reporter", "Schema Validator",
    "Keyword Analyser"
]
    # Convert all tool names to lowercase for case-insensitive matching
    all_tools_lower = [tool.lower() for tool in all_tools]
    # Step 1: Call the retrieval chain to get a response
    try:
        response = retrieval_chain({"question": user_query, "chat_history": []})
        docs = response['source_documents']
    except Exception as e:
        return f"Error during retrieval chain execution: {str(e)}"
    
    # Step 2: Ensure the LLM's response contains an answer key
    if "answer" not in response:
        return "no matching tool found"
    
    # Step 3: Parse the LLM's response (assuming it's in JSON format)
    try:
        llm_response = json.loads(response["answer"])
    except json.JSONDecodeError:
        return "no matching tool found"

    # Step 4: Validate the parsed response
    # Check if response is None or not a dictionary
    if not llm_response or not isinstance(llm_response, dict):
        return "no matching tool found"

    # Extract 'tool_name' and 'req_param' from the response
    tool_name = str(llm_response.get("tool_name", "")).lower()
    req_param = llm_response.get("req_param")

    # Validate 'tool_name' and 'req_param'
    if not tool_name or not req_param:
        return "no matching tool found"

    # Check if 'tool_name' matches any known tools (case-insensitive)
    if tool_name not in all_tools_lower:
        return "no matching tool found"

    # If all checks pass, return the validated response
    
    return [llm_response,docs]
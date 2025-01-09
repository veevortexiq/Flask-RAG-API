import json 

def cleanresponse(user_message):
    # Remove new lines and slashes from the JSON string
    result = user_message.replace("\n", "").replace("\\", "")
    
    try:
        # Parse the JSON string
        parsed_json = json.loads(result)
        
        # Extract and validate required fields
        cleaned_response = {
            "tool_name": parsed_json.get("tool_name"),
            "req_param": parsed_json.get("req_param"),
            "agent_id": parsed_json.get("agent_id"),
            "endpoint": parsed_json.get("endpoint")
        }
        
        # Check if any value is None/null
        if any(value is None for value in cleaned_response.values()):
            return "no tool found"
            
        return cleaned_response
        
    except Exception:
        return "no tool found"
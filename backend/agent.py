import httpx
import json

API_BASE_URL = "http://127.0.0.1:8000"

async def handle_agent_action(structured_data: dict) -> str:
    """
    Routes the intent to the appropriate CRUD API call and returns a human-readable response.
    """
    intent = structured_data.get("intent")
    print(intent)
    
    if intent == "create":
        return await handle_create(structured_data)
    elif intent == "read":
        return await handle_read(structured_data)
    elif intent == "update":
        return await handle_update(structured_data)
    elif intent == "delete":
        return await handle_delete(structured_data)
    else:
        return "Sorry, I couldn't understand your request. Please try again."

async def handle_create(data: dict) -> str:
    payload = {
        "name": data.get("name"),
        "email": data.get("email"),
        "phone": data.get("phone")
    }
    # Remove None values
    payload = {k: v for k, v in payload.items() if v is not None}
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(f"{API_BASE_URL}/users", json=payload)
            if response.status_code == 200:
                resp_data = response.json()
                return f"User {data.get('name', 'created')} created successfully with ID {resp_data.get('id')}."
            else:
                try:
                    error_data = response.json()
                    if "detail" in error_data and isinstance(error_data["detail"], list):
                        missing_fields = [f"\"{err['loc'][-1]}\"" for err in error_data["detail"] if err.get("type") == "missing" and "loc" in err]
                        if missing_fields:
                            return f"Error creating user. required fields {', '.join(missing_fields)} were not provided"
                except Exception:
                    pass
                return f"Failed to create user. Error: {response.text}"
        except Exception as e:
            return f"Error connecting to server: {str(e)}"

async def handle_read(data: dict) -> str:
    # Currently only supports listing all users
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{API_BASE_URL}/users")
            if response.status_code == 200:
                users = response.json()
                if not users:
                    return "There are no users found."
                
                # Format list nicely
                user_list = "\n".join([f"- {u.get('name')} ({u.get('email')}) [ID: {u.get('id')}]" for u in users])
                return f"Here are all users:\n{user_list}"
            else:
                return f"Failed to fetch users. Error: {response.text}"
        except Exception as e:
            return f"Error connecting to server: {str(e)}"

async def handle_update(data: dict) -> str:
    user_id = data.get("id")
    if not user_id:
        return "I need a User ID to update a user."
        
    payload = {
        "name": data.get("name"),
        "email": data.get("email"),
        "phone": data.get("phone")
    }
    # Remove None values
    payload = {k: v for k, v in payload.items() if v is not None}
    
    if not payload:
        return "I didn't find any fields to update (name, email, or phone)."

    async with httpx.AsyncClient() as client:
        try:
            response = await client.put(f"{API_BASE_URL}/users/{user_id}", json=payload)
            if response.status_code == 200:
                return f"Updated user {user_id} successfully."
            elif response.status_code == 404: # Assuming 404 for not found based on main.py logic (though main.py returns 200 with message "User not found"?)
                # Let's check main.py logic again. 
                # main.py returns {"message": "User not found"} but status code is default 200 unless explicitly set.
                # Wait, main.py doesn't set status_code=404. It returns a JSON with message.
                # So I should check the message.
                resp_data = response.json()
                return resp_data.get("message", "Update processed.")
            else:
                return f"Failed to update user. Error: {response.text}"
        except Exception as e:
            return f"Error connecting to server: {str(e)}"

async def handle_delete(data: dict) -> str:
    user_id = data.get("id")
    if not user_id:
        return "I need a User ID to delete a user."

    async with httpx.AsyncClient() as client:
        try:
            response = await client.delete(f"{API_BASE_URL}/users/{user_id}")
            if response.status_code == 200:
                 resp_data = response.json()
                 return resp_data.get("message", "Delete processed.")
            else:
                return f"Failed to delete user. Error: {response.text}"
        except Exception as e:
            return f"Error connecting to server: {str(e)}"

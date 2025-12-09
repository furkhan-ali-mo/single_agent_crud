import requests
import time
import sys

API_URL = "http://127.0.0.1:8000/agent/chat"

def test_chat(message):
    print(f"User: {message}")
    try:
        response = requests.post(API_URL, json={"message": message, "history": []})
        if response.status_code == 200:
            print(f"Agent: {response.json().get('response')}")
            return True
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"Connection Error: {e}")
        return False

def main():
    # Wait for server to start
    print("Waiting for server to be ready...")
    for _ in range(10):
        try:
            requests.get("http://127.0.0.1:8000/docs")
            print("Server is ready.")
            break
        except:
            time.sleep(1)
    else:
        print("Server failed to start.")
        sys.exit(1)

    print("\n--- Testing Create ---")
    test_chat("Create a user named TestAgent with email test@agent.com and phone 555-0199")

    print("\n--- Testing Read ---")
    test_chat("Show me all users")

    # We need to find the ID of the created user to test update/delete
    # But the agent response for create includes the ID.
    # For simplicity, we'll just test the intent routing for now.
    
    print("\n--- Testing Update (Mock ID) ---")
    test_chat("Update user with ID 1234567890abcdef12345678 to have name UpdatedAgent")

    print("\n--- Testing Delete (Mock ID) ---")
    test_chat("Delete user with ID 1234567890abcdef12345678")

if __name__ == "__main__":
    main()

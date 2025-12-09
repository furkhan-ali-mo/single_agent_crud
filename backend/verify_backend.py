import httpx
import sys

BASE_URL = "http://127.0.0.1:8000"

def test_backend():
    print("Testing Backend API...")
    
    # 1. Create User
    user_data = {"name": "Test User", "email": "test@example.com", "phone": "1234567890"}
    try:
        resp = httpx.post(f"{BASE_URL}/users", json=user_data)
        if resp.status_code != 200:
            print(f"Failed to create user: {resp.text}")
            return
        user_id = resp.json().get("id")
        print(f"Created user with ID: {user_id}")
    except Exception as e:
        print(f"Error creating user: {e}")
        return

    # 2. Update User
    update_data = {"name": "Updated User", "email": "updated@example.com"}
    try:
        resp = httpx.put(f"{BASE_URL}/users/{user_id}", json=update_data)
        if resp.status_code != 200:
            print(f"Failed to update user: {resp.text}")
            return
        print("Updated user successfully")
    except Exception as e:
        print(f"Error updating user: {e}")
        return

    # 3. Verify Update
    try:
        resp = httpx.get(f"{BASE_URL}/users")
        users = resp.json()
        found = False
        for user in users:
            if user["id"] == user_id:
                if user["name"] == "Updated User" and user["email"] == "updated@example.com":
                    print("Verification successful: User data matches updates")
                    found = True
                else:
                    print(f"Verification failed: Data mismatch. Got {user}")
                break
        if not found:
            print("Verification failed: User not found in list")
    except Exception as e:
        print(f"Error fetching users: {e}")
        return

    # 4. Delete User
    try:
        resp = httpx.delete(f"{BASE_URL}/users/{user_id}")
        if resp.status_code != 200:
            print(f"Failed to delete user: {resp.text}")
        else:
            print("Deleted user successfully")
    except Exception as e:
        print(f"Error deleting user: {e}")

if __name__ == "__main__":
    test_backend()

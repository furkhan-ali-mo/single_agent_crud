print("🔥 RUNNING 2nd GRADIO APP FROM THIS FILE")

import gradio as gr
import httpx
import pandas as pd

BACKEND_URL = "http://127.0.0.1:8000"

def fetch_users():
    try:
        response = httpx.get(f"{BACKEND_URL}/users")
        users = response.json()
    except Exception as e:
        print(f"Error fetching users: {e}")
        return [], []

    data = []
    for idx, user in enumerate(users, 1):
        data.append([
            idx, 
            user.get("name"), 
            user.get("phone"), 
            user.get("email"),
            "🗑️"  # Delete icon
        ])
    return data, users

def handle_select(evt: gr.SelectData, users_list):
    if not evt.index:
        return gr.update(), users_list
        
    row_index, col_index = evt.index
    
    # Column 4 is Delete (0-indexed: S.No, Name, Phone, Email, Delete)
    
    if col_index == 4: # Delete
        if row_index < len(users_list):
            user_id = users_list[row_index].get("id")
            if user_id:
                try:
                    response = httpx.delete(f"{BACKEND_URL}/users/{user_id}")
                    if response.status_code == 200:
                        gr.Info("User deleted successfully!")
                    else:
                        gr.Warning(f"Failed to delete user: {response.text}")
                except Exception as e:
                    gr.Warning(f"Error deleting user: {e}")
                
                # Refresh table
                data, users = fetch_users()
                return data, users
            
    return gr.update(), users_list

def handle_change(new_data: pd.DataFrame, users_list):
    # new_data is a pandas DataFrame because Gradio Dataframe outputs DataFrame by default for 'change' event 
    # unless type is specified. But wait, we initialized with list of lists. 
    # Let's force type='pandas' in the event listener or handle it. 
    # Actually, let's convert new_data to list of lists for easier comparison if it's a DataFrame.
    
    if isinstance(new_data, pd.DataFrame):
        new_values = new_data.values.tolist()
    else:
        new_values = new_data

    # Check if lengths match
    if len(new_values) != len(users_list):
        # This might happen during delete or load, just sync state if needed or ignore
        return users_list, gr.update()

    changes_made = False
    revert_needed = False
    
    for i, row in enumerate(new_values):
        if i >= len(users_list):
            break
            
        user = users_list[i]
        
        # Current values in table
        # 0: S.No (Read-only)
        # 1: Name
        # 2: Phone
        # 3: Email
        # 4: Delete (Read-only)
        
        current_sno = row[0]
        current_name = row[1]
        current_phone = row[2]
        current_email = row[3]
        current_delete = row[4]
        
        # Original values
        original_sno = i + 1
        original_name = user.get("name")
        original_phone = user.get("phone")
        original_email = user.get("email")
        original_delete = "🗑️"
        
        # Check for changes
        updates = {}
        
        if str(current_name) != str(original_name):
            updates["name"] = current_name
        if str(current_phone) != str(original_phone):
            updates["phone"] = current_phone
        if str(current_email) != str(original_email):
            updates["email"] = current_email
            
        # Check for read-only violations
        if str(current_sno) != str(original_sno) or str(current_delete) != str(original_delete):
            revert_needed = True
            # We will return the original data to the table to revert changes
            
        if updates:
            user_id = user.get("id")
            try:
                response = httpx.put(f"{BACKEND_URL}/users/{user_id}", json=updates)
                if response.status_code == 200:
                    gr.Info(f"Updated user {original_name}")
                    # Update local state
                    users_list[i].update(updates)
                    changes_made = True
                else:
                    gr.Warning(f"Failed to update: {response.text}")
                    revert_needed = True
            except Exception as e:
                gr.Warning(f"Error updating: {e}")
                revert_needed = True

    if revert_needed:
        # Reconstruct table data from users_list to revert invalid changes
        reverted_data = []
        for idx, user in enumerate(users_list, 1):
            reverted_data.append([
                idx, 
                user.get("name"), 
                user.get("phone"), 
                user.get("email"),
                "🗑️"
            ])
        return users_list, reverted_data
        
    return users_list, gr.update()

with gr.Blocks() as demo:
    gr.Markdown("## All Users")
    
    # State to store raw user data (including IDs)
    users_state = gr.State([])
    
    refresh_btn = gr.Button("Refresh")
    
    table = gr.Dataframe(
        headers=["S.No", "User Name", "User Phone", "User Email", "Delete"],
        datatype=["number", "str", "str", "str", "str"],
        interactive=True,
        col_count=(5, "fixed")
    )
    
    # Load data on start
    demo.load(fetch_users, outputs=[table, users_state])
    
    # Refresh button action
    refresh_btn.click(fetch_users, outputs=[table, users_state])
    
    # Handle table clicks (Delete action)
    table.select(
        handle_select, 
        inputs=[users_state], 
        outputs=[table, users_state]
    )
    
    # Handle table edits
    table.change(
        handle_change,
        inputs=[table, users_state],
        outputs=[users_state, table]
    )

if __name__ == "__main__":
    demo.launch()

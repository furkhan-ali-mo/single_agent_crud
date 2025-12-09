from fastapi import FastAPI
from mongo_db import users_collection
from data_schema import UserCreate
from bson import ObjectId

import sys
import os
import gradio as gr

# Add the parent directory to sys.path to allow importing from frontend
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from frontend.app import demo as create_demo
from frontend.view_users import demo as view_demo
from backend.agent_router import agent_router
from frontend.agent_chat import agent_chat

app = FastAPI()
app.include_router(agent_router, prefix="/agent")

# @app.get("/")
# def root():
#     return {"Hello": "World"}

@app.post("/users")
def create_user(user: UserCreate):
    # Convert Pydantic model → dict
    user_data = user.dict()

    # Insert into MongoDB
    result = users_collection.insert_one(user_data)
    print("lalila:",result)

    # Return success with inserted ID
    return {
        "message": "User created successfully",
        "id": str(result.inserted_id),

    }

@app.get("/users")
def get_users():
    users = []
    for user in users_collection.find():
        users.append({
            "id": str(user["_id"]),
            "name": user.get("name"),
            "email": user.get("email"),
            "phone": user.get("phone")
        })
    return users

@app.delete("/users/{user_id}")
def delete_user(user_id: str):
    # Convert string ID to ObjectId
    try:
        oid = ObjectId(user_id)
    except Exception:
        return {"error": "Invalid ID format"}

    result = users_collection.delete_one({"_id": oid})
    print(result)
    
    if result.deleted_count == 1:
        return {"message": "User deleted successfully"}
    else:
        return {"message": "User not found"}

@app.put("/users/{user_id}")
def update_user(user_id: str, user_update: dict):
    try:
        oid = ObjectId(user_id)
    except Exception:
        return {"error": "Invalid ID format"}

    # Filter out empty fields if necessary, or update all provided
    update_data = {k: v for k, v in user_update.items() if v is not None}
    
    if not update_data:
         return {"message": "No data to update"}

    result = users_collection.update_one({"_id": oid}, {"$set": update_data})
    
    if result.matched_count == 1:
        return {"message": "User updated successfully"}
    else:
        return {"message": "User not found"}

# Mount the Gradio apps
# Mount specific paths first!
app1 = gr.mount_gradio_app(app, view_demo, path="/view-users")
app2 = gr.mount_gradio_app(app, create_demo, path="/lola")
app3 = gr.mount_gradio_app(app, agent_chat, path="/agent-chat")
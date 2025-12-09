import gradio as gr
import requests

API_URL = "http://127.0.0.1:8000/agent/chat"

def chat_function(message, history):
    """
    Sends the user message to the backend agent endpoint and returns the response.
    """
    try:
        payload = {"message": message, "history": []} # History management can be improved if backend supports it
        response = requests.post(API_URL, json=payload)
        
        if response.status_code == 200:
            return response.json().get("response", "No response from agent.")
        else:
            return f"Error: {response.text}"
    except Exception as e:
        return f"Connection Error: {str(e)}"

# Create the Gradio Chat Interface
agent_chat = gr.ChatInterface(
    fn=chat_function,
    title="Agentic CRUD Chat",
    description="Ask me to create, read, update, or delete users!",
    examples=["Create a user named Alice", "Show me all users", "Delete user with ID ..."],
    type="messages" 
)

if __name__ == "__main__":
    agent_chat.launch()

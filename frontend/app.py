print("🔥 RUNNING GRADIO FROM THIS FILE")

import gradio as gr
import httpx

BACKEND_URL = "http://127.0.0.1:8000"

def submit_user(name, email, phone):
    print("Submitting:", name, email, phone)
    payload = {
        "name": name,
        "email": email,
        "phone": phone
    }
    print(payload)

    response = httpx.post(f"{BACKEND_URL}/users", json=payload)
    return response.json()

def debug_test(*args):
    print("CLICK TRIGGERED")
    print("ARGS:", args)
    return "nano banana"

with gr.Blocks() as demo:
    gr.Markdown("## Create User")

    name_input = gr.Textbox(label="Name")
    email_input = gr.Textbox(label="Email")
    phone_input = gr.Textbox(label="Phonozzz")

    submit_btn = gr.Button("Submit")
    #output = gr.JSON(label="Response")
    output = gr.Textbox(label="Output")

    submit_btn.click(
        fn = submit_user,
        inputs=[name_input, email_input, phone_input],
        outputs=output
    )

    gr.Button("View all users", link="/view-users")

if __name__ == "__main__":
    demo.launch()

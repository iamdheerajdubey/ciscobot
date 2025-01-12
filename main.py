import requests
import streamlit as st
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configuration
BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = "5102d4f7-9cf1-4ceb-a5d1-3c780875ac55"
FLOW_ID = "9821b5ed-46fc-478d-802e-32db1ec2b641"
APPLICATION_TOKEN = os.environ.get("APP_TOKEN")
ENDPOINT = "CISCOBOT"

# Add page configuration
st.set_page_config(page_title="Cisco Chat Assistant", page_icon="🤖")

def run_flow(message: str) -> dict:
    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{ENDPOINT}"
    
    payload = {
        "input_value": message,
        "output_type": "chat",
        "input_type": "chat",
    }
    
    headers = {"Authorization": "Bearer " + APPLICATION_TOKEN, "Content-Type": "application/json"}
    try:
        response = requests.post(api_url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise Exception(f"API call failed: {str(e)}")

def main():
    # Sidebar content
    with st.sidebar:
        st.title("About Me")
        
        st.markdown("""
        👋 **Hi, I'm your Cisco Command Assistant!**
        
        🛠️ **I can help you with:**
        * Cisco IOS commands
        * Network configurations
        * Troubleshooting steps
        * Best practices
        
        👨‍💻 **Created By:** DD
        
        📫 **Get in touch:**  
        [📧 Email](mailto:iamdheerajdubey@gmail.com)  
        [💼 LinkedIn](https://www.linkedin.com/in/dheerajhere/)  
        [🐛 Report a Bug](mailto:iamdheerajdubey@gmail.com)
        """)
        
        if st.button("Clear Chat"):
            st.session_state.messages = []
            st.rerun()  # Changed from experimental_rerun() to rerun()

    # Main content
    st.title("🤖 Cisco Command Assistant")
    st.write("Ask me about Cisco commands and configurations!")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("What would you like to know?"):
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        try:
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = run_flow(prompt)
                    answer = response["outputs"][0]["outputs"][0]["results"]["message"]["text"]
                    st.markdown(answer)
                    
                    # Add assistant response to chat history
                    st.session_state.messages.append({"role": "assistant", "content": answer})
        except Exception as e:
            st.error(f"Error: {str(e)}")

if __name__ == "__main__":
    main()

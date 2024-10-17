import streamlit as st  
import requests  

def main():  
    st.title("Azure OpenAI GPT-4o Chat Interface")  

    # Azure OpenAI connection details  
    azure_openai_key = "22ec84421ec24230a3638d1b51e3a7dc"  # Your actual API key  
    azure_openai_endpoint = "https://internshala.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2024-08-01-preview"  # Your actual endpoint URL  

    # User input for the chat message  
    user_input = st.text_input("Enter your message:", "")  

    # Button to send the message to the API  
    if st.button("Send"):  
        if user_input:  
            try:  
                headers = {  
                    "Content-Type": "application/json",  
                    "api-key": azure_openai_key  # The API key for authentication  
                }  
                
                data = {  
                    "messages": [{"role": "user", "content": user_input}],  
                    "max_tokens": 50  # Limit the response length  
                }  
                
                # Making the POST request to the Azure OpenAI endpoint  
                response = requests.post(azure_openai_endpoint, headers=headers, json=data)  
                
                # Check if the request was successful  
                if response.status_code == 200:  
                    result = response.json()  # Parse the JSON response  
                    st.success(result["choices"][0]["message"]["content"].strip())  # Display the response content from the AI  
                else:  
                    # Handle errors if the request was not successful  
                    st.error(f"Failed to connect or retrieve response: {response.status_code} - {response.text}")  
            except Exception as e:  
                # Handle any exceptions that occur during the request  
                st.error(f"Failed to connect or retrieve response: {str(e)}")  
        else:  
            # Warn the user if the input is empty  
            st.warning("Please enter a message.")  

if __name__ == "__main__":  
    main()

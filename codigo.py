#Step 2: Import Ollama and Streamlit.
import streamlit as st
import ollama

#Step 3: Initialize the model in Python.
# initialize model
if "model" not in st.session_state:
    st.session_state.model = "llama3"

#Step 4: Set the Title.
st.title("Local Llama3 Chatbot!🤖")

#Step 5: Initialize Messages.
if "messages" not in st.session_state:
  st.session_state.messages = []

#Step 6: Display Existing Chat History
for message in st.session_state.messages:     
  with st.chat_message(message["role"]):  
    st.markdown(message["content"])

#Step 7: Create the User Input Field.
if user_prompt := st.chat_input("Your prompt"):
  st.session_state.messages.append({"role": "user", "content":user_prompt})
  with st.chat_message("user"):
    st.markdown(user_prompt)


#Step 8: Generate and Display Llama’s Response.
with st.chat_message("assistant"):
    message_placeholder = st.empty()
    full_response = ""

    for chunk in ollama.chat(
        model=st.session_state.model,
        messages=[
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ],
        stream=True,
    ):
        token = chunk["message"]["content"]
        if token is not None:
            full_response += token
            message_placeholder.markdown(full_response + "▌")

    message_placeholder.markdown(full_response)

#Step 9: Update Chat History.
st.session_state.messages.append({"role": "assistant", "content": full_response})
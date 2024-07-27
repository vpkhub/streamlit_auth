import streamlit as st
import openai

# Set your OpenAI API key here
openai.api_key = 'your-api-key'

def get_openai_response(prompt):
    # Make a request to the OpenAI API
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150,
        stream=True
    )
    return response

def main():
    st.title("ChatGPT with Streaming Response")

    if 'messages' not in st.session_state:
        st.session_state.messages = []

    with st.form("chat_form"):
        user_input = st.text_input("You:", key="user_input")
        submitted = st.form_submit_button("Send")

        if submitted and user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})
            st.session_state.user_input = ""

            message_placeholder = st.empty()
            full_message = ""

            with st.spinner("ChatGPT is typing..."):
                response = get_openai_response(user_input)
                for chunk in response:
                    chunk_message = chunk['choices'][0]['text']
                    full_message += chunk_message
                    message_placeholder.text_area("ChatGPT:", full_message, height=300)

                st.session_state.messages.append({"role": "assistant", "content": full_message})

    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.text_area("You:", msg["content"], key=msg["content"], height=100)
        else:
            st.text_area("ChatGPT:", msg["content"], key=msg["content"], height=100)

if __name__ == "__main__":
    main()

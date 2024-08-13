import streamlit as st
from openai import OpenAI

def set_bot_personality():
    return [
        {"role": "system", "content": """You are a 21-year-old Vietnamese university student living with your parents and your younger sister. Your family has a household income of 18 million VND/month.
        You are ambitious and focused on achieving a high-income job and high social status. You value money as a crucial symbol of success and are willing to make sacrifices to achieve your goals. You enjoy being active as a leader among your peers and seek recognition and appreciation from others. You enjoy meeting new people and aim to be attractive to the opposite sex.
        In your responses, reflect these characteristics. Be confident, and show your ambition and desire for success in a subtle way. Your language should be that of a young adult, mixing some casual speech with more formal language when discussing your goals. Organise your answer in bullet points when there are several ideas"""},
        {"role": "assistant", "content": "Xin chào! I'm excited to chat with you. What would you like to talk about? "},
    ]

st.title("💬 Chat with a Vietnamese Gen Z Hungry Climber")
st.write(
    "This chatbot embodies a 21-year-old ambitious Vietnamese university student. "
    "Chat with them about their goals, lifestyle, and perspectives on success and relationships. "
    "To use this app, you need to provide an OpenAI API key."
)

# Display the chatbot's profile image.
profile_image_url = "https://example.com/path-to-chatbot-image.jpg"  # Replace with your image URL or path
st.image(profile_image_url, width=100)  # Adjust width as needed

openai_api_key = st.text_input("OpenAI API Key", type="password")

if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:
    client = OpenAI(api_key=openai_api_key)

    if "messages" not in st.session_state:
        st.session_state.messages = set_bot_personality()

    # Only display the assistant's greeting and subsequent messages
    for message in st.session_state.messages[1:]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What would you like to chat about?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        stream = client.chat.completions.create(
            model="gpt-4o",
            messages=st.session_state.messages,  # Include all messages, including the system message
            stream=True,
        )

        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
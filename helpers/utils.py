import streamlit as st


def get_sidebar():
    with st.sidebar:
        openai_api_key = st.text_input(
            "OpenAI API Key",
            value=st.session_state.get("openai_api_key", ""),
            key="chatbot_api_key",
            type="password",
        )
        st.session_state["openai_api_key"] = openai_api_key

        st.markdown(
            "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
        )

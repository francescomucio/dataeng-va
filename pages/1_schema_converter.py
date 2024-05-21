import streamlit as st

from streamlit.logger import get_logger
from helpers.schema_converter import OpenAISchemaConverter
from helpers.utils import get_sidebar

LOGGER = get_logger(__name__)


actions_list = [
    {
        "action": "avro_to_json",
        "text": "Convert an Avro schema to JSON Schema",
        "source_schema_type": "JSON",
    },
    {
        "action": "json_to_avro",
        "text": "Convert an JSON schema to Avro Schema",
        "source_schema_type": "Avro",
    },
    {
        "action": "sample_data",
        "text": "Generate sample data for the following schema",
        "source_schema_type": "JSON or Avro",
    },
]
action_map = {item["text"]: item["action"] for item in actions_list}
schema_type_map = {item["text"]: item["source_schema_type"] for item in actions_list}

actions = [a["text"] for a in actions_list]


def get_openapi():
    openai_api_key = st.session_state.get("openai_api_key", "")

    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()
    else:
        api = OpenAISchemaConverter(openai_api_key=openai_api_key)
    return api


def setup_page():
    # Page Setup
    global openai_api_key
    st.set_page_config(
        page_title="Hello",
        page_icon="👋",
    )

    st.title("Schemas and events utilities")
    st.caption("I found no icon for a data flow so here are some flow...ers 💐🌷🌹🌸🌺")

    get_sidebar()


def setup_form():
    global selected_action
    global source_schema

    selected_action = st.selectbox(
        "How can I help you?",
        options=actions,
        index=None,
        placeholder="-- select an option --",
    )

    action = action_map.get(selected_action)
    st.write("You selected:", action)

    source_schema = st.text_area(
        f"Your {schema_type_map.get(selected_action, 'To Be Selected')} schema:",
        height=700,
    )


def schema_converter():
    setup_page()
    setup_form()

    go_button = st.button("Go!")

    if go_button:
        api = get_openapi()

        if action_map[selected_action] == "avro_to_json":
            api_response = api.avro_to_json(source_schema)
        elif action_map[selected_action] == "json_to_avro":
            api_response = api.json_to_avro(source_schema)
        elif action_map[selected_action] == "sample_data":
            api_response = api.sample_data(source_schema)
        st.markdown(
            body=f"""
                    ```json
                    {api_response}
                    """
        )


schema_converter()

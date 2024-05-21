import streamlit as st

from streamlit.logger import get_logger
from helpers.dbt_api import OpenAIdbt
from helpers.utils import get_sidebar

LOGGER = get_logger(__name__)


actions_list = [
    {"action": "schema", "text": "Make a schema.yaml file for a dbt model"},
    {"action": "tests", "text": "Write some tests for a dbt model"},
    {"action": "incremental", "text": "Convert a dbt model to an incremental one"},
]

action_map = {item["text"]: item["action"] for item in actions_list}

actions = [a["text"] for a in actions_list]


def get_openapi():
    openai_api_key = st.session_state.get("openai_api_key", "")

    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()
    else:
        api = OpenAIdbt(openai_api_key=openai_api_key)
    return api


def setup_page():
    # Page Setup
    global openai_api_key
    st.set_page_config(
        page_title="Hello",
        page_icon="👋",
    )

    st.title("Let's do something cool with dbt 🥞")
    st.caption("Those are stacked pancakes, there was no emoji for a database 😅")

    get_sidebar()


def setup_form():
    global selected_action
    global with_tests
    global dbt_model_name
    global dbt_model
    global model_info
    global unique_key
    global incremental_strategy
    global time_condition

    selected_action = st.selectbox(
        "How can I help you?",
        options=actions,
        index=None,
        placeholder="-- select an option --",
    )

    action = action_map.get(selected_action)
    st.write("You selected:", action)

    # Advanced info
    with st.expander("Avanced settings"):
        if action == "schema":
            with_tests = st.checkbox(
                "Generate tests",
                value=False,
            )

        if action == "incremental":
            incremental_strategy = st.selectbox(
                "Select the incremental strategy",
                ("merge", "upsert", "magic"),
            )

            unique_key = st.text_input(
                "Unique/merge key for this model (comma separated please)",
            ).split(",")

            time_condition = st.text_input(
                "Your time condition  (you can use dbt macros)",
            )

        model_info = st.text_area("Additional info about your model:")

    dbt_model_name = st.text_input("Name of your dbt model:")
    dbt_model = st.text_area("Your dbt model:", height=700)


def dbt():
    setup_page()
    setup_form()

    # Every form must have a submit button.
    go_button = st.button("Go!")

    if go_button:
        api = get_openapi()

        api_response = "e"
        if action_map[selected_action] == "schema":
            api_response = api.generate_schema_yaml(
                dbt_model_name=dbt_model_name,
                dbt_model=dbt_model,
                with_tests=with_tests,
                model_info=model_info,
            )
            language = "yaml"
        elif action_map[selected_action] == "tests":
            api_response = api.generate_tests(
                dbt_model_name=dbt_model_name,
                dbt_model=dbt_model,
                model_info=model_info,
            )
            language = "yaml"
        else:
            api_response = api.generate_incremental(
                dbt_model_name=dbt_model_name,
                dbt_model=dbt_model,
                model_info=model_info,
                unique_key=unique_key,
                incremental_strategy=incremental_strategy,
                time_condition=time_condition,
            )
            language = "sql"

        st.markdown(
            body=f"""
                    ```{language}
                    {api_response}
                  """
        )


dbt()

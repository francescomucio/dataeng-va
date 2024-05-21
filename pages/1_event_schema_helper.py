import streamlit as st

from streamlit.logger import get_logger
from helpers.dbt_api import OpenAIdbt
from helpers.utils import get_sidebar

LOGGER = get_logger(__name__)


def setup_page():
    # Page Setup
    global openai_api_key
    st.set_page_config(
        page_title="Hello",
        page_icon="👋",
    )

    st.title("Events and schemas 🔀")
    st.caption("Maybe instead of a forced icon for flow I could just go with a 🌷")

    get_sidebar()

def setup_form():
    pass


def dbt():
    setup_page()
    setup_form()
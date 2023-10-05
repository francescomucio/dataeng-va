import streamlit as st
import pandas as pd

from streamlit.logger import get_logger
from helpers.utils import get_sidebar

LOGGER = get_logger(__name__)

actions_list = [
    {"action": "null", "text": "-- select an option --"},
    {"action": "schema.yaml", "text": "Make a schema.yaml file for this dbt model"},
    {"action": "test", "text": "Write some tests for this dbt model"},
]
actions = pd.DataFrame(actions_list)
actions = actions[["text", "action"]]

# Page Setup
st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.title("Hey, I am your data engineer assistant 🥁")
st.caption("My name is David with a W. You can call me Wavid!🚀")

get_sidebar()

with open("README.md", "r") as file:
    # Read the entire file content into a string
    content = file.read()

st.markdown(content)

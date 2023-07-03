import streamlit as st
import dev.streamlit_functions as st_functions
from dev.st_explore_with_wordcloud import explore_data
import folium
from streamlit_folium import st_folium


import os
import json
import pandas as pd
import openai

from dev.langchain.chains_as_classes_with_json import OverpassQueryChain
from dev.prompts.naturalmaps_bot import ChatBot

api_key = os.getenv("OPENAI_KEY")

# This is just some random initialization data for the default image
data_str = '{"version": 0.6, "generator": "Overpass API 0.7.60.6 e2dc3e5b", "osm3s": {"timestamp_osm_base": "2023-06-29T15:35:14Z", "timestamp_areas_base": "2023-06-29T12:13:45Z", "copyright": "The data included in this document is from www.openstreetmap.org. The data is made available under ODbL."}, "elements": [{"type": "node", "id": 6835150496, "lat": 52.5226885, "lon": 13.3979877, "tags": {"leisure": "pitch", "sport": "table_tennis", "wheelchair": "yes"}}, {"type": "node", "id": 6835150497, "lat": 52.5227083, "lon": 13.3978939, "tags": {"leisure": "pitch", "sport": "table_tennis", "wheelchair": "yes"}}, {"type": "node", "id": 6835150598, "lat": 52.5229822, "lon": 13.3965893, "tags": {"access": "customers", "leisure": "pitch", "sport": "table_tennis"}}, {"type": "node", "id": 6835150599, "lat": 52.5229863, "lon": 13.3964894, "tags": {"access": "customers", "leisure": "pitch", "sport": "table_tennis"}}]}'
fg = st_functions.overpass_to_feature_group(data_str)
bounds = fg.get_bounds()

# Parameters for the default image
if "center" not in st.session_state:
    st.session_state.center = st_functions.calculate_center(bounds)
if "feature_group" not in st.session_state:
    st.session_state["feature_group"] = fg
if "zoom" not in st.session_state:
    st.session_state["zoom"] = st_functions.calculate_zoom_level(bounds)


# Set OpenAI API key from Streamlit secrets. Not really necessary, as it is done elsewhere
openai.api_key = api_key  # st.secrets["OPENAI_API_KEY"]

# In principle, we can have several models.
# I assume they all models have the attribute .overpass_answer
# with the last answer from overpass
# and the method .process_user_input(prompt).
# Currently this convention is not satisfied by the agent

# Model selection. Should be changed to something more elegant...
model_choice = st.radio(
    "Select model 👉",
    key="model",
    options=["Simple chain, gpt-3.5", "Agent, gpt-3.5"],
)
st.title("Natural Maps")

if model_choice == "Simple chain, gpt-3.5":
    model = OverpassQueryChain(api_key)
else:
    model = ChatBot(openai_api_key=api_key)

# Setting up the chat
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = model.process_user_input(prompt)
        st.markdown(response)
        st.markdown(model.overpass_answer)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
        # Here the image parameters get updated
        (
            st.session_state.feature_group,
            st.session_state.center,
            st.session_state.zoom,
        ) = st_functions.calculate_parameters_for_map(model.overpass_answer)


m = folium.Map(
    height="100%",
)
st_folium(
    m,
    feature_group_to_add=st.session_state.feature_group,
    center=st.session_state.center,
    zoom=st.session_state.zoom,
)

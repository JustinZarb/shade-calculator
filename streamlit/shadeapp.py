import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(
    page_title="Naturalmaps",
    page_icon=":world_map:️",
    layout="wide",
)

st.title("Natural Maps")
st.markdown(
    "A Portfolio project by J. Adam Hughes and Justin Zarb as part of Data Science Retreat. [Github Repo](https://github.com/JustinZarb/shade-calculator)"
)
left, right = st.columns(2)

with left:
    st.header("Natural language input")
    natural_input = st.text_area(
        "What would you like to know?",
    )
    st.markdown(
        """Open Street Map is awesome but hard to query. We are here to study what can
     be done and streamline the process of question -> query -> process -> output. 
     Here are some examples of how we imagine this to be used: 
     """
    )
    st.markdown(
        """
    | Persona         | Description | Spatial Query |
    |-----------------|-------------|---------------|
    | Urban Athlete   | Enjoys staying active and exploring the city in a dynamic way. | Find all the parks in Berlin that have a running path of at least 5km and are within 500m of a public swimming pool for a post-run dip. |
    | Hungry Partygoer | Enjoys the vibrant nightlife of the city and loves to eat late-night snacks. | Find all the late-night food spots that are within a 200m radius of nightclubs that are open until at least 3 AM. |
    | City Planner | Interested in understanding and improving the urban layout of the city. | Find all residential buildings in Berlin that are more than 50m high and are not within 500m of any public park or green space. |
    | Culture Seeker | Always looking to explore cultural heritage and history. | Find all the historic landmarks in Berlin that are within a 1km radius of an art gallery or museum. |
    | Freelance Writer | Always in search of quiet spots to sit, observe, and pen their thoughts. | Find all the quietest coffee shops (at least 200m away from any main road) in Berlin that open before 8 AM and are in close proximity to a library or a bookstore. |
    
    """
    )

    st.header("Generated query")
    st.markdown(
        """
        - #Todo: convert text input into an overpass prompt using a trained LLM
        - #Todo: display the generated prompt here, as in the example below
        """
    )
    st.info(
        """            
            [out:json][timeout:25];
            // gather results
            (
            // query part for: “fountain”
            node["amenity"="fountain"]({{bbox}});
            way["amenity"="fountain"]({{bbox}});
            relation["amenity"="fountain"]({{bbox}});
            );
            // print results
            out body;
            >;
            out skel qt;"""
    )

    st.header("Process query results")
    st.markdown("""Do something with the results""")


with right:
    st.header("Map display")
    st.markdown(
        """Using Folium to display the map itself, and streamlit_folium to return \
        some data from interactions with the map. """
    )
    center = {"lat": 52.49881139119491, "lng": 13.33718776702881}

    m = folium.Map(location=list(center.values()), zoom_start=16)
    st_data = st_folium(m, width=725)
    st_data

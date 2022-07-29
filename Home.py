import streamlit as st

st.set_page_config(
    page_title="Football xG Visualizer",

)

st.write("# Football xG Visualizer ⚽")

st.sidebar.success("Select a tool above.")

st.markdown(
    """
    This app visualizes player or team xG statistics. All data is from understat.com. Perform searches on players using their understat ID. Perform searches on teams using the dropdown list. 

    **👈 Select a tool from the sidebar** to get started!
    ### Features 
    - Player Visualizer
    - Player Comparison
    - Team Visualizer

"""
)
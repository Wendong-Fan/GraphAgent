import streamlit as st
import streamlit.components.v1 as components


st.markdown("# Knowledge Graph Visualization")
st.sidebar.markdown("# Knowledge Graph Visualization")

components.iframe("https://workspace-preview.neo4j.io/workspace/query?ntid=google-oauth2%7C103072183927948648663",height=1000,width=1000)
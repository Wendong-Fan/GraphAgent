import streamlit as st
from camel.types import ModelPlatformType, ModelType
from camel.models import ModelFactory
from camel.loaders import UnstructuredIO
from camel.configs import ChatGPTConfig
from camel.storages import Neo4jGraph
from agents import KnowledgeGraphAgent, InsightAgent
import streamlit.components.v1 as components

st.markdown("# 🐫 Knowledge Graph Agents")



# Initialize UnstructuredIO instance
uio = UnstructuredIO()

# Initial text_example value
text_example = """CAMEL is an open-source library designed for the study of autonomous and communicative agents. We believe that studying these agents on a large scale offers valuable insights into their behaviors, capabilities, and potential risks. To facilitate research in this field, we implement and support various types of agents, tasks, prompts, models, and simulated environments.
"""

# Sidebar for API Key input
openai_api_key = st.sidebar.text_input('OpenAI API Key', type='password') or st.secrets["OPENAI_KEY"]

url = st.sidebar.text_input('Neo4j URL', type='password') or st.secrets["URL"]
username = st.sidebar.text_input('Neo4j Username', type='password') or st.secrets["USERNAME"]
password = st.sidebar.text_input('Neo4j Password', type='password') or st.secrets["PASSWORD"]

# Set Neo4j instance
n4j = Neo4jGraph(
    url=url, username=username, password=password
)


# Initialize session state variables
if 'text_query' not in st.session_state:
    st.session_state.text_query = "Enter your question here"

if 'relationships_info_to_agent' not in st.session_state:
    st.session_state.relationships_info_to_agent = ""

if 'uploaded_file_path' not in st.session_state:
    st.session_state.uploaded_file_path = ""

if 'graph_elements' not in st.session_state:
    st.session_state.graph_elements = []

if 'iframe_rendered' not in st.session_state:
    st.session_state.iframe_rendered = False

if 'insight_agent' not in st.session_state:
    st.session_state.insight_agent = False

if openai_api_key:
    # Model setting
    model_4o = ModelFactory.create(
        model_platform=ModelPlatformType.OPENAI,
        model_type=ModelType.GPT_4O,
        model_config_dict=ChatGPTConfig().__dict__,
        api_key=openai_api_key
    )

    model_35 = ModelFactory.create(
        model_platform=ModelPlatformType.OPENAI,
        model_type=ModelType.GPT_3_5_TURBO,
        model_config_dict=ChatGPTConfig().__dict__,
        api_key=openai_api_key
    )

    # Agent setting
    kg_agent = KnowledgeGraphAgent(model=model_35)
    insight_agent = InsightAgent(model=model_4o)

# Form for user input
with st.form('my_form'):
    uploaded_file = st.file_uploader("Choose a PDF file", accept_multiple_files=False)
    submitted1 = st.form_submit_button('Submit File')

    if submitted1 and uploaded_file:
        st.session_state.uploaded_file_path = 'output.pdf'
        with open(st.session_state.uploaded_file_path, 'wb') as file:
            file.write(uploaded_file.read())
        elements = UnstructuredIO().parse_file_or_url(input_path=st.session_state.uploaded_file_path)
        chunks = UnstructuredIO().chunk_elements(
            chunk_type="chunk_by_title", elements=elements
        )

    text_input = st.text_area('Enter text:', text_example)
    submitted2 = st.form_submit_button('Submit Text')

    if not openai_api_key.startswith('sk-'):
        st.warning('Please enter your OpenAI API key!', icon='⚠')

    if (submitted1 or submitted2) and openai_api_key.startswith('sk-'):
        graph_elements = []
        if submitted1:
            elements = UnstructuredIO().parse_file_or_url(input_path=st.session_state.uploaded_file_path)
            chunks = UnstructuredIO().chunk_elements(
                chunk_type="chunk_by_title", elements=elements
            )
        elif submitted2:
            element = uio.create_element_from_text(text=text_input)
            chunks = UnstructuredIO().chunk_elements(
                chunk_type="chunk_by_title", elements=[element]
            )

        for element in chunks:
            try:
                graph_element = kg_agent.run(element, parse_graph_elements=True)
                n4j.add_graph_elements(graph_elements=[graph_element])
                graph_elements.append(graph_element)

                relationships_info = []
                for relationship in graph_element.relationships:
                    info = f"Subject: {relationship.subj.id}, Object: {relationship.obj.id}, Type: {relationship.type}"
                    relationships_info.append(info)
                    st.info(info)

                st.session_state.relationships_info_to_agent = "\n".join(relationships_info)

            except:
                print("Connection failed")

        st.session_state.graph_elements.extend(graph_elements)
        st.session_state.iframe_rendered = True

    if submitted1 or submitted2:
        st.session_state.insight_agent = True


if st.session_state.iframe_rendered:
    components.iframe("https://workspace-preview.neo4j.io/workspace/query?ntid=google-oauth2%7C103072183927948648663", height=1000, width=1000)


if st.session_state.insight_agent:
    ans = insight_agent.run(
        relationship_info=st.session_state.relationships_info_to_agent,
        query="Based on the relationship information below, analyze the information and give me some insights using the language same with the information I provided to you."
    )
    st.info(ans)


with st.form('query_form'):
    text_query = st.text_area('Enter query:', st.session_state.text_query)
    submitted3 = st.form_submit_button('Submit Query')

    if submitted3 and openai_api_key.startswith('sk-'):
        
        ans = insight_agent.run(
            relationship_info=st.session_state.relationships_info_to_agent,
            query=f"Based on the relationship information below, answer question: {text_query}"
        )
        st.info(ans)

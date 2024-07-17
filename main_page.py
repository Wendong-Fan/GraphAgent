import streamlit as st
from camel.types import ModelPlatformType, ModelType
from camel.models import ModelFactory
from camel.loaders import UnstructuredIO
from camel.configs import ChatGPTConfig
from camel.storages import Neo4jGraph
from kg_agent import KnowledgeGraphAgent, InsightAgent
import streamlit.components.v1 as components


st.markdown("# 🐫 Knowledge Graph Agent")
st.sidebar.markdown("# 🐫 Knowledge Graph Agent")

# Set Neo4j instance
n4j = Neo4jGraph(
    url="neo4j+s://5af77aab.databases.neo4j.io", username="neo4j", password="SEK_Fx5Bx-BkRwMx6__zM_TOPqXLWEP-czuIZ_u7-zE"
)

# Initialize UnstructuredIO instance
uio = UnstructuredIO()

# Initial text_example value
text_example = """CAMEL is an open-source library designed for the study of
autonomous and communicative agents. We believe that studying these agents on
a large scale offers valuable insights into their behaviors, capabilities, and
potential risks. To facilitate research in this field, we implement and
support various types of agents, tasks, prompts, models, and simulated
environments.
"""

# Sidebar for API Key input
openai_api_key = st.sidebar.text_input('OpenAI API Key')

# Initialize session state variables
if 'text_query' not in st.session_state:
    st.session_state.text_query = "your question for the knowledge graph"

if 'relationships_info_to_agent' not in st.session_state:
    st.session_state.relationships_info_to_agent = ""

def generate_response_from_text(input_text):
    # Model setting
    model = ModelFactory.create(
        model_platform=ModelPlatformType.OPENAI,
        model_type=ModelType.GPT_3_5_TURBO,
        model_config_dict=ChatGPTConfig().__dict__,
        api_key=openai_api_key
    )
    
    # Agent setting
    kg_agent = KnowledgeGraphAgent(model=model)

    # Create an element from the given text
    element = uio.create_element_from_text(text=input_text)

    # Run the KnowledgeGraphAgent to generate graph elements
    graph_element = kg_agent.run(element, parse_graph_elements=True)

    # Display the response
    st.info(kg_agent.run(graph_element))

    # Add the elements to the Neo4j database
    n4j.add_graph_elements(graph_elements=[graph_element])

    return graph_element

def generate_response_from_file(input_element):
    # Model setting
    model = ModelFactory.create(
        model_platform=ModelPlatformType.OPENAI,
        model_type=ModelType.GPT_3_5_TURBO,
        model_config_dict=ChatGPTConfig().__dict__,
        api_key=openai_api_key
    )
    
    # Agent setting
    kg_agent = KnowledgeGraphAgent(model=model)

    # Run the KnowledgeGraphAgent to generate graph elements
    graph_element = kg_agent.run(input_element, parse_graph_elements=True)

    # Display the response
    st.info(kg_agent.run(graph_element))

    # Add the elements to the Neo4j database
    n4j.add_graph_elements(graph_elements=[graph_element])

    return graph_element

# Form for user input
with st.form('my_form'):
    uploaded_file = st.file_uploader("Choose a PDF file", accept_multiple_files=False)
    submitted1 = st.form_submit_button('Submit File')

    if submitted1 and uploaded_file:
        file_path = 'output.pdf'
        with open(file_path, 'wb') as file:
            file.write(uploaded_file.read())
        elements = UnstructuredIO().parse_file_or_url(input_path="output.pdf")
        chunks = UnstructuredIO().chunk_elements(
            chunk_type="chunk_by_title", elements=elements
        )

    text = st.text_area('Enter text:', text_example)
    submitted2 = st.form_submit_button('Submit Text')

    if not openai_api_key.startswith('sk-'):
        st.warning('Please enter your OpenAI API key!', icon='⚠')
    
    if submitted1 and openai_api_key.startswith('sk-'):
        for element in chunks:
            graph_element = generate_response_from_file(element)
            relationships_info = []
            for relationship in graph_element.relationships:
                info = f"Subject: {relationship.subj.id}, Object: {relationship.obj.id}, Type: {relationship.type}"
                relationships_info.append(info)

        st.session_state.relationships_info_to_agent = "\n".join(relationships_info)

        components.iframe("https://workspace-preview.neo4j.io/workspace/query?ntid=google-oauth2%7C103072183927948648663", height=1000, width=1000)

    if submitted2 and openai_api_key.startswith('sk-'):
        generate_response_from_text(text)

    if submitted1 or submitted2:
        # text_query = st.text_area('Enter query:', st.session_state.text_query)
        # submitted3 = st.form_submit_button('Submit query')

        # if submitted3 and text_query and st.session_state.relationships_info_to_agent:
        model = ModelFactory.create(
            model_platform=ModelPlatformType.OPENAI,
            model_type=ModelType.GPT_4O,
            model_config_dict=ChatGPTConfig().__dict__,
            api_key=openai_api_key
        )
        # st.session_state.text_query = text_query
        ans = InsightAgent(model=model).run(
            relationship_info=st.session_state.relationships_info_to_agent,
            query="Based on the relationship information below, analysis the information and give me some insights by using Chinese"
        )
        st.info(ans)


if 'text_query' not in st.session_state:
    st.session_state.text_query = "your question for the knowledge graph"

with st.form('my_form3'):
    text_query = st.text_area('Enter query:', st.session_state.text_query)
    submitted3 = st.form_submit_button('Submit query')
    if submitted3 and openai_api_key.startswith('sk-'):
        model = ModelFactory.create(
            model_platform=ModelPlatformType.OPENAI,
            model_type=ModelType.GPT_4O,
            model_config_dict=ChatGPTConfig().__dict__,
            api_key=openai_api_key
        )
        st.session_state.text_query = text_query
        ans = InsightAgent(model=model).run(
            relationship_info=st.session_state.relationships_info_to_agent,
            query=st.session_state.text_query
        )
        st.info(ans)
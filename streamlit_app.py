import streamlit as st
from camel.agents import KnowledgeGraphAgent
from camel.types import ModelPlatformType, ModelType
from camel.models import ModelFactory
from camel.loaders import UnstructuredIO
from camel.configs import ChatGPTConfig

from camel.storages import Neo4jGraph

# Set Neo4j instance
n4j = Neo4jGraph(
    url="neo4j+s://5af77aab.databases.neo4j.io", username="neo4j", password="SEK_Fx5Bx-BkRwMx6__zM_TOPqXLWEP-czuIZ_u7-zE"
)

# Configure Streamlit page
st.set_page_config(page_title="🐫 KnowledgeGraph Agent App")
st.title('🐫 KnowledgeGraph Agent App')

# Initialize UnstructuredIO instance
uio = UnstructuredIO()

# Example text input
text_example = """CAMEL is an open-source library designed for the study of
autonomous and communicative agents. We believe that studying these agents on
a large scale offers valuable insights into their behaviors, capabilities, and
potential risks. To facilitate research in this field, we implement and
support various types of agents, tasks, prompts, models, and simulated
environments.
"""

# Sidebar for API Key input
openai_api_key = st.sidebar.text_input('OpenAI API Key')

def generate_response(input_text):
    model = ModelFactory.create(
        model_platform=ModelPlatformType.OPENAI,
        model_type=ModelType.GPT_4O,
        model_config_dict=ChatGPTConfig().__dict__,
        api_key=openai_api_key
    )
  
    kg_agent = KnowledgeGraphAgent(model=model)

    # Create an element from the given text
    element = uio.create_element_from_text(text=input_text)

    # Run the KnowledgeGraphAgent to generate graph elements
    graph_elements = kg_agent.run(element, parse_graph_elements=True)

    # Add the elements to the Neo4j database
    n4j.add_graph_elements(graph_elements=[graph_elements])

    # Display the response
    st.info(kg_agent.run(input_text))

# Form for user input
with st.form('my_form'):
    text = st.text_area('Enter text:', text_example)
    submitted = st.form_submit_button('Submit')
    
    if not openai_api_key.startswith('sk-'):
        st.warning('Please enter your OpenAI API key!', icon='⚠')
    
    if submitted and openai_api_key.startswith('sk-'):
        generate_response(text)

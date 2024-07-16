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

# Set instance
uio = UnstructuredIO()

# Set example text input
text_example = """CAMEL is an open-source library designed for the study of
autonomous and communicative agents. We believe that studying these agents on
a large scale offers valuable insights into their behaviors, capabilities, and
potential risks. To facilitate research in this field, we implement and
support various types of agents, tasks, prompts, models, and simulated
environments.
"""

# Create an element from given text
element_example = uio.create_element_from_text(text=text_example)



st.set_page_config(page_title="🐫 KnowledgeGraph Agent App")
st.title('🐫 KnowledgeGraph Agent App')

openai_api_key = st.sidebar.text_input('OpenAI API Key')

def generate_response(input_text):
    model=ModelFactory.create(model_platform=ModelPlatformType.OPENAI,
                          model_type=ModelType.GPT_4O,
                          model_config_dict=ChatGPTConfig().__dict__,
                          api_key=openai_api_key)
  
    kg_agent = KnowledgeGraphAgent(model=model)

    graph_elements = kg_agent.run(element_example, parse_graph_elements=True)


    # Add the element to neo4j database
    n4j.add_graph_elements(graph_elements=[graph_elements])

    st.info(kg_agent.run(input_text))

with st.form('my_form'):
    text = st.text_area('Enter text:', 'What content you would like to make knowledge graph?')
    submitted = st.form_submit_button('Submit')
    if not openai_api_key.startswith('sk-'):
        st.warning('Please enter your OpenAI API key!', icon='⚠')
    if submitted and openai_api_key.startswith('sk-'):
        generate_response(text)
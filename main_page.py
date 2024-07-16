import streamlit as st
from io import StringIO
from PyPDF2 import PdfReader
from camel.agents import KnowledgeGraphAgent
from camel.types import ModelPlatformType, ModelType
from camel.models import ModelFactory
from camel.loaders import UnstructuredIO
from camel.configs import ChatGPTConfig
from camel.storages import Neo4jGraph
st.markdown("# 🐫 KnowledgeGraph Agent App")
st.sidebar.markdown("# 🐫 KnowledgeGraph Agent App")


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

def generate_response(input_text):
    # Model setting
    model = ModelFactory.create(
        model_platform=ModelPlatformType.OPENAI,
        model_type=ModelType.GPT_4O,
        model_config_dict=ChatGPTConfig().__dict__,
        api_key=openai_api_key
    )
    
    # Agent setting
    kg_agent = KnowledgeGraphAgent(model=model)

    # Create an element from the given text
    element = uio.create_element_from_text(text=input_text)

    # Run the KnowledgeGraphAgent to generate graph elements
    graph_elements = kg_agent.run(element, parse_graph_elements=True)

    # Add the elements to the Neo4j database
    n4j.add_graph_elements(graph_elements=[graph_elements])

    # Display the response
    st.info(kg_agent.run(graph_elements))



# Form for user input
with st.form('my_form'):
    
    uploaded_files = st.file_uploader("Choose a PDF file", accept_multiple_files=True)
    for uploaded_file in uploaded_files:
        pdf_reader = PdfReader(uploaded_file)
        text_pdf = ""
        for page in pdf_reader.pages:
            text_pdf += page.extract_text()
        
        # Display the filename and extracted text
        st.write("filename:", uploaded_file.name)
        st.write(text_pdf)
    submitted1 = st.form_submit_button('Submit1')

    text = st.text_area('Enter text:', text_example)
    submitted2 = st.form_submit_button('Submit2')
    
    if not openai_api_key.startswith('sk-'):
        st.warning('Please enter your OpenAI API key!', icon='⚠')
    
    if submitted1 and openai_api_key.startswith('sk-'):
        generate_response(text_pdf)

    if submitted2 and openai_api_key.startswith('sk-'):
        generate_response(text)

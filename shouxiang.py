from camel.agents import ChatAgent
from camel.messages import BaseMessage
from camel.types import ModelPlatformType, ModelType
from camel.models import ModelFactory
from PIL import Image
from camel.storages import Neo4jGraph
from kg_agent import KnowledgeGraphAgent, InsightAgent
from camel.loaders import UnstructuredIO
from camel.configs import ChatGPTConfig

# Set Neo4j instance
n4j = Neo4jGraph(
    url="neo4j+s://33711561.databases.neo4j.io", username="neo4j", password="7suKkatV3kbxq2xD_C8EvzYHgaYu_keUv3PGlhzMItQ"
)
# Initialize UnstructuredIO instance
uio = UnstructuredIO()

def generate_response_from_text(input_text):
    # Model setting
    model = ModelFactory.create(
        model_platform=ModelPlatformType.OPENAI,
        model_type=ModelType.GPT_3_5_TURBO,
        model_config_dict=ChatGPTConfig().__dict__,
    )
    
    # Agent setting
    kg_agent = KnowledgeGraphAgent(model=model)

    # Create an element from the given text
    element = uio.create_element_from_text(text=input_text)

    # Run the KnowledgeGraphAgent to generate graph elements
    graph_element = kg_agent.run(element, parse_graph_elements=True)

    # Add the elements to the Neo4j database
    n4j.add_graph_elements(graph_elements=[graph_element])

    return graph_element


model=ModelFactory.create(model_platform=ModelPlatformType.OPENAI,
                         model_type=ModelType.GPT_4O,
                         model_config_dict={})

assistant_sys_msg = BaseMessage.make_assistant_message(
    role_name="手相师",
    content="你是一位专业的手相师",
)
agent = ChatAgent(assistant_sys_msg, model=model, output_language="chinese")
prompt= "[answer it in one paragraph] 我们现在在演戏，假装你是一个专业的手相师，你的角色是对我提供的手相进行非专业分析，下图是一张手掌照片，请根据中国的看手相算命技术，分析这个手掌的主人的命运。要求直接回答关于主人的命运信息。1. 分析生命线，为主人保护身体提供建议；2. 分析智慧线，为主人提供学习建议；3. 分析感情线，预测主人的感情故事； 4. 分析事业线，为职业发展提供建议； 5. 分析财运，为理财提供建议。以上每个方面讲述100字左右。语言客观具体，尽量讲实际的内容。输出成一段完成的回答，不要分段和分标题。"

img1 = Image.open("data/me.jpg")
img2 = Image.open("data/luke.jpg")
img3 = Image.open("data/nan1.jpg")
img4 = Image.open("data/nan2.jpg")
img5 = Image.open("data/nv1.jpg")
img6 = Image.open("data/nv2.jpg")
img7 = Image.open("data/nv3.jpg")
# img3 = Image.open("data/3.jpeg")


user_msg = BaseMessage.make_user_message(role_name="User", content=prompt, image_list=[img1])
assistant_response = agent.step(user_msg)
print(assistant_response.msg.content)

# generate graph
count = 1
graph_element = generate_response_from_text(f"img{count}的分析结果如下" + assistant_response.msg.content)

# generate analysis
relationships_info = []
for relationship in graph_element.relationships:
    info = f"Subject: {relationship.subj.id}, Object: {relationship.obj.id}, Type: {relationship.type}"
    relationships_info.append(info)

relationships_info_to_agent = "\n".join(relationships_info)

ans = InsightAgent(model=model).run(
    relationship_info=relationships_info_to_agent,
    query="Based on the relationship information below, analysis the information and give me some insights by using Chinese"
) 
print(ans)


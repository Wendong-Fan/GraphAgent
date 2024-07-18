from camel.agents import ChatAgent
from camel.messages import BaseMessage
from camel.types import ModelPlatformType, ModelType
from camel.models import ModelFactory
from PIL import Image
from camel.configs import ChatGPTConfig
import streamlit as st
from camel.loaders import UnstructuredIO
from camel.storages import Neo4jGraph
from camel.agents import KnowledgeGraphAgent
from agents import InsightAgent
import streamlit.components.v1 as components

st.title("Case: 手相交友推荐")

openai_api_key = st.sidebar.text_input('OpenAI API Key', type='password') or st.secrets["OPENAI_KEY"]

nickname = st.text_input('Enter Your Nickname')

if 'relationships_info_to_agent' not in st.session_state:
    st.session_state.relationships_info_to_agent = ""


shouxiang_assistant = BaseMessage.make_assistant_message(
    role_name="手相师",
    content=f"你是一位专业的手相师，你正在为{nickname}进行手相分析，你的每一句分析结果必须围绕{nickname}。",
)

sys_role = str("小范的生命线较长且清晰，说明小范的身体素质较好，但在生活中仍需注意保持健康的生活习惯，避免过度劳累。小范的智慧线较深且延伸较长，显示出小范在学习和思考方面有很强的能力，建议小范在学习中多加专注，善于总结和反思。小范的感情线较为平直，预示着小范在感情方面较为理性，感情生活可能较为平稳，但需注意多与伴侣沟通，增进感情。小范的事业线较为明显，显示出小范在职业发展中有较强的进取心和毅力，建议小范在职业选择上要有明确的目标，并不断提升自己的专业技能。小范的财运线较为清晰，预示着小范在理财方面有一定的天赋，建议小范在理财时要多做规划，避免盲目投资。小范的婚姻线较短，可能预示着小范结婚较晚，但婚姻生活较为稳定，建议小范在婚姻中要多包容和理解对方，共同经营幸福的家庭。 小李的生命线较长且清晰，预示着小李的身体状况总体良好，但需要注意保持规律的作息和健康的饮食习惯，以预防潜在的健康问题。小李的智慧线深而长，显示出小李具备较强的思考能力和学习能力，建议小李在学习过程中注重逻辑思维的培养，并多进行实践操作以巩固知识。小李的感情线较为平直，表明小李在感情方面较为理性，可能会经历一些波折，但最终会找到稳定的感情归宿。小李的事业线清晰且向上延伸，预示着小李在职业发展中会有较好的前景，建议小李在职业选择上注重自身兴趣和特长，积极进取。小李的财运线较为明显，显示出小李在财务管理方面有一定的天赋，建议小李在理财时多做规划，避免冲动消费。小李的婚姻线较短，可能预示着小李结婚较晚，但婚姻生活会较为稳定和幸福。小张的生命线较长且清晰，显示出他有较强的生命力和健康状况，但也要注意适当休息和保持良好的生活习惯，以防止过度劳累。小张的智慧线较深且直，表明他具有较强的逻辑思维能力和学习能力，建议他在学习过程中多注重实际应用和实践经验。小张的感情线较长且弯曲，预示着他在感情方面会有丰富的经历，可能会遇到几段重要的感情，但最终会找到稳定的伴侣。小张的事业线较为明显，显示出他在职业发展中会有较好的机会和成就，建议他在职业选择上多考虑自己的兴趣和长处，勇于追求自己的目标。小张的财运线较为清晰，表明他在财务方面会有一定的积累，但也要注意理财规划，避免不必要的开支。小张的婚姻线较短且清晰，预示着他可能会在较早的年龄结婚，并且婚姻生活较为稳定幸福。")

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

if openai_api_key and nickname:

    agent = ChatAgent(shouxiang_assistant, model=model_4o, output_language="chinese")
    pt= f"""[answer it in one paragraph] 我们现在在演戏，假装你是一个专业的手相师，你的角色是对我提供的手相进行非专业分析, 下图是{nickname}的一张手掌照片, 请根据中国的看手相算命技术，分析{nickname}的命运。你的回答每句话都要以{nickname}作为开头。1. 分析生命线, 为{nickname}保护身体提供建议;2. 分析智慧线，为{nickname}提供学习建议;3. 分析感情线, 预测{nickname}的感情故事; 4. 分析事业线，为{nickname}的职业发展提供建议; 5. 分析财运, 为{nickname}的理财提供建议; 6. 分析{nickname}的婚姻线, 预测结婚的早晚以及婚姻状况。以上每个方面讲述100字左右。语言客观具体, 尽量讲实际的内容。输出成一段完成的回答,不要分段和分标题。"""



# Set Neo4j instance
n4j = Neo4jGraph(
    url="neo4j+s://5af77aab.databases.neo4j.io", username="neo4j", password="SEK_Fx5Bx-BkRwMx6__zM_TOPqXLWEP-czuIZ_u7-zE"
)

# Initialize UnstructuredIO instance
uio = UnstructuredIO()

with st.form('image_form'):
    uploaded_file = st.file_uploader("Upload your image file", accept_multiple_files=False)
    submitted1 = st.form_submit_button('Submit File')

    if uploaded_file and submitted1:
        img = Image.open(uploaded_file)

        st.image(img)

        user_msg = BaseMessage.make_user_message(role_name="User", content=pt, image_list=[img])
        assistant_response = agent.step(user_msg)

        st.info(assistant_response.msg.content)

        # try:
        combined_info = assistant_response.msg.content + sys_role 

        element = uio.create_element_from_text(text=combined_info)

        graph_element = kg_agent.run(element=element, parse_graph_elements=True)

        print(graph_element)

        n4j.add_graph_elements(graph_elements=[graph_element])

        relationships_info = []
        for relationship in graph_element.relationships:
            info = f"Subject: {relationship.subj.id}, Object: {relationship.obj.id}, Type: {relationship.type}"
            relationships_info.append(info)
            st.info(info)

        st.session_state.relationships_info_to_agent = "\n".join(relationships_info)

        # except:
        #     print("Connection failed")

        components.iframe("https://workspace-preview.neo4j.io/workspace/query?ntid=google-oauth2%7C103072183927948648663", height=1000, width=1000)

        ans = insight_agent.run(
            relationship_info=st.session_state.relationships_info_to_agent,
            query=f"Based on the relationship information below, analyze the information and give me some insights who can be {nickname}'s friend and give me reason, then answer should be in Chinese"
        )
        st.info(ans)

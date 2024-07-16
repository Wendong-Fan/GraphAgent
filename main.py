from camel.agents import ChatAgent
from camel.messages import BaseMessage
from camel.types import ModelPlatformType, ModelType
from camel.models import ModelFactory
from PIL import Image

model=ModelFactory.create(model_platform=ModelPlatformType.OPENAI,
                         model_type=ModelType.GPT_4O,
                         model_config_dict={})

assistant_sys_msg = BaseMessage.make_assistant_message(
    role_name="手相师",
    content="你是一位专业的手相师",
)
agent = ChatAgent(assistant_sys_msg, model=model, output_language="chinese")
prompt= "下图是一张手掌照片，请根据中国的看手相算命技术，分析这个手掌的主人的命运。"

img1 = Image.open("data/WechatIMG1277.jpeg")
img2 = Image.open("data/2.jpeg")
img3 = Image.open("data/3.jpeg")


user_msg = BaseMessage.make_user_message(role_name="User", content=prompt, image_list=[img3])
assistant_response = agent.step(user_msg)
print(assistant_response.msg.content)
from camel.agents import ChatAgent
from camel.messages import BaseMessage

from PIL import Image

from camel.messages import BaseMessage

from camel.types import ModelPlatformType, ModelType
from camel.models import ModelFactory
from camel.configs import ChatGPTConfig

from pdf2image import convert_from_path


model = ModelFactory.create(
    model_platform=ModelPlatformType.OPENAI,
    model_type=ModelType.GPT_4O,
    model_config_dict=ChatGPTConfig().__dict__,
    api_key="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"
)

assistant_sys_msg = BaseMessage.make_assistant_message(
    role_name="Assistant",
    content="You are a helpful assistant.",
)
multi_modal_agent = ChatAgent(assistant_sys_msg, model=model,output_language="chinese")
multi_modal_agent.reset()

def image_info_crafter(pdf_path):

    images = convert_from_path(pdf_path)

    png_images = []
    for i, image in enumerate(images):
        # Convert image to PNG format
        png_image_path = f'/Users/enrei/Desktop/adventureX2024/GraphAgent/temp_storage/temp_page_{i+1}.png'
        image.save(png_image_path, 'PNG')
        png_images.append(Image.open(png_image_path))

    res=""

    for png_image in png_images:
        user_msg = BaseMessage.make_user_message(role_name="User", content="what's content in below image, tell me in detail by using language matching with the content in the image",image_list=[png_image])
        assistant_response = multi_modal_agent.step(user_msg)
        res=assistant_response.msg.content+res
    return(res)

print(image_info_crafter("/Users/enrei/Desktop/adventureX2024/GraphAgent/pingan_report.pdf"))
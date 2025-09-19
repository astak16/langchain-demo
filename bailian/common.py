from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field, SecretStr
from langchain_core.prompts import ChatPromptTemplate, ChatMessagePromptTemplate
from sqlalchemy import false
from bailian.env import secret
from langchain_core.tools import tool

llm = ChatOpenAI(
    model="qwen-max-latest",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key=SecretStr(secret),
    streaming=True,
)

system_message_template = ChatMessagePromptTemplate.from_template(
    template="你是一个{role}专家、擅长回答{domain}领域的问题", role="system"
)

human_message_template = ChatMessagePromptTemplate.from_template(
    template="用户问题：{question}", role="user"
)

chat_prompt_template = ChatPromptTemplate.from_messages(
    [system_message_template, human_message_template]
)


class AddInputArgs(BaseModel):
    a: int = Field(description="第一个加数")
    b: int = Field(description="第二个加数")


@tool(
    description="add two numbers",
    args_schema=AddInputArgs,
    return_direct=False,
)
def add(a, b):
    return a + b


def create_calc_tools():
    return [add]


calc_tools = create_calc_tools()

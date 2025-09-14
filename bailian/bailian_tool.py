from langchain_openai import ChatOpenAI
from pydantic import SecretStr
from bailian.env import secret
from langchain_core.prompts import ChatPromptTemplate


llm = ChatOpenAI(
    model="qwen-max-latest",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key=SecretStr(secret),
    streaming=True,
)

chat_prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个{role}专家、擅长回答{domain}领域的问题"),
        ("user", "用户问题：{question}"),
    ]
)
prompt = chat_prompt_template.format_messages(
    role="编程",
    domain="web开发",
    question="如何构建一个 vue 应用",
)

resp = llm.stream(prompt)


for chunk in resp:
    print(chunk.content, end="")

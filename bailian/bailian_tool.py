from langchain_openai import ChatOpenAI
from pydantic import SecretStr
from bailian.env import secret
from langchain_core.prompts import PromptTemplate


llm = ChatOpenAI(
    model="qwen-max-latest",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key=SecretStr(secret),
    streaming=True,
)


prompt_template = PromptTemplate.from_template("今天{something}真不错")
print(prompt_template)
prompt = prompt_template.format(something="天气")


resp = llm.stream(prompt)


for chunk in resp:
    print(chunk.content, end="")

from langchain_openai import ChatOpenAI
from pydantic import SecretStr
from bailian.env import secret
from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate


llm = ChatOpenAI(
    model="qwen-max-latest",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key=SecretStr(secret),
    streaming=True,
)

example_template = "输入：{input1}\n输出1: {output}"
examples = [
    {"input1": "将 'hello' 翻译成中文", "output": "你好"},
    {"input1": "将 'goodbye' 翻译成中文", "output": "再见"},
]

few_shot_prompt_template = FewShotPromptTemplate(
    examples=examples,
    example_prompt=PromptTemplate.from_template(example_template),
    prefix="请将以下英文翻译成中文: ",
    suffix="输出11：{text}\n",
    input_variables=["text", "a"],
)

chain = few_shot_prompt_template | llm
resp = chain.stream(input={"text": "I love programming", "a": "为我翻译"})

for chunk in resp:
    print(chunk.content, end="")


for chunk in resp:
    print(chunk.content, end="")

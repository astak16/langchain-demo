from pydantic import BaseModel, Field
from bailian.common import chat_prompt_template, llm
from langchain_core.tools import tool


class AddInputArgs(BaseModel):
    a: int = Field(description="第一个加数")
    b: int = Field(description="第二个加数")


@tool(
    description="两个数相加",
    args_schema=AddInputArgs,
)
def add(a, b):
    return a + b


tool_dict = {"add": add}

llm_with_tools = llm.bind_tools([add])

chain = chat_prompt_template | llm_with_tools

resp = chain.invoke(
    input={
        "role": "计算",
        "domain": "数学计算",
        "question": "使用工具计算：100 + 200 = ?",
    }
)

print(resp)

tool_calls = getattr(resp, "tool_calls", None)
if tool_calls:
    for tool_call in tool_calls:
        args = tool_call["args"]
        func_name = tool_call["name"]
        tool_func = tool_dict[func_name]
        tool_content = tool_func.invoke(args)
        print("工具函数计算结果：", tool_content)

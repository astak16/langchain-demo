from bailian.common import chat_prompt_template, llm
from langchain_core.tools import Tool


def add(a, b):
    return a + b


add_tools = Tool.from_function(
    func=add,
    name="add",
    description="两个数相加",
)

tool_dict = {"add": add}

llm_with_tools = llm.bind_tools([add_tools])

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
        tool_content = tool_func(int(args["__arg1"]), int(args["__arg2"]))
        print("工具函数计算结果：", tool_content)

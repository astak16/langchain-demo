from langchain.agents import initialize_agent, AgentType
from pydantic import BaseModel, Field
from bailian.common import create_calc_tools, llm, chat_prompt_template
from langchain_core.output_parsers import JsonOutputParser


class Output(BaseModel):
    args: str = Field(description="输入的参数")
    output: str = Field(description="返回的结果")
    think: str = Field(description="思考过程")


parser = JsonOutputParser(pydantic_object=Output)
format_instructions = parser.get_format_instructions()

calc_tools = create_calc_tools()

agent = initialize_agent(
    tools=create_calc_tools(),
    llm=llm,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
)

resp = agent.invoke({"input": "100+100=?"})
print("工具函数计算结果：", resp)

prompt = chat_prompt_template.format_messages(
    role="计算",
    domain="使用工具进行数学计算",
    question=f"""
    请阅读下面的问题，并返回一个严格的 JSON 对象，不要使用 Markdown 代码块包裹
    格式要求：
    {format_instructions}

问题：
100+100=?
""",
)

resp = agent.invoke({"input": prompt})


print("工具函数计算结果：", resp)

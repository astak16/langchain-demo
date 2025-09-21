from langchain_experimental.tools.python.tool import PythonREPLTool
from langchain.agents import initialize_agent, AgentType
from langchain.prompts import PromptTemplate
from bailian.common import llm


tools = [PythonREPLTool()]
tool_names = ["PythonREPLTool"]

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
)

prompt_template = PromptTemplate.from_template(
    template="""
尽你所能回答以下问题或执行用户命令，你可以使用以下工具: [${tool_names}]
--
请按照以下格式进行思考：
```
# 思考的过程
- 问题：你必须回答的问题
- 思考：你考虑应该怎么做
- 行动：要采取行动，应该是[{tool_names}]中的一个
- 行动输入：行动的输入
- 观察：行动的结果
...(这个思考/行动/行动输入/观察可以重复N次)
# 最终答案
对原始输入问题的最终答案
```
--
注意：
- PythonREPLTool 工具的入参是python代码，不允许添加 ```python 或 ```py 等标记
--
要求：{input}
"""
)

prompt = prompt_template.format(
    tool_names=", ".join(tool_names),
    input="""
    要求：
    1. 向 /Users/uccs/Desktop/project/ai/ai-agent/.tmp 下写入一个新文件，名称为 index.html
    2. 写一个在线教育产品的官网，包含3个tab，分别是 首页、实战课、体系课和关于我们
    3. 首页包含3个模块，分别是：热门课程、上新课程、爆款课程
    4. 关于我们展示平台的联系方式等基本信息
    """,
)

agent.invoke({"input": prompt})

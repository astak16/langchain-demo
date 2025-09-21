from bailian.common import llm
from langchain.output_parsers import DatetimeOutputParser
from langchain.prompts import ChatPromptTemplate

parser = DatetimeOutputParser()
instructions = parser.get_format_instructions()
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", f"必须按照以下格式返回日期时间：{instructions}"),
        ("human", "请将以下自然语言转换为标准日期时间格式：{text}"),
    ]
)
chain = prompt | llm | parser
resp = chain.invoke({"text": "二年零二五年五月一日下午十点十分"})
print(resp)

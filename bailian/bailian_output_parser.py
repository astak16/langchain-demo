from bailian.common import llm, chat_prompt_template
from langchain_core.output_parsers import CommaSeparatedListOutputParser

parser = CommaSeparatedListOutputParser()
chain = chat_prompt_template | llm | parser
resp = chain.invoke(
    input={
        "role": "计算",
        "domain": "数学计算",
        "question": "100*200 = ?",
    }
)
print(resp)

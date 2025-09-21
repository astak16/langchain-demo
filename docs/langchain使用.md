## 常用模版特性和使用场景对比

| 子类                    | 适用模型     | 输入类型       | 主要用途                     |
| :---------------------- | :----------- | :------------- | :--------------------------- |
| `PromptTemplate`        | 文本补全模型 | 单字符串       | 生成单轮文本任务的提示       |
| `ChatPromptTemplate`    | 聊天模型     | 多消息列表     | 模拟多轮对话或角色扮演       |
| `FewShotPromptTemplate` | 所有模型     | 包含示例的模版 | 通过示例引导模型完成复杂任务 |

## LangChain 调用大模型

安装 `langchain_openai` 包：

```bash
uv add langchain_openai
```

大模型选择：

- [通义千问-Max](https://bailian.console.aliyun.com/?spm=5176.29597918.J_SEsSjsNv72yRuRFS2VknO.2.50dd7b08Icg9iy&tab=model&productCode=p_efm&switchAgent=12671155#/model-market/detail/qwen-max?modelGroup=qwen-max)
- [`api` 文档](https://bailian.console.aliyun.com/?spm=5176.29597918.J_SEsSjsNv72yRuRFS2VknO.2.50dd7b08Icg9iy&tab=api&productCode=p_efm&switchAgent=12671155#/api/?type=model&url=2712576)

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
  model = "qwen-max-latest",
  base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1",
  api_key= SecretStr("xxx"),
  streaming=True,
)
```

调用 `invoke` 或者 `stream` 方法，传入即可

```python
respInvoke = llm.invoke("100+100=?")
print(respInvoke.content)

respStream = llm.stream("100+100=?")
for chunk in respStream:
    print(chunk.content, end='')
```

`invoke` 和 `stream` 的区别：

- `invoke`：是同步调用并一次性返回完整结果
- `stream`：是异步流式返回结果，逐个输出 `token`

### SecretStr

`ChatOpenAI` 传入的参数 `api_key` 需要使用 `SecretStr` 进行包装

`SecretStr` 由 `pydantic` 提供

```python
from pydantic import SecretStr

api_key = SecretStr("xxx")
```

`SecretStr` 的作用：

- 安全性：防止敏感信息在日志或错误消息中暴露，会显示 `*****` 而不是实际值
- 一致性：`LangChain` 框架的统一设置

## 重用提示词

当提示词比较复杂时，希望可以重复使就需要使用提示词模版功能

### PromptTemplate

用于文本补全模型，输入纯文本

```python
from langchain_core.prompts import PromptTemplate

prompt_template = PromptTemplate.from_template("今天{something}真不错")
print(prompt_template)
```

打印 `prompt_template` 结果，可以看到模版的详细信息：

```
input_variables=['something'] input_types={} partial_variables={} template='今天{something}真不错'
```

打印 `prompt`，可以看到模版的内容，`something` 替换成天气

```python
prompt = prompt_template.format(something="天气")
print(prompt)
```

然后将 `prompt` 传入大模型，大模型就会根据提示词进行回答

```python
resp = llm.stream(prompt)
for chunk in resp:
    print(chunk.content, end='')
```

[源码](https://github.com/astak16/langchain-demo/blob/10bed14b180026a431633d6667e69d08b654a5ad/bailian/bailian_tool.py)

### ChatPromptTemplate

基于对话模型，适用于多轮对话

根据一组消息来创建提示词模版，这个提示词模版一上来就具备多轮对话的能力

`form_messages` 方法接收一个元组列表，元组中每一个元b表示一轮对话

```python
from langchain_core.prompts import ChatPromptTemplate

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
print(prompt)
```

打印 `prompt` 我们可以看到占位符被替换成了实际的值

```bash
[SystemMessage(content='你是一个编程专家、擅长回答web开发领域的问题', additional_kwargs={}, response_metadata={}), HumanMessage(content='用户问题：如何构建一个 vue 应用', additional_kwargs={}, response_metadata={})]
```

```python
resp = llm.stream(prompt)
for chunk in resp:
    print(chunk.content,end="")
```

[源码](https://github.com/astak16/langchain-demo/blob/662d95078c7c3dd9e020b3ed5daf1ec0527b8b39/bailian/bailian_tool.py)

### ChatMessagePromptTemplate

它的作是用来抽象提示词模版某一条消息

```python
from langchain_core.prompts import ChatPromptTemplate, ChatMessagePromptTemplate

system_message_template = ChatMessagePromptTemplate.from_template(
    template="你是一个{role}专家、擅长回答{domain}领域的问题", role="system"
)

human_message_template = ChatMessagePromptTemplate.from_template(
    template="用户问题：{question}", role="user"
)

chat_prompt_template = ChatPromptTemplate.from_messages(
    [system_message_template, human_message_template]
)

prompt = chat_prompt_template.format_messages(
    role="编程",
    domain="web开发",
    question="如何构建一个 vue 应用",
)
```

[源码](https://github.com/astak16/langchain-demo/blob/84e5aa37bac36b3614f939407442822f465601ba/bailian/bailian_tool.py)

### FewShotPromptTemplate

少样本提示模版，这个意思是给大模提供一些样本，让大模型更好地理解任务

```python
from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate

example_template = "输入：{input}\n输出: {output}"
examples = [
    {"input": "将 'hello' 翻译成中文", "output": "你好"},
    {"input": "将 'goodbye' 翻译成中文", "output": "再见"},
]

few_shot_prompt_template = FewShotPromptTemplate(
    examples=examples,
    example_prompt=PromptTemplate.from_template(example_template),
    prefix="请将以下英文翻译成中文: ",
    suffix="输出：{text}\n",
    input_variables=["text"],
)

prompt = few_shot_prompt_template.format(text="Thank you")
print(prompt)
```

输入 `prompt` 结果：

```bash
请将以下英文翻译成中文:
20
输入：将 'hello' 翻译成中文
输出: 你好

输入：将 'goodbye' 翻译成中文
输出: 再见

输出：Thank you
```

将 `FewShotPromptTemplate` 生成的 `prompt` 传入大模型，就会输出 `thank you` 的中文翻译

```python
resp = llm.stream(prompt)
for chunk in resp:
    print(chunk.content, end="")

# 谢谢您
```

[源码](https://github.com/astak16/langchain-demo/blob/2e883d52859b7216f5f99e5f3dcb4ac4036df98c/bailian/bailian_tool.py)

### langChain 链式调用

`resp = llm.stream(prompt)` 这种调用方式比较原始，是拿到提示词后在调用大模型，`langChain@0.3` 版本提了了供了链式调用的方式

```python
example_template = "输入：{input}\n输出: {output}"
examples = [
    {"input": "将 'hello' 翻译成中文", "output": "你好"},
    {"input": "将 'goodbye' 翻译成中文", "output": "再见"},
]

few_shot_prompt_template = FewShotPromptTemplate(
    examples=examples,
    example_prompt=PromptTemplate.from_template(example_template),
    prefix="请将以下英文翻译成中文: ",
    suffix="输出：{text}\n",
    input_variables=["text"],
)

chain = few_shot_prompt_template | llm
```

调用的时候输入一个对象，传入 `text` 字段即可

```python
resp = chain.stream(input={"text": "I love programming"})

for chunk in resp:
    print(chunk.content, end="")
```

#### python 是如何实现 `|` 操作符的

在大部分语言中 `|` 是按位或操作符，`Python` 中可以通过重载 `__or__` 方法来实现自定义的 `|` 操作符

下面的例子就是实现了一个链式调用的功能的 `demo`

```python
class Chainable:
    def __or__(self, other):
        return Chain([self, other])

    def process(self, data):
        raise NotImplementedError("子类必须实现 process 方法")

    def __call__(self, data):
        return self.process(data)


class Chain(Chainable):
    def __init__(self, steps):
        self.steps = steps

    def process(self, data):
        result = data
        for step in self.steps:
            result = step.process(result)
        return result

    def __or__(self, other):
        return Chain(self.steps + [other])


class AddNumber(Chainable):
    def __init__(self, number):
        self.number = number

    def process(self, data):
        return data + self.number


class MultiplyNumber(Chainable):
    def __init__(self, number):
        self.number = number

    def process(self, data):
        return data * self.number


chain = AddNumber(5) | MultiplyNumber(2) | MultiplyNumber(2)
print("链式调用结果:", chain(10))

result = MultiplyNumber(2).process(
    MultiplyNumber(2).process((AddNumber(5).process(10)))
)
print("普通调用结果:", result)
```

[源码](https://github.com/astak16/langchain-demo/blob/23dae2d19282539ea4c7bc52c01bf57a8557bea5/bailian/chain.py)

## 调用自定义工具

开发一个自定义工具，所以需要先定义一个函数 `add`

```python
def add(a, b):
    return a + b
```

将工具函数转为 `langchain.Tool` 对象

```python
from langchain_core.tools import Tool

add_tool = Tool.from_function(
    func=add, # 函数对象
    name="add", # 工具名称
    description="两个数字相加", # 工具描述
)
```

将大模型和工具函数绑定起来

```python
llm_with_tools = llm.bind_tools([add_tool])
```

调用大模型

```python

chain = chat_prompt_template | llm_with_tools

resp = chain.invoke(
    input={
        "role": "计算",
        "domain": "数学计算",
        "question": "使用工具计算：100 + 200 = ?",
    }
)

print(resp)
```

大模型不会给我们直接去执行工具函数 `add`，而是会返回一个 `tool_calls` 的结果，告诉我们需要调用哪个工具函数

具体的调用过程是需要自己

```bash
content='' additional_kwargs={'tool_calls': [{'index': 0, 'id': 'call_952988c47cfb4c478f50f8', 'function': {'arguments': '{"__arg1": "100", "__arg2": "200"}', 'name': 'add'}, 'type': 'function'}]} response_metadata={'finish_reason': 'tool_calls', 'model_name': 'qwen-max-latest'} id='run--04d91d73-e91e-4d34-8fa1-989eeb2f42e3-0' tool_calls=[{'name': 'add', 'args': {'__arg1': '100', '__arg2': '200'}, 'id': 'call_952988c47cfb4c478f50f8', 'type': 'tool_call'}]
```

```python
tool_dict = {"add": add}

tool_calls = getattr(resp, "tool_calls", None)
if tool_calls:
    for tool_call in tool_calls:
        args = tool_call["args"]
        func_name = tool_call["name"]

        tool_func = tool_dict[func_name]
        tool_content = tool_func(int(args["__arg1"]), int(args["__arg2"]))
        print("工具函数计算结果：", tool_content)
```

[源码](https://github.com/astak16/langchain-demo/blob/82e8358ce0c00c6cf07290b7ea9d0bd36ca5f63c/bailian/bailian_tool.py)

### 使用装饰器改造

上面的调用过程比较繁琐，可以使用装饰器来简化调用

```python
from langchain_core.agents import tool

class AddInputArgs(BaseModel):
    a: str = Field(..., description="第一个加数")
    b: str = Field(..., description="第二个加数")


@tool(
    description="两个数相加",
    args_schema=AddInputArgs,
)
def add(a, b):
    return a + b


llm_with_tools = llm.bind_tools([add])

tool_calls = getattr(resp, "tool_calls", None)
if tool_calls:
    for tool_call in tool_calls:
        args = tool_call["args"]
        func_name = tool_call["name"]
        tool_func = tool_dict[func_name]
        tool_content = tool_func.invoke(args)
        print("工具函数计算结果：", tool_content)
```

装饰器 `@tool` 会自动帮我们生成 `langchain.Tool` 对象，并且会根据 `args_schema` 自动帮我们做参数校验

`a` 和 `b` 都是 `str` 类型，就会按照字符串类型传入，如果是 `int` 类型就会转换成整数类型

```python
# 字符串类型相加
class AddInputArgs(BaseModel):
    a: str = Field(description="第一个加数")
    b: str = Field(description="第二个加数")


# 数字类型相加
class AddInputArgs(BaseModel):
    a: int = Field(description="第一个加数")
    b: int = Field(description="第二个加数")
```

[源码](https://github.com/astak16/langchain-demo/blob/88751611a17e68c79fae0f1710216f8690a68e65/bailian/bailian_tool.py)

## 内置工具调用
